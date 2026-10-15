"""OCR comparison metrics.

All metrics compare a prediction against the ground truth text for one image.
Normalisation is deliberately light: Unicode NFC, trailing whitespace stripped,
blank lines dropped (Tesseract emits blank lines between paragraphs; that is not
an error a user would care about). Everything else - case, punctuation, quotes,
digits - counts, because a wrong character in a pasted command or URL matters.
"""

import re
import unicodedata
from collections import Counter

from rapidfuzz.distance import Levenshtein

QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "—": "-", "–": "-"})


def lines(text, keep_inner_spaces=False):
    out = []
    for ln in unicodedata.normalize("NFC", text).splitlines():
        ln = ln.rstrip()
        if not keep_inner_spaces:
            ln = " ".join(ln.split())
        if ln.strip():
            out.append(ln)
    return out


def tokens(text):
    return " ".join(lines(text)).split()


def cer(pred, gt):
    """Character error rate on whitespace-collapsed text (line breaks count as one char)."""
    p, g = "\n".join(lines(pred)), "\n".join(lines(gt))
    return Levenshtein.distance(p, g), len(g)


def cer_layout(pred, gt):
    """CER keeping indentation and inner spacing: how well code/tables survive a paste."""
    p, g = "\n".join(lines(pred, True)), "\n".join(lines(gt, True))
    return Levenshtein.distance(p, g), len(g)


def cer_lenient(pred, gt):
    """CER ignoring all whitespace and typographic quote/dash substitutions."""
    f = lambda t: re.sub(r"\s+", "", unicodedata.normalize("NFC", t).translate(QUOTES))
    p, g = f(pred), f(gt)
    return Levenshtein.distance(p, g), len(g)


def wer(pred, gt):
    p, g = tokens(pred), tokens(gt)
    return Levenshtein.distance(p, g), len(g)


def bag_f1(pred, gt):
    """Order-independent word F1: did the right words come out, regardless of layout?"""
    p, g = Counter(tokens(pred)), Counter(tokens(gt))
    tp = sum((p & g).values())
    if not p or not g:
        return 0.0
    prec, rec = tp / sum(p.values()), tp / sum(g.values())
    return 0.0 if tp == 0 else 2 * prec * rec / (prec + rec)


CRITICAL = re.compile(r"[0-9@/:#$%._\-=]")


def critical_tokens(pred, gt):
    """Exact-match recall of 'copy-paste critical' tokens: anything with digits or
    symbols (URLs, emails, hashes, IPs, prices, versions, paths)."""
    g = Counter(t for t in tokens(gt) if CRITICAL.search(t))
    p = Counter(tokens(pred))
    return sum((p & g).values()), sum(g.values())


def line_exact(pred, gt):
    """Fraction of ground-truth lines reproduced exactly (whitespace-collapsed)."""
    g = lines(gt)
    p = Counter(lines(pred))
    hit = 0
    for ln in g:
        if p[ln] > 0:
            p[ln] -= 1
            hit += 1
    return hit, len(g)


def score(pred, gt):
    e, n = cer(pred, gt)
    el, nl = cer_layout(pred, gt)
    elen, nlen = cer_lenient(pred, gt)
    we, wn = wer(pred, gt)
    ct, cn = critical_tokens(pred, gt)
    lh, ln = line_exact(pred, gt)
    return {
        "cer_edits": e, "cer_chars": n,
        "layout_edits": el, "layout_chars": nl,
        "lenient_edits": elen, "lenient_chars": nlen,
        "wer_edits": we, "wer_words": wn,
        "bag_f1": bag_f1(pred, gt),
        "crit_hit": ct, "crit_total": cn,
        "line_hit": lh, "line_total": ln,
        "perfect": e == 0,
    }
