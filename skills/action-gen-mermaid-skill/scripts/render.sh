#!/usr/bin/env bash
# render.sh — Mermaid (.mmd) → self-contained HTML viewer with embedded SVG
#
# Usage:
#   render.sh <input.mmd> <output_dir>          # render only
#   render.sh <input.mmd> <output_dir> --open    # render + open in browser
#
# Output files:
#   <output_dir>/mermaid-diagram.svg     ← raw SVG
#   <output_dir>/viewer.html             ← self-contained HTML (SVG embedded)
#
set -euo pipefail

INPUT="${1:?Usage: render.sh <input.mmd> <output_dir> [--open]}"
OUTPUT_DIR="${2:?Usage: render.sh <input.mmd> <output_dir> [--open]}"
OPEN_VIEWER="${3:-}"

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE="$SCRIPT_DIR/assets/viewer.html"
SVG_FILE="$OUTPUT_DIR/mermaid-diagram.svg"
VIEWER_FILE="$OUTPUT_DIR/viewer.html"

mkdir -p "$OUTPUT_DIR"

# --- Puppeteer config ---
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

cat > "$TMPDIR/puppeteer.json" << 'EOF'
{
  "executablePath": "/usr/bin/google-chrome-stable",
  "args": ["--no-sandbox", "--disable-setuid-sandbox"],
  "protocolTimeout": 60000
}
EOF

# --- Render SVG ---
PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable \
  mmdc -i "$INPUT" -o "$SVG_FILE" -p "$TMPDIR/puppeteer.json" -b transparent 2>/dev/null

echo "✅ SVG: $SVG_FILE"

# --- Build self-contained viewer (inline SVG into template) ---
# Split template at placeholder and sandwich SVG between halves
{
  sed '/<!--SVG_PLACEHOLDER-->/,$d' "$TEMPLATE"
  cat "$SVG_FILE"
  sed '1,/<!--SVG_PLACEHOLDER-->/d' "$TEMPLATE"
} > "$VIEWER_FILE"

echo "✅ Viewer: $VIEWER_FILE"

# --- Open in browser ---
if [ "$OPEN_VIEWER" = "--open" ]; then
  if command -v open &>/dev/null; then
    open "$VIEWER_FILE"
  elif command -v xdg-open &>/dev/null; then
    xdg-open "$VIEWER_FILE" &>/dev/null &
  else
    echo "⚠️  No browser opener found. Open manually: $VIEWER_FILE"
  fi
  echo "🌐 Opened viewer in browser"
fi
