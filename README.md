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