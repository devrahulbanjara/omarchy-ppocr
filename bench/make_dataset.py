"""Generate a golden OCR dataset of screen-like images with exact ground truth.

Each sample is an HTML page rendered by headless Chromium (real fonts, real
anti-aliasing, real HiDPI scaling), then cropped to the text with a random
margin, like a slurp selection. Ground truth is the exact text that was
rendered, line by line.

Usage: .venv/bin/python make_dataset.py [out_dir] [seed] [per_category_scale]
  golden: make_dataset.py dataset            (seed 1337, 100 images)
  dev:    make_dataset.py dev 7 0.4          (separate tuning set, never scored)
"""

import html
import json
import random
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "dataset")
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 1337  # golden set uses 1337; dev/tuning set uses another seed
PER_CATEGORY_SCALE = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
rng = random.Random(SEED)

MONO = ["JetBrainsMono Nerd Font", "DejaVu Sans Mono", "Liberation Mono", "Adwaita Mono", "iA Writer Mono S"]
SANS = ["Noto Sans", "DejaVu Sans", "Liberation Sans", "Adwaita Sans", "Nimbus Sans"]
SERIF = ["Liberation Serif", "DejaVu Serif", "Nimbus Roman", "C059"]
SCALES = [1, 1, 1.25, 1.25, 1.25, 1.5, 2]

# Omarchy-style themes: (background, foreground, muted, accent)
DARK = [
    ("#1a1b26", "#c0caf5", "#565f89", "#7aa2f7"),  # tokyo night
    ("#1e1e2e", "#cdd6f4", "#6c7086", "#89b4fa"),  # catppuccin mocha
    ("#282828", "#ebdbb2", "#928374", "#fabd2f"),  # gruvbox
    ("#2e3440", "#d8dee9", "#4c566a", "#88c0d0"),  # nord
    ("#2d353b", "#d3c6aa", "#859289", "#a7c080"),  # everforest
    ("#0d0d0d", "#e0e0e0", "#7a7a7a", "#d35f5f"),  # matte black
]
LIGHT = [
    ("#ffffff", "#1f2328", "#656d76", "#0969da"),
    ("#eff1f5", "#4c4f69", "#8c8fa1", "#1e66f5"),  # catppuccin latte
    ("#fdf6e3", "#586e75", "#93a1a1", "#268bd2"),  # solarized light
    ("#f6f8fa", "#24292f", "#57606a", "#cf222e"),
]

PROSE = [
    "The quick brown fox jumps over the lazy dog near the riverbank.",
    "Wayland compositors handle input, output and window management in one process.",
    "Backups are only useful if you have actually tried restoring from them.",
    "She opened the terminal, typed a single command, and the build finally passed.",
    "Most performance problems come from doing work that never needed to happen.",
    "The meeting moved to Thursday at 3:30 PM because the projector was broken.",
    "Keep your dotfiles in version control so a new machine takes minutes, not days.",
    "Optical character recognition turns pixels back into text you can edit.",
    "A tiling window manager arranges windows so that nothing ever overlaps.",
    "He paid $42.50 for the cable, which was twice what it cost last year.",
    "Good error messages explain what happened, why, and what to do next.",
    "The library closes at 9 PM on weekdays and at noon on Saturdays.",
    "Small, frequent commits make it far easier to find the change that broke things.",
    "Rain is expected through the weekend, with temperatures around 14 degrees.",
    "Every keyboard shortcut you learn saves a few seconds a hundred times a day.",
    "The report covers Q3 revenue, hiring plans, and the new office in Berlin.",
    "If the fan is loud, check which process is using the most CPU first.",
    "Latency matters more than throughput when a person is waiting for the result.",
    "The archive contains 1,284 photos taken between 2019 and 2024.",
    "Write the test first, watch it fail, then make it pass with the simplest code.",
    "Unplug the router, wait thirty seconds, and plug it back in again.",
    "Her flight, LH 2047, departs from gate B12 at 06:15 tomorrow morning.",
    "Readable code is written for the next person, who is usually you.",
    "The museum's new wing displays maps drawn between 1650 and 1720.",
    "Do not store passwords in plain text; use a password manager instead.",
    "Screen readers depend on applications exposing correct accessibility labels.",
    "The recipe calls for 250 g of flour, 2 eggs, and a pinch of salt.",
    "Version 2.4.1 fixes the crash that occurred when resuming from suspend.",
    "Our support team replies within 24 hours, including weekends and holidays.",
    "Compression trades CPU time for smaller files and faster transfers.",
]

