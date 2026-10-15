# Benchmark results

Hardware: **13th Gen Intel(R) Core(TM) i5-1335U**, no GPU, ONNX Runtime CPU. 100 golden images, every image OCR'd by launching the pipeline fresh (exactly what happens on a keypress), pipelines interleaved per image.

- **Omarchy default**: `tesseract 5.5.3`, `--oem 1 --psm 6 -l eng --dpi 300 -c preserve_interword_spaces=1` (the exact command in `omarchy-capture-text`)
- **omarchy-ppocr**: PP-OCRv6 *small* det + rec via RapidOCR / ONNX Runtime, detection resize `min 320`; headline accuracy is the run *without* the punctuation fix (`OCR_ASCII_PUNCT=0`), see the end of this report
- *PP-OCRv6 tiny* is shown for reference (lower-end machines); it was not part of the blind judging.

## Accuracy and cost

| Metric | Omarchy default (Tesseract) | omarchy-ppocr | PP-OCRv6 tiny |
|---|---:|---:|---:|
| Character error rate (CER) ↓ | 2.8% | **0.4%** | 0.7% |
| CER keeping indentation/spacing ↓ | 6.8% | **2.6%** | 3.2% |
| CER ignoring whitespace & typographic quotes ↓ | 2.9% | **0.3%** | 0.4% |
| Word error rate (WER) ↓ | 10.3% | **2.0%** | 5.0% |
| Bag-of-words F1 (order-free) ↑ | 0.865 | **0.968** | 0.931 |
| Critical tokens exact (URLs, hashes, numbers, paths) ↑ | 85.2% | **95.0%** | 86.7% |
| Lines reproduced exactly ↑ | 67.1% | **90.8%** | 79.8% |
| Images transcribed perfectly ↑ | 39.0% | **70.0%** | 51.0% |
| Empty output / failures ↓ | 2 | **0** | 0 |
| Latency mean ↓ | **0.29 s** | 1.34 s | 0.70 s |
| Latency p50 ↓ | **0.28 s** | 1.34 s | 0.69 s |
| Latency p95 ↓ | **0.51 s** | 1.68 s | 0.80 s |
| Peak RAM (mean) ↓ | **81 MB** | 293 MB | 179 MB |

- CER drop is significant: paired bootstrap (10,000 resamples) 95% CI for the CER reduction is **1.4 to 3.5 points**; per image, omarchy-ppocr is better on **54**, worse on **11**, tied on 35.
- Excluding the accented-text category (Omarchy ships only the English Tesseract model): CER 2.4% → **0.4%**.
- Model files on disk: ~31 MB (small det 9.5 MB + rec 21 MB). Tesseract `eng` data: ~23 MB.

## Release-configuration latency (cold vs warm server)

| | Tesseract | omarchy-ppocr cold | omarchy-ppocr warm |
|---|---:|---:|---:|
| Mean | 0.39 s | 1.41 s | 0.69 s |
| p50 | 0.38 s | 1.41 s | 0.70 s |
| p95 | 0.65 s | 1.78 s | 1.02 s |
| Max | 0.77 s | 2.34 s | 1.17 s |
| CER | 2.8% | 0.4% | 0.4% |

## Character error rate by category

| Category | n | Tesseract | omarchy-ppocr | tiny |
|---|---:|---:|---:|---:|
| accented | 8 | 6.9% | **0.5%** | 0.6% |
| code | 10 | 2.8% | **0.7%** | 2.0% |
| identifiers | 10 | 2.9% | **0.5%** | 0.5% |
| low_contrast | 8 | 0.2% | **0.0%** | 0.1% |
| mixed_styles | 12 | 2.5% | **0.0%** | 0.1% |
| numbers | 8 | **0.3%** | 0.9% | 2.6% |
| prose | 8 | 0.1% | **0.0%** | 0.0% |
| small_text | 8 | 2.9% | **0.0%** | 0.2% |
| table | 8 | 1.5% | **0.4%** | 0.4% |
| terminal | 10 | **2.3%** | 2.3% | 2.1% |
| ui | 10 | 22.7% | **0.0%** | 0.9% |

## By display scale

| Scale | n | Tesseract CER | **omarchy-ppocr CER** |
|---|---:|---:|---:|
| 1x | 30 | 5.1% | **0.4%** |
| 1.25x | 45 | 1.6% | **0.4%** |
| 1.5x | 12 | 3.3% | **0.2%** |
| 2x | 13 | 1.6% | **0.9%** |

## LLM-as-judge (blind A/B)

Claude judged all 200 outputs blind: for each image it saw the ground truth and two unlabeled outputs (A/B order randomised per image, key hidden), scored each 1–5 for *usefulness when pasted* (5 = paste-ready, 1 = unusable; one wrong character in a URL/number/code token is a meaningful error), tagged error types, and picked a preference.

| | Tesseract | **omarchy-ppocr** |
|---|---:|---:|
| Mean usability score (1–5) | 3.49 | **4.55** |
| Scored 5 | 36 | 70 |
| Scored 4 | 13 | 16 |
| Scored 3 | 18 | 13 |
| Scored 2 | 30 | 1 |
| Scored 1 | 3 | 0 |
| Preferred (head-to-head) | 8 | **61** |
| Tie | 31 | |

Judge's error tags (count of images):

| Error type | Tesseract | omarchy-ppocr |
|---|---:|---:|
| char_substitution | 45 | 10 |
| missing_text | 12 | 8 |
| extra_text | 13 | 0 |
| lost_indentation | 12 | 1 |
| extra_space | 11 | 1 |
| wrong_punctuation | 7 | 5 |
| diacritics | 9 | 1 |
| missing_space | 2 | 6 |
| case | 2 | 2 |
| empty_output | 2 | 0 |

Mean judge score by category:

| Category | Tesseract | omarchy-ppocr |
|---|---:|---:|
| accented | 2.00 | 4.38 |
| code | 2.10 | 4.10 |
| identifiers | 2.40 | 4.20 |
| low_contrast | 4.75 | 5.00 |
| mixed_styles | 4.25 | 4.92 |
| numbers | 4.38 | 4.38 |
| prose | 4.75 | 5.00 |
| small_text | 3.62 | 5.00 |
| table | 3.88 | 4.50 |
| terminal | 3.00 | 3.70 |
| ui | 3.60 | 5.00 |

## Post-processing fix (reported separately)

Inspecting the golden-set errors showed the multilingual model sometimes emits full-width CJK punctuation (`：`, `（`) in Latin text. The released script folds these to ASCII when a line has no CJK. Because this was found on the test set, the numbers above are the *unfixed* run; with the fix:

| | before | after |
|---|---:|---:|
| Character error rate (CER) ↓ | 0.4% | 0.4% |
| CER keeping indentation/spacing ↓ | 2.6% | 2.6% |
| CER ignoring whitespace & typographic quotes ↓ | 0.3% | 0.3% |
| Word error rate (WER) ↓ | 2.0% | 2.0% |
| Bag-of-words F1 (order-free) ↑ | 0.968 | 0.969 |
| Critical tokens exact (URLs, hashes, numbers, paths) ↑ | 95.0% | 95.1% |
| Lines reproduced exactly ↑ | 90.8% | 90.8% |
| Images transcribed perfectly ↑ | 70.0% | 70.0% |

