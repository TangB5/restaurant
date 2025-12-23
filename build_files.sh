#!/bin/bash

echo "=== START BUILD PROCESS ==="

# 1. Installation des dépendances dans le dossier courant
python3.12 -m pip install -r requirements.txt

# 2. Tailwind
echo "=== COMPILING TAILWIND ==="
npm install
npm run build

# 3. Collectstatic vers le dossier attendu par Vercel (staticfiles_build)
echo "=== COLLECTING STATIC FILES ==="
python3.12 manage.py collectstatic --noinput --clear

# 4. Déplacer les fichiers vers le distDir défini dans vercel.json
mkdir -p staticfiles_build
cp -r static/* staticfiles_build/
# Si collectstatic a créé un dossier staticfiles ou static_root, on le copie aussi
cp -r staticfiles/* staticfiles_build/ 2>/dev/null || :

echo "=== BUILD FINISHED ==="