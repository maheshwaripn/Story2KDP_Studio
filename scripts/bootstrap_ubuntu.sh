#!/usr/bin/env bash
set -euo pipefail
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip git libglib2.0-0 libgl1 fonts-dejavu-core
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[web,dev]'
echo 'Ready: source .venv/bin/activate && streamlit run app.py --server.address 127.0.0.1'