ACCENTED = [
    "Le café de la gare est fermé le dimanche après-midi.",
    "Die Größe der Datei überschreitet das zulässige Maximum.",
    "El niño comió una manzana mientras leía el periódico.",
    "Ça coûte 12,50 € pour deux crêpes et un thé glacé.",
    "Über den Wolken muss die Freiheit wohl grenzenlos sein.",
    "La reunión será el miércoles a las diez de la mañana.",
    "Où est la bibliothèque la plus proche, s'il vous plaît ?",
    "Bitte schließen Sie die Tür, bevor Sie gehen.",
    "São Paulo é a maior cidade do Brasil em população.",
    "Æble, øl og smørrebrød er typisk dansk mad.",
    "Señor Núñez llegó tarde a la estación de tren.",
    "Je préfère le thé à la menthe après le dîner.",
]

CODE = [
    """def parse_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "version" not in data:
        raise ValueError(f"missing version in {path}")
    return {k: v for k, v in data.items() if v is not None}""",
    """const fetchUser = async (id) => {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
};""",
    """fn main() {
    let nums: Vec<i32> = (1..=10).collect();
    let sum: i32 = nums.iter().filter(|&x| x % 2 == 0).sum();
    println!("sum of evens = {}", sum);
}""",
    """#!/bin/bash
set -euo pipefail
for f in ~/Pictures/*.png; do
  [[ -f "$f" ]] || continue
  magick "$f" -resize 50% "${f%.png}-small.png"
done""",
    """SELECT u.id, u.email, COUNT(o.id) AS orders
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id, u.email
HAVING COUNT(o.id) > 3;""",
    """package main

import "fmt"

func main() {
    m := map[string]int{"a": 1, "b": 2}
    for k, v := range m {
        fmt.Printf("%s=%d\\n", k, v)
    }
}""",
    """class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop() if self._items else None""",
    """{
  "name": "omarchy-ocr",
  "version": "0.3.1",
  "scripts": { "build": "tsc -p .", "test": "vitest run" },
  "dependencies": { "zod": "^3.23.8" }
}""",
    """o.bind("SUPER + CTRL + PRINT", "Extract text (OCR)", "omarchy-capture-text")
hl.unbind("SUPER + SHIFT + F")
o.window("org.gnome.Calculator", { tag = "+floating-window" })""",
    """for (int i = 0; i < n; ++i) {
    if (arr[i] < 0 && i != last) {
        arr[i] = -arr[i] * 2;
    }
}
printf("%d items, max=%.2f\\n", n, max);""",
    """[Unit]
Description=Sync notes every 15 minutes
After=network-online.target

[Service]
ExecStart=/usr/bin/rsync -az ~/notes/ backup:/srv/notes/""",
    """import { useState } from "react";

export function Counter() {
  const [n, setN] = useState(0);
  return <button onClick={() => setN(n + 1)}>Clicked {n} times</button>;
}""",
]

