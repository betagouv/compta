# Outil de facilitation du suivi budgétaire et comptable


Ce dépôt contient deux parties

## Le front

> En NextJS

```bash
cd front
npm ci
npm run dev
python -mwebbrowser http://localhost:3000/
````

## Le back

> En Python

Qui repose sur l'API Google Sheet pour récupérer des données.
Une clé d'API est nécessaire : https://console.developers.google.com

```bash
cd back
virtualenv .venv --python=python3.6
source .venv/bin/activate
pip install --requirement requirements.txt --upgrade
GOOGLE_API_KEY=VOTRE-CLE-API-GOOGLE gunicorn app:app
python -mwebbrowser http://localhost:8000/
```

## En production

NGINX
GUNICORN
PM2
