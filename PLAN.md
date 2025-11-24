# Projet DATA FILTER

## 📅 Plan de Travail Détaillé (12 Jours)

### 📌 Phase 1 : Le Noyau Fonctionnel (Jours 1-4)
*Objectif : Mettre en place la structure, le menu, le chargement/sauvegarde de base (CSV/JSON), et le tri simple.*

| Jour | Tâche Principale | Sous-tâches et Explications | Éléments Nécessaires |
| :---: | :--- | :--- | :--- |
| **J1** | **Structure du Projet & Menu Interactif** | 1. **Initialisation :** Créer le fichier `data_filter.py`. 2. **Boucle Principale :** Implémenter la boucle infinie pour le menu. 3. **Affichage :** Définir et afficher le **Menu Principal** et les messages de base. 4. **Interaction :** Gérer la saisie utilisateur et le retour au menu. | Python standard. |
| **J2** | **Chargement de Base (JSON/CSV)** | 1. **Module `json` :** Écrire la fonction `load_json(filepath)` pour lire les données. 2. **Module `csv` :** Écrire la fonction `load_csv(filepath)` en utilisant `csv.DictReader` et en **assurant la robustesse** (conversion des chaînes en `int`/`float`/`bool` avec `try/except`). 3. **Intégration :** Lier ces fonctions au Menu Interactif. | Module `json`, Module `csv`. |
| **J3** | **Sauvegarde de Base (JSON/CSV)** | 1. **Module `json` :** Écrire la fonction `save_json(data, filepath)`. 2. **Module `csv` :** Écrire la fonction `save_csv(data, filepath)`. 3. **Sous-Menu Sauvegarde :** Implémenter le sous-menu pour choisir le format (Option 6). | Module `json`, Module `csv`. |
| **J4** | **Tri Simple (Monocritère)** | 1. **Sous-Menu Tri (Simple) :** Demander le champ et l'ordre (Asc/Desc). 2. **Implémentation :** Utiliser la fonction `sorted()` de Python avec une `lambda` pour trier la liste de dictionnaires selon le champ choisi (`key=lambda x: x['champ']`). 3. **Affichage :** Afficher un aperçu des données triées (Option 2 du menu). | Python standard (fonction `sorted()`). |

### 📌 Phase 2 : Le Cœur (Jours 5-8)
*Objectif : Implémenter les fonctionnalités de filtrage et de statistiques, en couvrant le minimum requis (Noir).*

| Jour | Tâche Principale | Sous-tâches et Explications | Éléments Nécessaires |
| :---: | :--- | :--- | :--- |
| **J5** | **Statistiques (Type Détermination)** | 1. **Détermination du Type :** Créer une fonction pour parcourir les premières entrées et déterminer le type dominant de chaque champ (`numeric`, `boolean`, `string`, `list`). 2. **Préparation des Données :** Créer des listes séparées pour les valeurs de chaque type (ex: `all_ages`, `all_apprentice_values`). | Python standard. |
| **J6** | **Statistiques (Calcul de Base)** | 1. **Numérique :** Coder les fonctions `calculate_min_max_avg(values)`. Gérer la **robustesse** (ignorer les non-numériques). 2. **Booléen :** Coder la fonction pour calculer le % Vrai et % Faux. 3. **Liste :** Coder la fonction pour calculer Min/Max/Moyenne sur la **taille** des listes. 4. **Affichage :** Intégrer et formater l'affichage des stats (Option 3). | Python standard. |
| **J7** | **Filtrage de Base (Numérique & Booléen)** | 1. **Sous-Menu Filtrage :** Mettre en place le menu pour ajouter des critères simples. 2. **Logique de Filtrage :** Coder la fonction qui gère les comparaisons ($<, >, =, \text{etc.}$) pour les champs numériques et booléens. | Python standard. |
| **J8** | **Filtrage de Base (Chaîne & Liste)** | 1. **Chaîne :** Implémenter le filtrage par **ordre lexicographique** ($<, >$). 2. **Liste :** Implémenter le filtrage par **taille de la liste**. 3. **Combinaison de Critères :** Permettre l'application de **multiples filtres** via l'opérateur logique `ET` (`AND`). | Python standard. |

### 📌 Phase 3 : Les Avancées (Jours 9-11)
*Objectif : Déployer les fonctionnalités "pour aller plus loin" (Bleu), y compris les librairies externes et les structures complexes.*

| Jour | Tâche Principale | Sous-tâches et Explications | Éléments Nécessaires |
| :---: | :--- | :--- | :--- |
| **J9** | **Chargement/Sauvegarde Avancés** | 1. **Installation :** Installer la librairie `pyyaml`. 2. **YAML :** Intégrer `yaml.safe_load` et `yaml.dump` aux menus (Gestion du support **YAML**). 3. **XML :** Intégrer l'utilisation de `xml.etree.ElementTree` pour lire/écrire le format **XML**. | Module `PyYAML`, Module `xml.etree.ElementTree`. |
| **J10** | **Tri Avancé & Stats Avancées** | 1. **Tri Multi-Critères :** Permettre à l'utilisateur de définir une séquence de champs de tri. 2. **Tri Combiné :** Permettre le tri sur une valeur calculée (`price * quantity` ou `moyenne des grades`). 3. **Stats Avancées :** Implémenter le calcul de la **Valeur Globale** ($price \times quantity$) et son affichage dans les stats. **Optionnel :** Installer `numpy` pour le calcul du percentile. | Module `numpy` (Optionnel). |
| **J11** | **Filtrage Avancé** | 1. **Critères Textuels :** Ajouter les opérateurs **contient**, **commence par**, **finit par** pour les chaînes. 2. **Comparaison aux Stats :** Permettre de filtrer par rapport à la **Moyenne Globale** et au **Percentile** (en utilisant le seuil calculé au J10). 3. **Comparaison de Champ à Champ :** (Ex: $firstname < lastname$). | Python standard. |

### 📌 Phase 4 : Finalisation et Robustesse (Jour 12)
*Objectif : Intégrer l'historique et finaliser le code pour la livraison.*

| Jour | Tâche Principale | Sous-tâches et Explications | Éléments Nécessaires |
| :---: | :--- | :--- | :--- |
| **J12** | **Historique & Finalisation** | 1. **Historique :** Définir la structure de la **Pile d'Historique**. 2. **Undo/Redo :** Intégrer la logique de `push` (sauvegarder l'état avant chaque tri/filtrage) et de `pop` (restaurer l'état) dans le Menu Principal (Option 7). 3. **Gestion des Champs :** Implémenter l'ajout/retrait de champs (Option 8). 4. **Nettoyage :** Ajouter les commentaires, vérifier le bon découpage du programme et s'assurer que le script est **exécutable en console**. | Structure de données "Pile" (liste Python). |

---

Ce plan vous offre une feuille de route solide. N'oubliez pas que le **découpage du programme** (fonctions, classes si vous le souhaitez) et la **qualité de l'interface** sont cruciaux pour la notation !