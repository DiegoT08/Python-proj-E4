# Python-proj-E4

# Projet Loyers

## Description

Le projet "Loyers" permet de collecter, nettoyer, analyser et visualiser les données relatives aux loyers en France. Il génère des visualisations interactives pour comparer les loyers moyens par département, entre les départements littoraux et non littoraux, et bien plus encore. Ce projet utilise des technologies telles que Python, Dash, SQLAlchemy et PostgreSQL pour stocker et traiter les données.

## Fonctionnalités

- **Collecte de données** : Le projet charge et nettoie les données de loyers depuis un fichier CSV.
- **Base de données** : Crée automatiquement la base de données `loyers_db` et la table `loyers` dans PostgreSQL si elles n'existent pas.
- **Visualisation** : Génère des graphiques et des cartes interactives pour analyser les loyers en fonction de différents critères.
- **Interface Web** : Un tableau de bord est créé avec Dash pour afficher les résultats de l'analyse, y compris des cartes des loyers par département et des histogrammes.

## Prérequis

- Python 3.7+
- PostgreSQL installé et configuré localement
- Le fichier `requirements.txt` contient toutes les bibliothèques nécessaires.

### Dépendances

Le projet nécessite plusieurs bibliothèques Python pour fonctionner. Vous pouvez les installer en utilisant `pip` :

```bash
pip install -r requirements.txt