TERMINAL = [
    """$ ls -la ~/Downloads
total 48
drwxr-xr-x  2 user user  4096 Oct 14 09:12 .
drwx------ 31 user user  4096 Oct 15 08:47 ..
-rw-r--r--  1 user user 18234 Oct 13 21:05 invoice-2024-10.pdf
-rw-r--r--  1 user user  9120 Oct 14 09:12 notes.md""",
    """$ git log --oneline -5
a3f9c21 Fix crash when monitor is unplugged
7b2e0d4 Add keybinding for OCR capture
e91c5aa Bump version to 3.1.2
4d8f6b3 Update README with install steps
0c7a1e9 Initial commit""",
    """$ sudo pacman -Syu
:: Synchronizing package databases...
 core is up to date
 extra is up to date
:: Starting full system upgrade...
resolving dependencies...
Packages (3) firefox-131.0-1  mesa-24.2.4-1  linux-6.11.3.arch1-1""",
    """$ df -h /
Filesystem        Size  Used Avail Use% Mounted on
/dev/nvme0n1p2    475G   75G  399G  16% /""",
    """$ ping -c 3 archlinux.org
PING archlinux.org (95.217.163.246) 56(84) bytes of data.
64 bytes from 95.217.163.246: icmp_seq=1 ttl=52 time=38.4 ms
64 bytes from 95.217.163.246: icmp_seq=2 ttl=52 time=37.9 ms
--- archlinux.org ping statistics ---
3 packets transmitted, 3 received, 0% packet loss""",
    """$ docker ps
CONTAINER ID   IMAGE           STATUS          PORTS
5f2a9c1e7b3d   postgres:16     Up 2 hours      0.0.0.0:5432->5432/tcp
b81d04e6a2f9   redis:7-alpine  Up 2 hours      6379/tcp""",
    """error[E0382]: borrow of moved value: `config`
  --> src/main.rs:14:20
   |
12 |     let handle = spawn(config);
   |                        ------ value moved here
14 |     println!("{:?}", config);
   |                      ^^^^^^ value borrowed here after move""",
    """Traceback (most recent call last):
  File "/home/user/app/main.py", line 27, in <module>
    result = compute(values)
  File "/home/user/app/main.py", line 11, in compute
    return sum(values) / len(values)
ZeroDivisionError: division by zero""",
    """$ systemctl status bluetooth
* bluetooth.service - Bluetooth service
     Loaded: loaded (/usr/lib/systemd/system/bluetooth.service; enabled)
     Active: active (running) since Tue 2024-10-15 08:41:02 CEST; 2h ago
   Main PID: 812 (bluetoothd)""",
    """$ npm install
added 214 packages, and audited 215 packages in 6s
38 packages are looking for funding
  run `npm fund` for details
found 0 vulnerabilities""",
    """$ curl -s https://api.github.com/repos/basecamp/omarchy | jq .stargazers_count
18342""",
    """$ free -h
               total        used        free      shared  buff/cache   available
Mem:            15Gi       8.3Gi       758Mi       806Mi       8.0Gi       7.0Gi
Swap:          4.0Gi       512Mi       3.5Gi""",
]

UI_SETS = [
    ["Settings", "Display", "Brightness", "Night Light", "Scale: 125%", "Apply", "Cancel"],
    ["Wi-Fi", "Connected", "HomeNetwork-5G", "Bluetooth", "Off", "Airplane mode"],
    ["File", "Edit", "View", "Selection", "Go", "Run", "Terminal", "Help"],
    ["Inbox (23)", "Starred", "Sent", "Drafts", "Spam", "Compose"],
    ["Sign in", "Email address", "Password", "Forgot password?", "Create account"],
    ["Volume", "Output Device", "Speakers (Built-in)", "Input Device", "Microphone"],
    ["Downloads", "Documents", "Pictures", "Music", "Videos", "Trash"],
    ["Battery 87%", "Power Saver", "Balanced", "Performance", "2:41 remaining"],
    ["Share", "Copy link", "Download", "Rename", "Move to folder", "Delete"],
    ["Notifications", "Do Not Disturb", "Clear all", "Updates available", "3 new"],
    ["Search settings", "Keyboard", "Layout: US", "Repeat rate", "Caps Lock as Ctrl"],
    ["Order #A-10293", "Shipped", "Arrives Fri, Oct 18", "Track package", "Return item"],
]

