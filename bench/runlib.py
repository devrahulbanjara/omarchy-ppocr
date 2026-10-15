"""Run an OCR pipeline as a subprocess, feeding a PNG on stdin like the real script does.

Returns text, wall-clock seconds, the process's own peak RSS in MB (via wait4), and exit code.
"""

import os
import subprocess
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VENV_PY = Path(os.environ.get("OMARCHY_PPOCR_HOME", "~/.local/share/omarchy-ppocr")).expanduser() / "venv/bin/python"

PIPELINES = {
    # Exact command from /usr/bin/omarchy-capture-text (Omarchy default)
    "tesseract": ["tesseract", "stdin", "stdout", "--oem", "1", "--psm", "6", "-l", "eng",
                  "--dpi", "300", "-c", "preserve_interword_spaces=1"],
    # New pipeline: PP-OCRv6 via RapidOCR/ONNX Runtime
    "ppocr": [str(VENV_PY), str(REPO / "lib" / "extract.py")],
}


def run(cmd, png_bytes, env=None):
    t0 = time.perf_counter()
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                         env={**os.environ, **(env or {})})
    p.stdin.write(png_bytes)
    p.stdin.close()
    out = p.stdout.read()
    _, status, ru = os.wait4(p.pid, 0)
    dt = time.perf_counter() - t0
    return out.decode("utf-8", "replace"), dt, ru.ru_maxrss / 1024, os.waitstatus_to_exitcode(status)
