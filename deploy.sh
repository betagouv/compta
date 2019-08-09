#!/bin/bash

cd front
npm ci
${NVM_BIN}/pm2 reload compta

cd ../back
source .venv/bin/activate
pip install --requirement requirements.txt --upgrade
sudo systemctl daemon-reload
sudo systemctl restart api-compta
