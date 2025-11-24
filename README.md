Projet Data Filter

Auteur : [Votre Nom]
Dernière mise à jour : Jour 3

Ce projet est une application en ligne de commande (CLI) développée en Python, visant à offrir un outil robuste pour le chargement, la manipulation (tri, filtrage, statistiques) et la sauvegarde de données structurées (CSV, JSON, etc.).

État du Projet (Jour 3)

Le squelette du projet est en place. Les fonctionnalités de base d'Entrée/Sortie (E/S) pour les formats standards sont terminées.

Fonctionnalités Implémentées

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

Fichiers Clés

Fichier

Description

data_filter.py

Le code source principal de l'application (contient toute la logique : menu, E/S, utilitaires).

items.csv

Fichier de données de test pour la robustesse (contient des valeurs invalides, manquantes et des types variés).

items.json

Fichier de données de test au format JSON.

Plan de Travail Détaillé

Voici le plan des étapes restantes à réaliser :

Jour

Objectif

Détail de l'Implémentation

J4

Tri Simple (Monocritère)

Implémentation du tri par une seule colonne, gestion du sens (ascendant/descendant) et de la cohérence des types.

J5

Statistiques (Base)

Calcul des valeurs Min/Max/Moyenne pour les colonnes numériques.

J6

Statistiques (Avancées)

Calcul des Mediane/Mode, analyse de la distribution des types (string, int, float, bool) et détection des valeurs nulles.

J7

Filtrage Simple

Implémentation des filtres de base (>, <, =, contient, commence par) pour une seule colonne.

J8

Filtrage Avancé

Ajout de la logique de combinaisons de filtres (ET / OU).

J9

E/S Avancées

Ajout du support pour les formats YAML et XML (nécessite l'installation de librairies supplémentaires).

J10

Tri Multi-critères

Extension de la fonctionnalité de tri pour pouvoir trier sur plusieurs colonnes successives.

J11

Projection

Création d'une fonction pour sélectionner uniquement certaines colonnes et les afficher/sauvegarder (projection).

J12

Gestion d'État

Implémentation de l'Historique (Undo/Redo) et de la Gestion des Champs (Ajouter/Retirer des colonnes).

Instructions de Lancement

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

Tapez 2 (Afficher les Données) pour vérifier la robustesse.

Tapez 6 (Sauvegarder les Données) pour tester l'exportation.