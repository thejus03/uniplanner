#!/usr/bin/env bash
# exit on error
set -o errexit
sudo apt install -y libsystemd-dev
pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
