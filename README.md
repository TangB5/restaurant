# 🍽️ Restaurant Management System

Une application web moderne construite avec **Django** et **Tailwind CSS**, déployée sur **Vercel** avec une base de données **PostgreSQL** hébergée sur **Supabase**.



## 🚀 Fonctionnalités
- 📜 **Gestion du Menu** : Affichage dynamique des plats par catégories.
- 📅 **Réservations** : Système de réservation de tables en ligne.
- 🛍️ **Commandes** : Gestion des commandes clients.
- 👤 **Comptes Utilisateurs** : Inscription, connexion et profil client.
- 🎨 **Design Responsive** : Interface fluide construite avec Tailwind CSS 4.
- 🛠️ **Panel Admin** : Gestion complète via l'interface d'administration Django.

## 🛠️ Stack Technique
- **Framework** : Django 5.2 (Python 3.12)
- **Base de données** : PostgreSQL (via Supabase)
- **Frontend** : Tailwind CSS 4, JavaScript
- **Déploiement** : Vercel
- **Gestion des fichiers statiques** : WhiteNoise

## 📁 Architecture du Projet
```text
.
├── restaurant/          # Configuration du projet (settings, wsgi, urls)
├── commandes/           # Application gestion des commandes
├── compte/              # Application gestion des utilisateurs
├── menu/                # Application gestion du catalogue (plats, prix)
├── reservation/         # Application gestion des réservations
├── static/              # Fichiers CSS, JS et Images de plats
├── templates/           # Templates HTML globaux
├── manage.py            # Script d'administration Django
├── vercel.json          # Configuration pour le déploiement Vercel
└── build_files.sh       # Script de build (Tailwind + Collectstatic)

⚙️ Installation Locale
Cloner le projet :

Bash

git clone [https://github.com/ton-pseudo/nom-du-repo.git](https://github.com/ton-pseudo/nom-du-repo.git)
cd nom-du-repo
Créer un environnement virtuel :

Bash

python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
Installer les dépendances :

Bash

pip install -r requirements.txt
npm install
Configurer la base de données : Assurez-vous d'avoir PostgreSQL installé localement ou configurez vos variables d'environnement dans un fichier .env.

Lancer les migrations et compiler Tailwind :

Bash

python manage.py migrate
npm run build
Démarrer le serveur :

Bash

python manage.py runserver
📦 Déploiement sur Vercel
Le projet est configuré pour un déploiement automatique sur Vercel.

Variables d'environnement nécessaires :

DATABASE_URL : URI de connexion PostgreSQL Supabase.

SECRET : Clé secrète Django.

DEBUG : False en production.

📄 Licence
Ce projet est sous licence MIT.


---

### Une astuce pour ton GitHub
Une fois que tu as ajouté ce fichier :
1. Fais un dernier `git add README.md`
2. `git commit -m "Docs: Add README with project description"`
3. `git push`

**Souhaites-tu que je t'écrive maintenant les commandes précises pour injecter tes données locales vers Supabase une fois que ton lien Vercel sera actif ?**