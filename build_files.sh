#!/bin/bash

echo "=== START BUILD PROCESS ==="

python3.12 -m pip install -r requirements.txt

echo "=== COMPILING TAILWIND ==="
npm install
npm run build


echo "=== COLLECTING STATIC FILES ==="
python3.12 manage.py collectstatic --noinput --clear

echo "=== BUILD FINISHED ==="