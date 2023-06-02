#!/usr/bin/sh

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt
    deactivate
fi

