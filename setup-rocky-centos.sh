#!/usr/bin/env bash
set -euo pipefail

sudo dnf update -y
sudo dnf install -y python3 python3-pip python3-devel gcc gcc-c++ make sqlite sqlite-devel

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install --no-cache-dir -r requirements.txt
python -m src.doctor
