"""Run OCR pipelines over a dataset and score them.

Usage:
  .venv/bin/python bench.py <dataset_dir> <results_dir> name=cmd_key[:ENV=VAL,ENV=VAL] ...

A ppocr pipeline whose name ends in "_warm" talks to the warm OCR server
(start it first with `omarchy-ppocr-extract --serve`); any other ppocr pipeline
runs cold in a fresh process per image.

Example:
  bench.py dataset results tesseract=tesseract ppocr=ppocr
  bench.py dev dev_results base=ppocr max960=ppocr:OCR_DET_LIMIT_TYPE=max,OCR_DET_LIMIT_SIDE=960

Each image is OCR'd by launching the pipeline fresh, exactly like a keypress
does, so latency includes process start-up and model loading. Pipelines are
interleaved per image so thermal throttling or background load hits all of them
equally.
"""

import json
import statistics
import sys
from pathlib import Path

import metrics
import runlib


def parse_specs(args):
    specs = []
    for a in args:
        name, rest = a.split("=", 1)
        key, _, envs = rest.partition(":")
        env = dict(kv.split("=", 1) for kv in envs.split(",") if kv)
        if key == "ppocr" and name.endswith("_warm"):
            env.setdefault("OMARCHY_PPOCR_DAEMON", "1")
        elif key == "ppocr":
            env.setdefault("OMARCHY_PPOCR_DAEMON", "0")  # cold, fresh process per image
        specs.append((name, runlib.PIPELINES[key], env))
    return specs


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(q * (len(xs) - 1))))]


def summarize(rows):
    s = lambda k: sum(r[k] for r in rows)
    lat = [r["latency_s"] for r in rows]
    return {
        "images": len(rows),
        "CER": s("cer_edits") / s("cer_chars"),
        "CER_layout": s("layout_edits") / s("layout_chars"),
        "CER_lenient": s("lenient_edits") / s("lenient_chars"),
        "WER": s("wer_edits") / s("wer_words"),
        "bag_F1": statistics.mean(r["bag_f1"] for r in rows),
        "critical_token_acc": s("crit_hit") / max(1, s("crit_total")),
        "line_exact": s("line_hit") / s("line_total"),
        "perfect_images": sum(r["perfect"] for r in rows) / len(rows),
        "latency_mean_s": statistics.mean(lat),
        "latency_p50_s": pct(lat, 0.5),
        "latency_p95_s": pct(lat, 0.95),
        "latency_max_s": max(lat),
        "peak_rss_mean_mb": statistics.mean(r["rss_mb"] for r in rows),
        "peak_rss_max_mb": max(r["rss_mb"] for r in rows),
        "failures": sum(r["exit"] != 0 or not r["chars_out"] for r in rows),
    }


def main():
    data, out = Path(sys.argv[1]), Path(sys.argv[2])
    specs = parse_specs(sys.argv[3:])
    manifest = {m["id"]: m for m in json.loads((data / "manifest.json").read_text())}
    out.mkdir(parents=True, exist_ok=True)

    # Warm the page cache / model files once per pipeline so image #1 isn't penalised.
    first = (data / f"{next(iter(manifest))}.png").read_bytes()
    for _, cmd, env in specs:
        runlib.run(cmd, first, env)

    rows = {name: [] for name, _, _ in specs}
    for sid, meta in manifest.items():
        png = (data / f"{sid}.png").read_bytes()
        gt = (data / f"{sid}.gt.txt").read_text()
        for name, cmd, env in specs:
            text, dt, rss, rc = runlib.run(cmd, png, env)
            (out / name).mkdir(exist_ok=True)
            (out / name / f"{sid}.txt").write_text(text)
            r = {"id": sid, "category": meta["category"], "scale": meta["scale"], "latency_s": dt,
                 "rss_mb": rss, "exit": rc, "chars_out": len(text.strip()), **metrics.score(text, gt)}
            rows[name].append(r)
        print(sid, "  ".join(f"{n}: cer={rows[n][-1]['cer_edits']}/{rows[n][-1]['cer_chars']} {rows[n][-1]['latency_s']:.2f}s"
                             for n in rows), flush=True)

    summary = {"overall": {n: summarize(r) for n, r in rows.items()}, "by_category": {}, "by_scale": {}}
    for n, rs in rows.items():
        for c in sorted({r["category"] for r in rs}):
            summary["by_category"].setdefault(c, {})[n] = summarize([r for r in rs if r["category"] == c])
        for sc in sorted({r["scale"] for r in rs}):
            summary["by_scale"].setdefault(str(sc), {})[n] = summarize([r for r in rs if r["scale"] == sc])
    (out / "per_image.json").write_text(json.dumps(rows, indent=1))
    (out / "summary.json").write_text(json.dumps(summary, indent=1))

    keys = ["CER", "CER_layout", "WER", "bag_F1", "critical_token_acc", "line_exact", "perfect_images",
            "latency_mean_s", "latency_p95_s", "peak_rss_mean_mb", "failures"]
    print("\n" + "metric".ljust(20) + "".join(n.rjust(14) for n in rows))
    for k in keys:
        print(k.ljust(20) + "".join(f"{summary['overall'][n][k]:14.3f}" for n in rows))
    print("\nCER by category")
    for c, d in summary["by_category"].items():
        print(c.ljust(20) + "".join(f"{d[n]['CER']:14.3f}" for n in rows))


if __name__ == "__main__":
    main()
