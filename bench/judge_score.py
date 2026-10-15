"""Unblind LLM-judge verdicts and aggregate them.

Usage: .venv/bin/python judge_score.py <judge_dir>
Reads judge_dir/verdicts_*.jsonl and judge_dir/KEY_do_not_show_judge.json.
"""

import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

d = Path(sys.argv[1])
key = json.loads((d / "KEY_do_not_show_judge.json").read_text())
verdicts = {}
for f in sorted(d.glob("verdicts_*.jsonl")):
    for line in f.read_text().splitlines():
        if line.strip():
            v = json.loads(line)
            verdicts[v["id"]] = v

pipes = sorted({p for k in key.values() for p in k.values()})
scores = defaultdict(list)
errors = defaultdict(Counter)
wins = Counter()
by_cat = defaultdict(lambda: defaultdict(list))
for sid, v in verdicts.items():
    k = key[sid]
    cat = sid.split("_", 1)[1]
    for lab in "AB":
        p = k[lab]
        scores[p].append(v[f"score_{lab}"])
        by_cat[cat][p].append(v[f"score_{lab}"])
        errors[p].update(v.get(f"errors_{lab}", []))
    pref = v["preferred"]
    wins[k[pref] if pref in "AB" else "tie"] += 1

summary = {
    "judged": len(verdicts),
    "mean_usability_score": {p: statistics.mean(scores[p]) for p in pipes},
    "score_distribution": {p: dict(sorted(Counter(scores[p]).items())) for p in pipes},
    "pairwise_preference": dict(wins),
    "error_tags": {p: dict(errors[p].most_common()) for p in pipes},
    "mean_score_by_category": {c: {p: round(statistics.mean(s), 2) for p, s in ps.items()} for c, ps in sorted(by_cat.items())},
    "missing": sorted(set(key) - set(verdicts)),
}
(d / "judge_summary.json").write_text(json.dumps(summary, indent=1))

unblinded = []
for sid, v in sorted(verdicts.items()):
    k = key[sid]
    unblinded.append({"id": sid, "preferred": k.get(v["preferred"], "tie"),
                      **{k[l]: {"score": v[f"score_{l}"], "errors": v.get(f"errors_{l}", [])} for l in "AB"},
                      "reason": v.get("reason", "")})
(d / "judge_unblinded.json").write_text(json.dumps(unblinded, indent=1))
print(json.dumps(summary, indent=1))