TABLES = [
    (["Name", "Role", "Location", "Since"],
     [["Alice Moreau", "Engineer", "Paris", "2019"], ["Bob Chen", "Designer", "Taipei", "2021"],
      ["Carlos Ruiz", "Manager", "Madrid", "2017"], ["Dana Kim", "Analyst", "Seoul", "2023"]]),
    (["Month", "Revenue", "Costs", "Profit"],
     [["Jan", "12,430", "9,210", "3,220"], ["Feb", "13,980", "9,875", "4,105"],
      ["Mar", "15,102", "10,640", "4,462"], ["Apr", "14,377", "10,021", "4,356"]]),
    (["PID", "USER", "CPU%", "MEM%", "COMMAND"],
     [["1043", "user", "12.4", "3.1", "chromium"], ["877", "root", "4.0", "0.8", "Hyprland"],
      ["2210", "user", "1.7", "1.2", "alacritty"], ["15", "root", "0.0", "0.0", "kthreadd"]]),
    (["Package", "Old", "New"],
     [["linux", "6.10.9", "6.11.3"], ["mesa", "24.2.3", "24.2.4"], ["hyprland", "0.44.0", "0.44.1"],
      ["firefox", "130.0.1", "131.0"]]),
    (["Item", "Qty", "Unit", "Total"],
     [["USB-C cable", "2", "$9.99", "$19.98"], ["Keyboard", "1", "$89.00", "$89.00"],
      ["Mouse pad", "3", "$7.50", "$22.50"], ["Webcam", "1", "$54.95", "$54.95"]]),
    (["Station", "Arrives", "Departs", "Platform"],
     [["Lyon", "08:14", "08:19", "3"], ["Dijon", "09:47", "09:52", "1A"], ["Paris", "11:30", "-", "12"]]),
    (["Key", "Action"],
     [["Super + Return", "Terminal"], ["Super + W", "Close window"], ["Super + Space", "Launcher"],
      ["Super + Ctrl + Print", "OCR"]]),
    (["Test", "Passed", "Failed", "Time"],
     [["unit", "412", "0", "3.2s"], ["integration", "88", "2", "41.7s"], ["e2e", "19", "1", "2m 14s"]]),
]

HEX = "0123456789abcdef"
WORDS = ["alpha", "bravo", "delta", "omega", "nova", "pixel", "river", "stone", "cloud", "ember", "lunar", "maple"]


def ident_lines():
    r = rng
    uuid = "-".join("".join(r.choice(HEX) for _ in range(n)) for n in (8, 4, 4, 4, 12))
    sha = "".join(r.choice(HEX) for _ in range(40))
    ip = ".".join(str(r.randint(1, 254)) for _ in range(4))
    w1, w2 = r.sample(WORDS, 2)
    lines = [
        f"https://github.com/{w1}-{w2}/{r.choice(WORDS)}-{r.randint(2, 9)}/pull/{r.randint(100, 9999)}",
        f"{w1}.{w2}{r.randint(10, 99)}@example.com",
        f"UUID: {uuid}",
        f"commit {sha}",
        f"Server: {ip}:{r.choice([22, 443, 8080, 5432, 3000])}",
        f"/home/user/.config/{w1}/{w2}_{r.randint(1, 50)}.toml",
        f"API_KEY=demo-{''.join(r.choice(HEX + 'XYZQ') for _ in range(24))}",
        f"https://www.{w2}-{w1}.org/docs/v{r.randint(1, 4)}/getting-started?ref=nav#install",
    ]
    r.shuffle(lines)
    return lines[: r.randint(4, 7)]


def number_lines():
    r = rng
    return [
        f"Invoice No. INV-{r.randint(2020, 2026)}-{r.randint(1000, 99999):05d}",
        f"Date: {r.randint(1, 28):02d}/{r.randint(1, 12):02d}/{r.randint(2020, 2026)}",
        f"Amount due: ${r.randint(10, 9999):,}.{r.randint(0, 99):02d}",
        f"Phone: +1 ({r.randint(200, 999)}) {r.randint(200, 999)}-{r.randint(1000, 9999)}",
        f"IBAN: DE{r.randint(10, 99)} {r.randint(1000, 9999)} {r.randint(1000, 9999)} {r.randint(1000, 9999)} {r.randint(1000, 9999)} {r.randint(10, 99)}",
        f"Version {r.randint(0, 9)}.{r.randint(0, 30)}.{r.randint(0, 99)} (build {r.randint(10000, 99999)})",
        f"Order total: {r.randint(1, 99)} items, {r.uniform(0.5, 30):.2f} kg",
        f"Tracking: 1Z{''.join(r.choice('0123456789ABCDEFGHJKLMNPRSTUVWXY') for _ in range(16))}",
    ][: r.randint(4, 8)]


def esc(s):
    return html.escape(s, quote=False)


def page(body, bg, fg, font, size, extra_css=""):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;background:{bg};}}
body{{color:{fg};font-family:'{font}';font-size:{size}px;line-height:1.45;padding:40px;
  font-variant-ligatures:none;font-feature-settings:"liga" 0,"calt" 0;-webkit-font-smoothing:antialiased;}}
