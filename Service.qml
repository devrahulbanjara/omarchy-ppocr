import QtQuick
import Quickshell
import Quickshell.Io

// Headless companion for omarchy-ppocr.
//
// - First load after `omarchy plugin add`: if the OCR engine isn't installed yet,
//   opens install.sh once in a floating terminal (it asks before doing anything).
// - Pre-warms the OCR server at shell start so the first capture is fast too.
// - IPC: omarchy-shell ppocr capture | install | warm | stop
Item {
  id: root

  property var shell: null
  property var manifest: null

  readonly property string home: Quickshell.env("HOME")
  readonly property string pluginDir: String(Qt.resolvedUrl(".")).replace(/^file:\/\//, "").replace(/\/$/, "")
  readonly property string extract: home + "/.local/bin/omarchy-ppocr-extract"
  readonly property string captureCmd: home + "/.local/bin/omarchy-ppocr-capture"
  readonly property string promptedMarker: home + "/.local/share/omarchy-ppocr/.install-prompted"
  property bool installed: false

  function runInstaller() {
    Quickshell.execDetached(["omarchy-launch-floating-terminal-with-presentation",
                             "'" + pluginDir + "/install.sh' --from-plugin"])
  }

  function warm() {
    if (installed) Quickshell.execDetached([extract, "--serve"])
  }

  IpcHandler {
    target: "ppocr"

    function capture(): void {
      if (root.installed) Quickshell.execDetached([root.captureCmd])
      else root.runInstaller()
    }

    function install(): void { root.runInstaller() }

    function warm(): void { root.warm() }

    function stop(): void {
      if (root.installed) Quickshell.execDetached([root.extract, "--stop"])
    }

    function status(): string {
      return root.installed ? "installed" : "not installed"
    }
  }

  // Exit 0 = installed, 2 = not installed and never prompted, 1 = not installed, already prompted.
  // When installed, sync the engine script from this checkout so `omarchy plugin update`
  // takes effect without re-running the installer (and restart a stale warm server).
  Process {
    id: probe
    command: ["bash", "-c",
      "if [[ -x \"$1\" ]]; then " +
      "  src=\"$3/lib/extract.py\"; dst=\"$(dirname \"$2\")/extract.py\"; " +
      "  if [[ -f $src && -f $dst ]] && ! cmp -s \"$src\" \"$dst\"; then install -m 644 \"$src\" \"$dst\"; \"$1\" --stop; fi; " +
      "  exit 0; " +
      "fi; " +
      "[[ -e \"$2\" ]] && exit 1; mkdir -p \"$(dirname \"$2\")\" && touch \"$2\"; exit 2",
      "probe", root.extract, root.promptedMarker, root.pluginDir]
    onExited: function(exitCode) {
      root.installed = exitCode === 0
      if (root.installed) root.warm()
      else if (exitCode === 2) root.runInstaller()
    }
  }

  Component.onCompleted: probe.running = true
}
