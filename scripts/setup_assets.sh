#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$DIR" )"
VENDOR_DIR="$PROJECT_ROOT/static/vendor"
MONACO_DIR="$VENDOR_DIR/monaco-editor"

echo "Setting up assets in $VENDOR_DIR..."
mkdir -p "$VENDOR_DIR"

# Download Monaco Editor
if [ ! -d "$MONACO_DIR" ]; then
    echo "Downloading Monaco Editor..."
    TMP_DIR=$(mktemp -d)
    cd "$TMP_DIR"
    npm init -y > /dev/null
    npm install monaco-editor@0.44.0 > /dev/null
    cp -r node_modules/monaco-editor/min "$MONACO_DIR"
    cd - > /dev/null
    rm -rf "$TMP_DIR"
    echo "Monaco Editor setup complete."
else
    echo "Monaco Editor already exists."
fi

# Download Fonts
echo "Downloading Google Fonts..."
python3 "$DIR/setup_assets.py"
echo "All assets setup complete."
