"""Render bench/RESULTS.md from results/, results_final/ and judge/ summaries."""

import json
import platform
import random
import subprocess
from pathlib import Path

B = Path(__file__).parent
S = json.loads((B / "results/summary.json").read_text())
J = json.loads((B / "judge/judge_summary.json").read_text())
PF = json.loads((B / "results_final/summary.json").read_text())["overall"]["ppocr_cold"]
rows = json.loads((B / "results/per_image.json").read_text())
O = S["overall"]
T, P, TINY = O["tesseract"], O["ppocr"], O["ppocr_tiny"]


def pct(x):
    return f"{100 * x:.1f}%"


def cpu():
    try:
        return next(l.split(":", 1)[1].strip() for l in open("/proc/cpuinfo") if l.startswith("model name"))
    except Exception:
        return platform.processor()


# paired bootstrap of corpus CER difference
Tm = {r["id"]: r for r in rows["tesseract"]}
Pm = {r["id"]: r for r in rows["ppocr"]}
ids = list(Tm)
rng = random.Random(0)
diffs = []
for _ in range(10000):
    s = [rng.choice(ids) for _ in ids]
    c = lambda D: sum(D[i]["cer_edits"] for i in s) / sum(D[i]["cer_chars"] for i in s)
    diffs.append(c(Tm) - c(Pm))
diffs.sort()
better = sum(Pm[i]["cer_edits"] < Tm[i]["cer_edits"] for i in ids)
worse = sum(Pm[i]["cer_edits"] > Tm[i]["cer_edits"] for i in ids)
noacc = [i for i in ids if "accented" not in i]
cer_na = lambda D: sum(D[i]["cer_edits"] for i in noacc) / sum(D[i]["cer_chars"] for i in noacc)

tess_ver = subprocess.run(["tesseract", "--version"], capture_output=True, text=True).stdout.split("\n")[0]

out = []
w = out.append
w("# Benchmark results\n")
w(f"Hardware: **{cpu()}**, no GPU, ONNX Runtime CPU. 100 golden images, every image OCR'd by launching the "
  "pipeline fresh (exactly what happens on a keypress), pipelines interleaved per image.\n")
w(f"- **Omarchy default**: `{tess_ver}`, `--oem 1 --psm 6 -l eng --dpi 300 -c preserve_interword_spaces=1` "
  "(the exact command in `omarchy-capture-text`)")
w("- **omarchy-ppocr**: PP-OCRv6 *small* det + rec via RapidOCR / ONNX Runtime, detection resize `min 320`; "
  "headline accuracy is the run *without* the punctuation fix (`OCR_ASCII_PUNCT=0`), see the end of this report")
w("- *PP-OCRv6 tiny* is shown for reference (lower-end machines); it was not part of the blind judging.\n")

w("## Accuracy and cost\n")
w("| Metric | Omarchy default (Tesseract) | omarchy-ppocr | PP-OCRv6 tiny |")
w("|---|---:|---:|---:|")
spec = [
    ("Character error rate (CER) ↓", "CER", pct),
    ("CER keeping indentation/spacing ↓", "CER_layout", pct),
    ("CER ignoring whitespace & typographic quotes ↓", "CER_lenient", pct),
    ("Word error rate (WER) ↓", "WER", pct),
    ("Bag-of-words F1 (order-free) ↑", "bag_F1", lambda x: f"{x:.3f}"),
    ("Critical tokens exact (URLs, hashes, numbers, paths) ↑", "critical_token_acc", pct),
    ("Lines reproduced exactly ↑", "line_exact", pct),
    ("Images transcribed perfectly ↑", "perfect_images", pct),
    ("Empty output / failures ↓", "failures", lambda x: str(int(x))),
    ("Latency mean ↓", "latency_mean_s", lambda x: f"{x:.2f} s"),
    ("Latency p50 ↓", "latency_p50_s", lambda x: f"{x:.2f} s"),
    ("Latency p95 ↓", "latency_p95_s", lambda x: f"{x:.2f} s"),
    ("Peak RAM (mean) ↓", "peak_rss_mean_mb", lambda x: f"{x:.0f} MB"),
]
for label, k, f in spec:
    lower_better = "↓" in label
    best = min(T[k], P[k]) if lower_better else max(T[k], P[k])
    b = lambda v: f"**{f(v)}**" if v == best else f(v)
    w(f"| {label} | {b(T[k])} | {b(P[k])} | {f(TINY[k])} |")
w("")
w(f"- CER drop is significant: paired bootstrap (10,000 resamples) 95% CI for the CER reduction is "
  f"**{100 * diffs[250]:.1f} to {100 * diffs[9750]:.1f} points**; per image, omarchy-ppocr is better on "
  f"**{better}**, worse on **{worse}**, tied on {100 - better - worse}.")
