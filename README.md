📊 Projet Data Filter

Auteur : [Votre Nom]
Dernière mise à jour : Jour 4

Ce projet est une application en ligne de commande (CLI) développée en Python, visant à offrir un outil robuste pour le chargement, la manipulation (tri, filtrage, statistiques) et la sauvegarde de données structurées (CSV, JSON, etc.).

🚀 État du Projet (Jour 4)

Les fonctionnalités de base d'Entrée/Sortie (E/S) sont terminées. Nous commençons les fonctionnalités de manipulation des données.

✅ Fonctionnalités Implémentées

Jours

Catégorie

Description

Statut

J1

Structure

Menu interactif de navigation principal.

Terminé

J2

Chargement

Sous-menu pour charger des fichiers CSV et JSON. Logique de robustesse (convertir_type) implémentée pour gérer les chaînes, les nombres, les booléens et les valeurs manquantes/nulles.

Terminé

J3

Sauvegarde

Sous-menu pour sauvegarder les données en CSV et JSON. Gestion des en-têtes pour le CSV.

Terminé

J2-J3

Affichage

Aperçu des données chargées (Option 2).

Terminé

J4

Tri Simple

Tri par une seule colonne, gestion du sens (Ascendant/Descendant) et gestion robuste des valeurs nulles (None).

Terminé

🛠️ Fichiers Clés

Fichier

Description

data_filter.py

Le code source principal de l'application (contient toute la logique : menu, E/S, utilitaires, tri).

items.csv

Fichier de données de test pour la robustesse (contient des valeurs invalides, manquantes et des types variés).

items.json

Fichier de données de test au format JSON.

📅 Plan de Travail Détaillé

Voici le plan des étapes restantes à réaliser :

Jour

Objectif

Détail de l'Implémentation

Statut

J4

Tri Simple (Monocritère)

Implémentation du tri par une seule colonne, gestion du sens (ascendant/descendant) et de la cohérence des types.

TERMINÉ

J5

Statistiques (Base)

Calcul des valeurs Min/Max/Moyenne pour les colonnes numériques.

À faire

J6

Statistiques (Avancées)

Calcul des Mediane/Mode, analyse de la distribution des types (string, int, float, bool) et détection des valeurs nulles.

À faire

J7

Filtrage Simple

Implémentation des filtres de base (>, <, =, contient, commence par) pour une seule colonne.

À faire

J8

Filtrage Avancé

Ajout de la logique de combinaisons de filtres (ET / OU).

À faire

J9

E/S Avancées

Ajout du support pour les formats YAML et XML (nécessite l'installation de librairies supplémentaires).

À faire

J10

Tri Multi-critères

Extension de la fonctionnalité de tri pour pouvoir trier sur plusieurs colonnes successives.

À faire

J11

Projection

Création d'une fonction pour sélectionner uniquement certaines colonnes et les afficher/sauvegarder (projection).

À faire

J12

Gestion d'État

Implémentation de l'Historique (Undo/Redo) et de la Gestion des Champs (Ajouter/Retirer des colonnes).

À faire

⚙️ Instructions de Lancement

Prérequis

Python 3.x installé.

(Pour les Jours 9 et suivants) : Vous aurez besoin de modules comme pyyaml ou xmltodict.

Lancement

Clonez ou téléchargez ce dépôt.

Assurez-vous que le fichier data_filter.py est présent.

Ouvrez votre terminal (dans PyCharm ou ailleurs) et naviguez vers le répertoire du projet.

Exécutez l'application avec la commande :

python data_filter.py


Test Rapide

Dans le menu principal, tapez 1 (Charger les Données).

Tapez 1 (CSV) et entrez le chemin items.csv.

Tapez 5 (Tri).

Choisissez une colonne (ex: 3 pour price) et l'ordre (a ou d).

Tapez 2 (Afficher les Données) pour vérifier le résultat.

Test Rapide

Dans le menu principal, tapez 1 (Charger les Données).

Tapez 1 (CSV) et entrez le chemin items.csv.

Tapez 3 (Statistiques) pour voir les Min/Max/Moyenne des colonnes id, price et quantity.