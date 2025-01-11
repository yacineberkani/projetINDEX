# Projet : Système d’Indexation et de Recherche

Ce projet consiste à construire un système qui permet de :
1. **Index** un corpus de documents textuels (ex. BA_AirlineReviews.csv).
2. **Rechercher** rapidement un mot ou une expression (moteur de recherche).
3. **Afficher** des informations statistiques et un Word Cloud via une interface utilisateur **Dash**.

---

## Table des matières
1. [Aperçu](#aperçu)
2. [Structure du projet](#structure-du-projet)
3. [Installation](#installation)
4. [Exécution](#exécution)
5. [Fonctionnalités principales](#fonctionnalités-principales)
6. [Points d’amélioration](#points-damélioration)
7. [Licence](#licence)

---

## Aperçu
L’application permet de :
- **Charger** un fichier CSV (ex. `BA_AirlineReviews.csv`) qui contient les avis, titres, etc.  
- **Construire** un index inversé : chaque mot est associé à la liste des documents (et positions) où il apparaît.  
- **Rechercher** un mot unique, plusieurs mots (AND/OR) ou une expression exacte (phrase).  
- **Visualiser** les résultats dans une application Dash : 
  - Liste des documents retrouvés  
  - Statistiques (nombre d’occurrences, moyenne d’apparitions, distribution)  
  - Extraits de texte (contexte autour du mot/phrase)  
  - Word Cloud des mots voisins

---

## Structure du projet

````
projetINDEX/
|-- main.py                 # Point d'entrée principal : lance l'application Dash
|-- index_building.py       # Contient la construction de l'index inversé
|-- search_functions.py     # Contient les fonctions de recherche
|-- utils.py                # Petites fonctions utilitaires (extraits, stats, word cloud, etc.)
|-- requirements.txt        # Vos dépendances (pandas, dash, plotly, wordcloud, etc.)
|-- BA_AirlineReviews.csv   # Votre jeu de données
|-- ...
`````

**Fichiers clés** :  
- **`index_building.py`** : Implémente la construction de l’index inversé à partir du CSV.  
- **`search_functions.py`** : Contient la logique de recherche (mot unique, phrase exacte, etc.).  
- **`utils.py`** : Fonctions d’affichage d’extraits, calcul de stats, génération du Word Cloud.  
- **`main.py`** : Lance l’application Dash ; se charge de la partie interface utilisateur et callbacks Dash.

---

## Installation

1. **Cloner** ou télécharger ce dépôt.  
2. **Installer les dépendances** (soit avec `pip`, soit avec un environnement virtuel) :

   ```bash
   pip install -r requirements.txt
   ```