#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
source ~/.zprofile
exec "$DIR/.venv/bin/python" "$DIR/src/menubar.py"
