#!/bin/bash

echo "=== START BUILD PROCESS ==="

# 1. Mise à jour de pip et installation des dépendances
# On utilise python3.12 pour correspondre à ton runtime Vercel
python3.12 -m pip install --upgrade pip
python3.12 -m pip install -r requirements.txt

# 2. Installation de Node et compilation Tailwind
echo "=== COMPILING TAILWIND ==="
npm install
npm run build

# 3. Collecte des fichiers statiques
echo "=== COLLECTING STATIC FILES ==="
# On s'assure que Django est bien utilisé via le même binaire python
python3.12 manage.py collectstatic --noinput --clear

echo "=== BUILD FINISHED ==="