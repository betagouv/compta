# Outil de facilitation du suivi budgétaire et comptable

Ce dépôt contient deux parties : 
- Une application qui récupère et formatte les données sur le Google Spreadsheet (le "back")
- Une application qui présente les données pour qu'elle soient utiles aux utilisateurs de l'outil (le "front")

## Avant propos: les variables d'environnement
Créez un fichier `.env` à la racine avec les informations suivantes:
```txt
API_URL=http://localhost:8000/api/ # ou l'URL sur laquelle pointe l'api de votre backend
GOOGLE_API_KEY=[clé d'API developers.google.com]
SAMPLE_SPREADSHEET_ID=[identifiant de la feuille de calcul]
CONVENTION_METADATA_SHEET=1sl1NhOY6Q-xGWaAIX2wS5KNqCPLmetsqxJFJTUHMkS8
```

l'API repose sur l'API Google Sheet pour récupérer des données. Pour obtenir la clé d'API, rendez-vous sur obtenue sur https://console.developers.google.com 

## Le front

> En NextJS

Accéder au front-end
```bash
cd front
```

Installer l'application
```bash
npm ci
```

Lancer l'application
```bash
npm run dev
```

Vérifier que l'application tourne
```bash
python -mwebbrowser http://localhost:3000/
```

## Le back

> En Python

Accéder au front-end
```bash
cd back
```

Installer l'application
```bash
virtualenv .venv --python=python3.6
source .venv/bin/activate
pip install --requirement requirements.txt --upgrade
```

Lancer l'application
```bash
gunicorn app:app
```

Vérifier que l'application tourne
```bash
python -mwebbrowser http://localhost:8000/
```

## En production

NGINX
GUNICORN
PM2