pre{{margin:0;font-family:inherit;white-space:pre;}}
{extra_css}
</style></head><body>{body}</body></html>"""


def theme(dark=None):
    dark = rng.random() < 0.55 if dark is None else dark
    return rng.choice(DARK if dark else LIGHT)


# ---------- category builders: each returns (html, ground_truth_lines, meta) ----------

def terminal():
    bg, fg, muted, acc = theme(dark=rng.random() < 0.85)
    text = rng.choice(TERMINAL)
    font, size = rng.choice(MONO), rng.choice([13, 14, 15, 16])
    return page(f"<pre>{esc(text)}</pre>", bg, fg, font, size), text.split("\n"), {"font": font, "size": size}


def code():
    bg, fg, muted, acc = theme()
    text = rng.choice(CODE)
    font, size = rng.choice(MONO), rng.choice([13, 14, 15])
    # light syntax colouring: keywords in accent colour
    lines = []
    for ln in text.split("\n"):
        h = esc(ln)
        for kw in ["def ", "return ", "const ", "fn ", "let ", "for ", "if ", "import ", "class ", "func ", "SELECT ", "FROM ", "WHERE "]:
            h = h.replace(kw, f'<span style="color:{acc}">{kw}</span>')
        lines.append(h)
    return page("<pre>" + "\n".join(lines) + "</pre>", bg, fg, font, size), text.split("\n"), {"font": font, "size": size}


def prose():
    bg, fg, muted, acc = theme(dark=rng.random() < 0.3)
    lines = rng.sample(PROSE, rng.randint(3, 6))
    font, size = rng.choice(SANS + SERIF), rng.choice([14, 15, 16, 18])
    body = "<pre>" + "\n".join(esc(l) for l in lines) + "</pre>"
    return page(body, bg, fg, font, size), lines, {"font": font, "size": size}


def ui():
    bg, fg, muted, acc = theme()
    labels = rng.choice(UI_SETS)
    font, size = rng.choice(SANS), rng.choice([13, 14, 15])
    # vertical list, horizontal bar, or button rows
    mode = rng.choice(["list", "bar", "grid"])
    if mode == "list":
        items = "".join(
            f'<div style="padding:7px 12px;margin:4px 0;border-radius:6px;background:{acc if i == 1 else "transparent"};'
            f'color:{bg if i == 1 else fg};width:fit-content">{esc(l)}</div>' for i, l in enumerate(labels))
        gt = labels
    elif mode == "bar":
        items = '<div style="display:flex;gap:26px">' + "".join(
            f'<span style="color:{acc if i == 0 else fg}">{esc(l)}</span>' for i, l in enumerate(labels)) + "</div>"
        gt = [" ".join(labels)]
    else:
        rows = [labels[i:i + 2] for i in range(0, len(labels), 2)]
        items = "".join(
            '<div style="display:flex;gap:40px;margin:10px 0">' + "".join(
                f'<span style="border:1px solid {muted};padding:6px 14px;border-radius:5px;min-width:150px">{esc(l)}</span>'
                for l in row) + "</div>" for row in rows)
        gt = [" ".join(row) for row in rows]
    return page(items, bg, fg, font, size), gt, {"font": font, "size": size, "layout": mode}


def small_text():
    bg, fg, muted, acc = theme()
    font = rng.choice(SANS + MONO)
    size = rng.choice([9, 10, 10, 11])
    lines = rng.sample(PROSE, rng.randint(3, 5))
    return page("<pre>" + "\n".join(esc(l) for l in lines) + "</pre>", bg, fg, font, size), lines, {"font": font, "size": size}


def low_contrast():
    dark = rng.random() < 0.5
    bg, fg, muted, acc = theme(dark)
    # draw with the theme's muted colour: realistic "secondary text" / placeholder contrast
    lines = rng.sample(PROSE, rng.randint(2, 4))
    font, size = rng.choice(SANS), rng.choice([13, 14, 15])
    return page("<pre>" + "\n".join(esc(l) for l in lines) + "</pre>", bg, muted, font, size), lines, {"font": font, "size": size, "fg": muted}


def table():
    bg, fg, muted, acc = theme()
    head, rows = rng.choice(TABLES)
    font, size = rng.choice(SANS + MONO), rng.choice([13, 14, 15])
    css = f"table{{border-collapse:collapse}}td,th{{padding:6px 22px 6px 0;text-align:left;border-bottom:1px solid {muted}}}th{{color:{acc}}}"
    body = "<table><tr>" + "".join(f"<th>{esc(h)}</th>" for h in head) + "</tr>" + "".join(
        "<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in rows) + "</table>"
    gt = [" ".join(head)] + [" ".join(r) for r in rows]
    return page(body, bg, fg, font, size, css), gt, {"font": font, "size": size}


def identifiers():
    bg, fg, muted, acc = theme()
    lines = ident_lines()
    font, size = rng.choice(MONO + SANS), rng.choice([13, 14, 15])
    return page("<pre>" + "\n".join(esc(l) for l in lines) + "</pre>", bg, fg, font, size), lines, {"font": font, "size": size}


def numbers():
    bg, fg, muted, acc = theme()
    lines = number_lines()
    font, size = rng.choice(SANS + SERIF + MONO), rng.choice([13, 14, 15, 16])
    return page("<pre>" + "\n".join(esc(l) for l in lines) + "</pre>", bg, fg, font, size), lines, {"font": font, "size": size}


def accented():
    bg, fg, muted, acc = theme()
    lines = rng.sample(ACCENTED, rng.randint(3, 5))
    font, size = rng.choice(SANS + SERIF), rng.choice([14, 15, 16])
    return page("<pre>" + "\n".join(esc(l) for l in lines) + "</pre>", bg, fg, font, size), lines, {"font": font, "size": size}


def mixed():
    bg, fg, muted, acc = theme()
    title = rng.choice(["Release Notes", "Getting Started", "Weekly Summary", "Account Overview", "Troubleshooting"])
    sub = rng.choice(["Updated 2 days ago", "Version 3.1 - October 2024", "Read time: 4 min", "Last synced 10:42"])
    body_lines = rng.sample(PROSE, 3)
    font = rng.choice(SANS + SERIF)
    html_body = (f'<div style="font-size:30px;font-weight:700;color:{acc}">{esc(title)}</div>'
                 f'<div style="font-size:13px;color:{muted};font-style:italic;margin-bottom:12px">{esc(sub)}</div>'
                 + "".join(f'<div style="{"font-weight:700;" if i == 0 else ""}">{esc(l)}</div>' for i, l in enumerate(body_lines)))
    return page(html_body, bg, fg, font, 16), [title, sub] + body_lines, {"font": font, "size": "13-30"}


CATEGORIES = [
    ("terminal", terminal, 10), ("code", code, 10), ("prose", prose, 8), ("ui", ui, 10),
    ("small_text", small_text, 8), ("low_contrast", low_contrast, 8), ("table", table, 8),
    ("identifiers", identifiers, 10), ("numbers", numbers, 8), ("accented", accented, 8),
    ("mixed_styles", mixed, 12),
]
assert sum(n for _, _, n in CATEGORIES) == 100
CATEGORIES = [(c, f, max(1, round(n * PER_CATEGORY_SCALE))) for c, f, n in CATEGORIES]


def render(html_text, scale, out_png):
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "p.html"
        src.write_text(html_text, encoding="utf-8")
        raw = Path(td) / "raw.png"
        subprocess.run(
            ["chromium", "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
             f"--user-data-dir={td}/prof", f"--force-device-scale-factor={scale}",
             "--window-size=1500,1000", f"--screenshot={raw}", src.as_uri()],
            check=True, capture_output=True, timeout=60)
        img = Image.open(raw).convert("RGB")
    bg = Image.new("RGB", img.size, img.getpixel((2, 2)))
    bbox = ImageChops.difference(img, bg).getbbox()
    pad = int(rng.randint(8, 40) * scale)
    x0, y0, x1, y1 = bbox
    img.crop((max(0, x0 - pad), max(0, y0 - pad), min(img.width, x1 + pad), min(img.height, y1 + pad))).save(out_png)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    idx = 0
    for cat, fn, n in CATEGORIES:
        for _ in range(n):
            idx += 1
            sid = f"{idx:03d}_{cat}"
            html_text, gt, meta = fn()
            scale = rng.choice(SCALES)
            render(html_text, scale, OUT / f"{sid}.png")
            (OUT / f"{sid}.gt.txt").write_text("\n".join(gt) + "\n", encoding="utf-8")
            manifest.append({"id": sid, "category": cat, "scale": scale, **meta})
            print(sid, scale, meta.get("font"), flush=True)
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1))


if __name__ == "__main__":
    main()
