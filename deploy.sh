#!/bin/bash

cd front
npm ci
npm run reload

cd ../back
source .venv/bin/activate
pip install --requirement requirements.txt --upgrade
sudo systemctl daemon-reload
sudo systemctl restart api-compta
