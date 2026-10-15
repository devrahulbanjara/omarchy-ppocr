"""Build blinded A/B packets for LLM-as-judge evaluation.

For each image the judge sees the ground truth and two outputs labelled A and B.
Which pipeline is A is randomised per image (seeded); the key is written to a
separate file the judge never reads.

Usage: .venv/bin/python judge_prep.py <dataset_dir> <results_dir> <pipeA> <pipeB> <out_dir> <n_batches>
"""

import json
import random
import sys
from pathlib import Path

data, res, p1, p2, out, nb = sys.argv[1:7]
data, res, out, nb = Path(data), Path(res), Path(out), int(nb)
out.mkdir(parents=True, exist_ok=True)
rng = random.Random(2024)

manifest = json.loads((data / "manifest.json").read_text())
key = {}
batches = [[] for _ in range(nb)]
for i, m in enumerate(manifest):
    sid = m["id"]
    a, b = (p1, p2) if rng.random() < 0.5 else (p2, p1)
    key[sid] = {"A": a, "B": b}
    batches[i % nb].append({
        "id": sid,
        "image": str((data / f"{sid}.png").resolve()),
        "ground_truth": (data / f"{sid}.gt.txt").read_text(),
        "A": (res / a / f"{sid}.txt").read_text(),
        "B": (res / b / f"{sid}.txt").read_text(),
    })

(out / "KEY_do_not_show_judge.json").write_text(json.dumps(key, indent=1))
for i, batch in enumerate(batches):
    with open(out / f"batch_{i}.md", "w") as f:
        for item in batch:
            f.write(f"\n\n========== ITEM {item['id']} ==========\nimage: {item['image']}\n")
            f.write("----- GROUND TRUTH -----\n" + item["ground_truth"].rstrip() + "\n")
            f.write("----- OUTPUT A -----\n" + item["A"].rstrip() + "\n")
            f.write("----- OUTPUT B -----\n" + item["B"].rstrip() + "\n")
print("wrote", nb, "batches to", out)
