#!/usr/bin/env python3
"""Read an image (path or stdin) and print the recognized text in reading order.

Uses PaddleOCR PP-OCRv6 models through RapidOCR + ONNX Runtime (CPU).

  extract.py [image|-]   OCR an image (stdin when omitted or "-")
  extract.py --serve     keep the model loaded and answer over a unix socket
  extract.py --status    say whether the warm server is running
  extract.py --stop      stop the warm server

The first OCR call runs in-process (cold, ~1.4 s) and then starts the warm server
in the background, so later captures skip Python start-up and model loading. The
server exits on its own after OMARCHY_PPOCR_IDLE seconds without a request
(default 600; 0 = never). Set OMARCHY_PPOCR_DAEMON=0 to never use or start it.
Each distinct set of OCR_* settings gets its own server, so a request is never
answered by a server running a different configuration.
"""

import hashlib
import json
import os
import re
import socket
import struct
import subprocess
import sys
import unicodedata

MODEL_SIZE = os.environ.get("OCR_MODEL_SIZE", "small")
TEXT_SCORE = float(os.environ.get("OCR_TEXT_SCORE", "0.5"))
BOX_THRESH = float(os.environ.get("OCR_BOX_THRESH", "0.5"))
DET_THRESH = float(os.environ.get("OCR_DET_THRESH", "0.3"))
UNCLIP = float(os.environ.get("OCR_UNCLIP", "1.6"))
# Detection resize: RapidOCR's default ("min", 736) upscales the *short* side to 736px, which
# turns a wide screenshot strip into a huge image and makes detection slow.
DET_LIMIT_TYPE = os.environ.get("OCR_DET_LIMIT_TYPE", "min")
DET_LIMIT_SIDE = int(os.environ.get("OCR_DET_LIMIT_SIDE", "320"))
# Using every logical core is slower on hybrid (P+E core) laptop CPUs than a few threads.
THREADS = int(os.environ.get("OCR_THREADS", "4"))
# Fold full-width CJK punctuation in non-CJK text (see ascii_punct); 0 disables, for benchmarking.
ASCII_PUNCT = os.environ.get("OCR_ASCII_PUNCT", "1") != "0"

IDLE_SECONDS = float(os.environ.get("OMARCHY_PPOCR_IDLE", "600"))
USE_DAEMON = os.environ.get("OMARCHY_PPOCR_DAEMON", "1") != "0"
_config = sorted((k, v) for k, v in os.environ.items() if k.startswith("OCR_"))
_suffix = "-" + hashlib.sha1(repr(_config).encode()).hexdigest()[:8] if _config else ""
SOCKET_PATH = os.path.join(os.environ.get("XDG_RUNTIME_DIR") or f"/tmp/omarchy-ppocr-{os.getuid()}",
                           f"omarchy-ppocr{_suffix}.sock")


def build_engine():
    # Imported lazily: rapidocr/onnxruntime take ~0.4 s to import, which the
    # warm-server client path must not pay.
    from rapidocr import LangDet, LangRec, ModelType, OCRVersion, RapidOCR

    det_size = ModelType(os.environ.get("OCR_DET_SIZE", MODEL_SIZE))
    rec_size = ModelType(os.environ.get("OCR_REC_SIZE", MODEL_SIZE))
    return RapidOCR(
        params={
            "Global.log_level": "error",
            "Global.use_cls": False,  # screenshots are upright; skip rotation model
            "Global.text_score": TEXT_SCORE,
            "Det.ocr_version": OCRVersion.PPOCRV6,
            "Det.model_type": det_size,
            "Det.box_thresh": BOX_THRESH,
            "Det.thresh": DET_THRESH,
            "Det.unclip_ratio": UNCLIP,
            "Det.lang_type": LangDet.EN,
            "Det.limit_type": DET_LIMIT_TYPE,
            "Det.limit_side_len": DET_LIMIT_SIDE,
            "Rec.ocr_version": OCRVersion.PPOCRV6,
            "Rec.model_type": rec_size,
            "Rec.lang_type": LangRec.EN,
            "EngineConfig.onnxruntime.intra_op_num_threads": THREADS,
        }
    )


CJK = re.compile(r"[぀-ヿ㐀-鿿가-힯]")
FULLWIDTH = re.compile(r"[！-～　]")


def ascii_punct(text):
    """The multilingual model sometimes emits full-width CJK punctuation (e.g. '：', '（')
    in Latin text. Fold those to ASCII unless the text actually contains CJK."""
    if not ASCII_PUNCT or CJK.search(text):
        return text
    return FULLWIDTH.sub(lambda m: unicodedata.normalize("NFKC", m.group()), text)


