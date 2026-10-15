#!/bin/bash

# omarchy-ppocr installer
#
#   ./install.sh               install, download models, bind SUPER+CTRL+PRINT
#   ./install.sh --no-bind     install without touching keybindings
#   ./install.sh --uninstall   remove everything and restore the Omarchy default binding
#   ./install.sh --from-plugin used by the Omarchy shell plugin: explain, ask, then install

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOME_DIR="${OMARCHY_PPOCR_HOME:-$HOME/.local/share/omarchy-ppocr}"
BIN_DIR="$HOME/.local/bin"
BINDINGS="$HOME/.config/hypr/bindings.lua"
BEGIN="-- omarchy-ppocr: begin. Written by omarchy-ppocr install.sh; './install.sh --uninstall' removes the block."
END="-- omarchy-ppocr: end."

RAPIDOCR_VERSION="3.10.0"
ONNXRUNTIME_VERSION="1.31.0"

say() { printf '\033[1;34m==>\033[0m %s\n' "$*"; }
die() { printf '\033[1;31merror:\033[0m %s\n' "$*" >&2; exit 1; }

remove_binding() {
  [[ -f $BINDINGS ]] || return 0
  sed -i "/^-- omarchy-ppocr: begin/,/^-- omarchy-ppocr: end/d" "$BINDINGS"
}

reload_hyprland() {
  command -v hyprctl >/dev/null || return 0
  hyprctl reload >/dev/null
  local errors
  errors=$(hyprctl configerrors 2>/dev/null || true)
  if [[ -n ${errors//[[:space:]]/} ]]; then
    echo "$errors"
    die "Hyprland reported config errors (see above)"
  fi
}

if [[ ${1:-} == "--uninstall" ]]; then
  say "Removing keybinding"
  remove_binding
  reload_hyprland
  say "Removing scripts and models"
  rm -f "$BIN_DIR/omarchy-ppocr-capture" "$BIN_DIR/omarchy-ppocr-extract"
  rm -rf "$HOME_DIR"
  say "Uninstalled. SUPER+CTRL+PRINT is back to Omarchy's default OCR."
  if [[ -d $HOME/.config/omarchy/plugins/io.github.devrahulbanjara.ppocr ]]; then
    echo "    To remove the shell plugin too: omarchy plugin remove io.github.devrahulbanjara.ppocr"
  fi
  exit 0
fi

BIND=1
[[ ${1:-} == "--no-bind" ]] && BIND=0

if [[ ${1:-} == "--from-plugin" ]]; then
  cat <<'INFO'
PP-OCR plugin setup

This will:
  * create a Python environment in ~/.local/share/omarchy-ppocr (rapidocr + onnxruntime, ~150 MB)
  * download the PP-OCRv6 small models (~31 MB)
  * install omarchy-ppocr-capture / omarchy-ppocr-extract into ~/.local/bin
  * rebind Super+Ctrl+Print to PP-OCR (your bindings.lua is backed up first)

No sudo. Undo any time with: ~/.config/omarchy/plugins/io.github.devrahulbanjara.ppocr/install.sh --uninstall

INFO
  if command -v gum >/dev/null; then
    gum confirm "Install PP-OCR?" || exit 130
  else
    read -rp "Install PP-OCR? [Y/n] " answer
    [[ -z $answer || $answer == [Yy]* ]] || exit 130
  fi
fi

for dep in grim slurp wl-copy hyprpicker; do
  command -v "$dep" >/dev/null || die "missing $dep (it ships with Omarchy)"
done

say "Creating Python environment in $HOME_DIR/venv"
mkdir -p "$HOME_DIR" "$BIN_DIR"
if command -v uv >/dev/null; then
  # onnxruntime wheels lag behind the newest CPython, so pin a well-supported one
  uv venv --quiet --allow-existing --python 3.12 "$HOME_DIR/venv"
  uv pip install --quiet --python "$HOME_DIR/venv/bin/python" \
    "rapidocr==$RAPIDOCR_VERSION" "onnxruntime==$ONNXRUNTIME_VERSION"
else
  python3 -m venv "$HOME_DIR/venv"
  "$HOME_DIR/venv/bin/pip" install --quiet \
    "rapidocr==$RAPIDOCR_VERSION" "onnxruntime==$ONNXRUNTIME_VERSION" ||
    die "pip install failed; installing uv (omarchy pkg add uv) lets this script use Python 3.12"
fi

say "Installing scripts to $BIN_DIR"
install -m 644 "$REPO/lib/extract.py" "$HOME_DIR/extract.py"
cat >"$BIN_DIR/omarchy-ppocr-extract" <<EOF
#!/bin/bash
exec "$HOME_DIR/venv/bin/python" "$HOME_DIR/extract.py" "\$@"
EOF
chmod 755 "$BIN_DIR/omarchy-ppocr-extract"
install -m 755 "$REPO/bin/omarchy-ppocr-capture" "$BIN_DIR/omarchy-ppocr-capture"

say "Downloading PP-OCRv6 models (~31 MB, one time)"
"$BIN_DIR/omarchy-ppocr-extract" "$REPO/assets/sample.png" >/dev/null ||
  die "test OCR run failed"
echo "    self-test: $("$BIN_DIR/omarchy-ppocr-extract" "$REPO/assets/sample.png" | head -1)"

if (( BIND )); then
  [[ -f $BINDINGS ]] || die "$BINDINGS not found; rerun with --no-bind and bind omarchy-ppocr-capture yourself"
  say "Binding SUPER+CTRL+PRINT in $BINDINGS (was: Omarchy's Tesseract OCR)"
  cp "$BINDINGS" "$BINDINGS.bak.$(date +%s)"
  remove_binding
  cat >>"$BINDINGS" <<EOF

$BEGIN
hl.unbind("SUPER + CTRL + PRINT")
o.bind("SUPER + CTRL + PRINT", "Extract text (OCR) with PP-OCRv6", "$BIN_DIR/omarchy-ppocr-capture")
$END
EOF
  reload_hyprland
fi

say "Done. Press SUPER+CTRL+PRINT, select a region, and the text is on your clipboard."