w(f"- Excluding the accented-text category (Omarchy ships only the English Tesseract model): "
  f"CER {pct(cer_na(Tm))} → **{pct(cer_na(Pm))}**.")
w(f"- Model files on disk: ~31 MB (small det 9.5 MB + rec 21 MB). Tesseract `eng` data: ~23 MB.\n")

F = json.loads((B / "results_final/summary.json").read_text())["overall"]
w("## Release-configuration latency (cold vs warm server)\n")
w("| | Tesseract | omarchy-ppocr cold | omarchy-ppocr warm |")
w("|---|---:|---:|---:|")
for label, k in [("Mean", "latency_mean_s"), ("p50", "latency_p50_s"), ("p95", "latency_p95_s"), ("Max", "latency_max_s")]:
    w(f"| {label} | {F['tesseract'][k]:.2f} s | {F['ppocr_cold'][k]:.2f} s | {F['ppocr_warm'][k]:.2f} s |")
w(f"| CER | {pct(F['tesseract']['CER'])} | {pct(F['ppocr_cold']['CER'])} | {pct(F['ppocr_warm']['CER'])} |")
w("")
w("## Character error rate by category\n")
w("| Category | n | Tesseract | omarchy-ppocr | tiny |")
w("|---|---:|---:|---:|---:|")
for c, d in S["by_category"].items():
    t, p = d["tesseract"]["CER"], d["ppocr"]["CER"]
    w(f"| {c} | {d['ppocr']['images']} | {'**' + pct(t) + '**' if t < p else pct(t)} | {'**' + pct(p) + '**' if p < t else pct(p)} | {pct(d['ppocr_tiny']['CER'])} |")
w("")
w("## By display scale\n")
w("| Scale | n | Tesseract CER | **omarchy-ppocr CER** |")
w("|---|---:|---:|---:|")
for sc, d in S["by_scale"].items():
    w(f"| {sc}x | {d['ppocr']['images']} | {pct(d['tesseract']['CER'])} | **{pct(d['ppocr']['CER'])}** |")
w("")

w("## LLM-as-judge (blind A/B)\n")
w("Claude judged all 200 outputs blind: for each image it saw the ground truth and two unlabeled outputs "
  "(A/B order randomised per image, key hidden), scored each 1–5 for *usefulness when pasted* "
  "(5 = paste-ready, 1 = unusable; one wrong character in a URL/number/code token is a meaningful error), "
  "tagged error types, and picked a preference.\n")
pt, pp = J["mean_usability_score"]["tesseract"], J["mean_usability_score"]["ppocr"]
pr = J["pairwise_preference"]
w(f"| | Tesseract | **omarchy-ppocr** |")
w("|---|---:|---:|")
w(f"| Mean usability score (1–5) | {pt:.2f} | **{pp:.2f}** |")
for s in ["5", "4", "3", "2", "1"]:
    w(f"| Scored {s} | {J['score_distribution']['tesseract'].get(s, 0)} | {J['score_distribution']['ppocr'].get(s, 0)} |")
w(f"| Preferred (head-to-head) | {pr.get('tesseract', 0)} | **{pr.get('ppocr', 0)}** |")
w(f"| Tie | {pr.get('tie', 0)} | |")
w("")
w("Judge's error tags (count of images):\n")
tags = sorted(set(J["error_tags"]["tesseract"]) | set(J["error_tags"]["ppocr"]),
              key=lambda t: -(J["error_tags"]["tesseract"].get(t, 0) + J["error_tags"]["ppocr"].get(t, 0)))
w("| Error type | Tesseract | omarchy-ppocr |")
w("|---|---:|---:|")
for t in tags:
    w(f"| {t} | {J['error_tags']['tesseract'].get(t, 0)} | {J['error_tags']['ppocr'].get(t, 0)} |")
w("")
w("Mean judge score by category:\n")
w("| Category | Tesseract | omarchy-ppocr |")
w("|---|---:|---:|")
for c, d in J["mean_score_by_category"].items():
    w(f"| {c} | {d['tesseract']:.2f} | {d['ppocr']:.2f} |")
w("")

w("## Post-processing fix (reported separately)\n")
w("Inspecting the golden-set errors showed the multilingual model sometimes emits full-width CJK punctuation "
  "(`：`, `（`) in Latin text. The released script folds these to ASCII when a line has no CJK. "
  "Because this was found on the test set, the numbers above are the *unfixed* run; with the fix:\n")
w(f"| | before | after |")
w("|---|---:|---:|")
for label, k, f in spec[:8]:
    w(f"| {label} | {f(P[k])} | {f(PF[k])} |")
w("")
(B / "RESULTS.md").write_text("\n".join(out) + "\n")
print("\n".join(out))