def to_lines(boxes, txts):
    """Group detected boxes into text lines, keeping indentation and column gaps."""
    items = []
    for box, txt in zip(boxes, txts):
        if not txt.strip():
            continue
        xs = [p[0] for p in box]
        ys = [p[1] for p in box]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        items.append({"x0": x0, "x1": x1, "y0": y0, "y1": y1, "cy": (y0 + y1) / 2, "h": y1 - y0, "t": ascii_punct(txt)})
    if not items:
        return ""

    items.sort(key=lambda i: i["cy"])
    lines = []
    for it in items:
        if lines:
            line = lines[-1]
            cy = sum(i["cy"] for i in line) / len(line)
            h = sum(i["h"] for i in line) / len(line)
            if abs(it["cy"] - cy) < 0.5 * min(h, it["h"]):
                line.append(it)
                continue
        lines.append([it])

    # Average character width, used to turn pixel gaps into spaces.
    widths = [(i["x1"] - i["x0"]) / len(i["t"]) for i in items if len(i["t"]) > 1]
    cw = sorted(widths)[len(widths) // 2] if widths else 10
    left = min(i["x0"] for i in items)
    heights = sorted(i["h"] for i in items)
    line_h = heights[len(heights) // 2]

    out = []
    prev_bottom = None
    for line in lines:
        line.sort(key=lambda i: i["x0"])
        top = min(i["y0"] for i in line)
        if prev_bottom is not None and top - prev_bottom > 0.9 * line_h:
            out.append("")  # paragraph break
        prev_bottom = max(i["y1"] for i in line)

        indent = round((line[0]["x0"] - left) / cw)
        text = " " * indent + line[0]["t"]
        for prev, cur in zip(line, line[1:]):
            gap = round((cur["x0"] - prev["x1"]) / cw)
            text += " " * max(1, gap if gap >= 3 else 1) + cur["t"]
        out.append(text.rstrip())
    return "\n".join(out)


def ocr(engine, data):
    result = engine(data)
    return to_lines(result.boxes, result.txts) if result.txts else ""


# ---------- warm server ----------
# Wire format, both directions: 1-byte op + 4-byte big-endian length + payload.
# Ops: b"O" OCR (payload = image bytes, reply = JSON {"text": ...}), b"S" status, b"Q" quit.


def send(sock, op, payload=b""):
    sock.sendall(op + struct.pack(">I", len(payload)) + payload)


def recv(sock):
    head = recv_exact(sock, 5)
    op, n = head[:1], struct.unpack(">I", head[1:])[0]
    return op, recv_exact(sock, n)


def recv_exact(sock, n):
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(min(1 << 20, n - len(buf)))
        if not chunk:
            raise ConnectionError("peer closed")
        buf += chunk
    return bytes(buf)


def serve():
    os.makedirs(os.path.dirname(SOCKET_PATH), mode=0o700, exist_ok=True)
    srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        srv.bind(SOCKET_PATH)
    except OSError:
        if request(b"S") is not None:
            return 0  # another server is already running
        os.unlink(SOCKET_PATH)  # stale socket from a crashed server
        srv.bind(SOCKET_PATH)
    os.chmod(SOCKET_PATH, 0o600)
    srv.listen(4)
    srv.settimeout(IDLE_SECONDS or None)

    engine = build_engine()
    try:
        while True:
            try:
                conn, _ = srv.accept()
            except socket.timeout:
                return 0
            with conn:
                conn.settimeout(30)
                try:
                    op, payload = recv(conn)
                    if op == b"O":
                        send(conn, b"O", json.dumps({"text": ocr(engine, payload)}).encode())
                    elif op == b"S":
                        send(conn, b"S", json.dumps({"pid": os.getpid(), "idle_timeout": IDLE_SECONDS,
                                                     "model": MODEL_SIZE, "threads": THREADS}).encode())
                    elif op == b"Q":
                        send(conn, b"Q")
                        return 0
                except Exception as e:  # a bad client must never take the server down
                    try:
                        send(conn, b"E", str(e).encode())
                    except OSError:
                        pass
    finally:
        try:
            os.unlink(SOCKET_PATH)
        except FileNotFoundError:
            pass


def request(op, payload=b""):
    """Send one request to the warm server; None when no server is listening."""
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.settimeout(60)
            s.connect(SOCKET_PATH)
            send(s, op, payload)
            rop, body = recv(s)
            if rop == b"E":
                return None
            return json.loads(body) if body else {}
    except (OSError, ConnectionError, ValueError):
        return None


def start_server():
    subprocess.Popen([sys.executable, os.path.abspath(__file__), "--serve"], start_new_session=True,
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "-"
    if arg == "--serve":
        return serve()
    if arg == "--status":
        st = request(b"S")
        print(f"running (pid {st['pid']}, model {st['model']}, idle timeout {st['idle_timeout']:.0f}s)" if st else "not running")
        return 0 if st else 1
    if arg == "--stop":
        return 0 if request(b"Q") is not None else 1

    data = sys.stdin.buffer.read() if arg == "-" else open(arg, "rb").read()
    if not data:
        return 1

    reply = request(b"O", data) if USE_DAEMON else None
    if reply is not None:
        text = reply["text"]
    else:
        text = ocr(build_engine(), data)
        if USE_DAEMON:
            start_server()
    if not text:
        return 1
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
