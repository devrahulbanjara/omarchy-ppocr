# LLM judge prompt (used verbatim, one judge per batch of 25 items)

You are a blind judge evaluating OCR outputs. Read judge/batch_N.md. It contains 25 items. Each item has an image path, the GROUND TRUTH text (exactly what was rendered on screen), and two anonymous OCR outputs, A and B. Do NOT open any file other than batch_N.md and the item images (never open KEY_do_not_show_judge.json or anything in results/). You may view an image when it helps judge layout or ambiguity, e.g. for tables, terminals, code, or UI layouts; it is optional for simple prose.

Context: a user selects a screen region, the OCR text is copied to the clipboard, and they paste it somewhere (a terminal, an editor, a chat). Judge how USEFUL each output is for that, compared with the ground truth.

For each item, score A and B independently, 1-5:
5 = paste-ready: identical in content (ignore only blank lines and differences in the amount of whitespace between columns)
4 = 1-2 trivial errors that a human would fix in seconds (e.g. one missing space, a single typographic quote)
3 = a few errors or one meaningful one (a wrong digit/char in a token that matters, a dropped symbol), still largely usable
2 = many errors, or missing/garbled lines; needs substantial fixing
1 = unusable or empty

Important rules: a single wrong character in a URL, hash, number, command, or code token is meaningful (not trivial) because the pasted text would be wrong. Missing indentation in code matters. Reading-order scrambles matter. Extra blank lines do not matter.

Error tags (use any that apply, empty list if none): "char_substitution", "missing_text", "extra_text", "missing_space", "extra_space", "wrong_punctuation", "diacritics", "case", "reading_order", "lost_indentation", "merged_lines", "split_lines", "empty_output".

preferred: "A", "B", or "tie" (tie only if equally useful).

Write your verdicts as JSON Lines to judge/verdicts_N.jsonl with exactly these keys:
{"id": "<item id>", "score_A": int, "score_B": int, "errors_A": [...], "errors_B": [...], "preferred": "A"|"B"|"tie", "reason": "<one short sentence citing the decisive difference>"}

Be careful and consistent; check every line of every item character by character. All 25 items must be present.

Model used for the published results: Claude Opus 5.5 (claude-opus-5-5), four independent judge instances.

Re-judging note: the identifier samples originally contained fake keys with an `sk_test_` prefix, which GitHub push protection flags as Stripe test keys. The prefix was changed to `demo-` (all random characters unchanged, so only those 10 images changed), the benchmark was re-run in full, and only those 10 items were re-judged by a fresh, independent judge instance with this same prompt (`judge/batch_rejudge.md`). The other 90 packets were byte-identical, so their verdicts were kept. Verdicts are merged in `judge/verdicts_all.jsonl`.
