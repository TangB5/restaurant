#!/bin/bash

# Installer les dépendances Python
pip install -r requirements.txt

# Installer Node et compiler Tailwind
npm install
npm run build

# Collecter les fichiers statiques
python3.12 manage.py collectstatic --noinput --clear