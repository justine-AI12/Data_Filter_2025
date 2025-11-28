import sys
import csv
import json
import statistics
from typing import List, Dict, Any, Union, Tuple, Callable
from collections import Counter
import math
import locale
import copy
import yaml  # Importation pour YAML (J9)
import xml.etree.ElementTree as ET  # Importation pour XML (J9)

# Alias de type pour clarifier la structure des données internes
DataList = List[Dict[str, Any]]


# --- FONCTIONS UTILITAIRES POUR LA ROBUSTESSE (J2) ---

def convertir_type(value: Any) -> Any:
    """
    Tente de convertir une chaîne de caractères en int, float ou booléen.

    Convertit les chaînes vides et les indicateurs N/A communs
    en 'None' pour assurer leur placement correct (à la fin) lors du tri.
    """

    # 1. Gérer les valeurs déjà converties par JSON (int, float, bool, list) et None
    if value is None:
        return None

    if isinstance(value, (int, float, bool, list)):
        return value

    # Si ce n'est pas None et ce n'est pas un type primitif, il DOIT être une chaîne
    if not isinstance(value, str):
        return value

    # À partir d'ici, 'value' est garanti être une chaîne (str)

    # Nettoyage et identification des valeurs manquantes (pour CSV/non-JSON)
    lower_value = value.strip().lower()

    # Traiter les chaînes vides ou les placeholders comme None
    if lower_value in ('', 'n/a', 'na', 'n.a.', 'nan', 'null'):
        return None

    # Tentative de conversion numérique
    try:
        # Tente d'abord de convertir en entier (si pas de point)
        if '.' not in value and value.strip() != "":
            return int(value)
        # Tente ensuite de convertir en flottant
        return float(value)
    except ValueError:
        pass  # La conversion numérique a échoué

    # Tentative de conversion booléenne
    if lower_value in ('true', 'vrai', 't', '1'):
        return True
    if lower_value in ('false', 'faux', 'f', '0'):
        return False

    return value  # Retourne la chaîne si aucune conversion n'est possible


def nettoyer_donnees(data: DataList) -> DataList:
    """
    Applique la fonction convertir_type à chaque valeur dans la liste de dictionnaires.
    C'est crucial pour les données lues depuis CSV (où tout est une chaîne).
    """
    donnees_nettoyees = []
    for item in data:
        nettoye = {k: convertir_type(v) for k, v in item.items()}
        donnees_nettoyees.append(nettoye)
    return donnees_nettoyees


# --- FONCTIONS DE CHARGEMENT (J2/J9) ---

def load_json(filepath: str) -> DataList:
    """Charge les données depuis un fichier JSON."""
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    if isinstance(raw_data, list):
        print(f"Succès : {len(raw_data)} enregistrements JSON chargés.")
        return nettoyer_donnees(raw_data)
    else:
        raise ValueError("Format JSON invalide : La racine doit être une liste d'enregistrements.")


def load_csv(filepath: str) -> DataList:
    """Charge les données depuis un fichier CSV."""
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    print(f"Succès : {len(data)} enregistrements CSV chargés.")
    return nettoyer_donnees(data)


def load_yaml(filepath: str) -> DataList:
    """Charge les données depuis un fichier YAML (J9)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_data = yaml.safe_load(f)

    if isinstance(raw_data, list):
        # YAML prend déjà en charge les types, mais on nettoie pour la cohérence
        print(f"Succès : {len(raw_data)} enregistrements YAML chargés.")
        return nettoyer_donnees(raw_data)
    else:
        raise ValueError("Format YAML invalide : La racine doit être une liste d'enregistrements.")


def load_xml(filepath: str) -> DataList:
    """
    Charge les données depuis un fichier XML (J9).
    Le XML est converti en une liste de dictionnaires.
    On suppose que le fichier a une structure de liste d'éléments similaires (ex: <root><item>...</item><item>...</item></root>).
    """
    tree = ET.parse(filepath)
    root = tree.getroot()
    data = []

    # On itère sur les enfants de la racine (ce qui représente les enregistrements)
    for element in root:
        record = {}
        # Les champs sont les sous-éléments ou les attributs

        # 1. Traiter les sous-éléments comme des champs
        for child in element:
            record[child.tag] = child.text

        # 2. Traiter les attributs de l'élément comme des champs (préfixés si besoin)
        for attr, value in element.attrib.items():
            record[attr] = value

        if record:
            data.append(record)

    if not data:
        raise ValueError("Format XML invalide ou vide : Aucune balise enfant trouvée sous l'élément racine.")

    print(f"Succès : {len(data)} enregistrements XML chargés.")
    return nettoyer_donnees(data)


def charger_donnees() -> DataList:
    """Gère le sous-menu pour le chargement des données (J2/J9)."""
    while True:
        print("\n" + "-" * 50)
        print("          SOUS-MENU CHARGEMENT")
        print("          Format(s) supporté(s) : 1, 2, 3, 4 (J9)")
        print("-" * 50)
        print("1. Charger un fichier CSV")
        print("2. Charger un fichier JSON")
        print("3. Charger un fichier YAML (J9 - Activé)")
        print("4. Charger un fichier XML (J9 - Activé)")
        print("0. Annuler et Retour au Menu Principal")
        print("-" * 50)

        choix = input("Votre choix de format : ").strip()

        if choix == '0':
            return []

        if choix in ('1', '2', '3', '4'):
            filepath = input("Entrez le chemin du fichier : ").strip()
            if not filepath:
                print("Chemin du fichier non valide.")
                continue

            try:
                if choix == '1':
                    return load_csv(filepath)
                elif choix == '2':
                    return load_json(filepath)
                elif choix == '3':
                    return load_yaml(filepath)
                elif choix == '4':
                    return load_xml(filepath)
            except FileNotFoundError:
                print(f"Erreur : Le fichier à l'emplacement '{filepath}' n'a pas été trouvé.")
            except ValueError as ve:
                print(f"Erreur de format de fichier : {ve}")
            except Exception as e:
                print(f"Erreur lors du chargement ou du traitement du fichier ({type(e).__name__}): {e}")

        else:
            print("Choix invalide.")

        input("Appuyez sur Entrée pour continuer...")


# --- FONCTIONS DE SAUVEGARDE (J3/J9) ---

def get_all_headers(data: DataList) -> List[str]:
    """
    Récupère l'ensemble des clés (en-têtes) présentes dans toutes les lignes de données.
    """
    headers = set()
    for row in data:
        headers.update(row.keys())

    if data:
        ordered_headers = list(data[0].keys())
        for h in sorted(list(headers - set(ordered_headers))):
            ordered_headers.append(h)
        return ordered_headers

    return list(sorted(list(headers)))


def save_json(data: DataList, filepath: str):
    """Sauvegarde les données au format JSON."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Succès : {len(data)} enregistrements sauvegardés au format JSON dans '{filepath}'.")


def save_csv(data: DataList, filepath: str):
    """Sauvegarde les données au format CSV."""
    if not data:
        raise ValueError("Impossible de sauvegarder : la liste de données est vide.")

    headers = get_all_headers(data)

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)

    print(f"Succès : {len(data)} enregistrements sauvegardés au format CSV dans '{filepath}'.")


def save_yaml(data: DataList, filepath: str):
    """Sauvegarde les données au format YAML (J9)."""
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
    print(f"Succès : {len(data)} enregistrements sauvegardés au format YAML dans '{filepath}'.")


def save_xml(data: DataList, filepath: str, root_tag: str = 'racine', item_tag: str = 'enregistrement'):
    """Sauvegarde les données au format XML (J9)."""
    if not data:
        raise ValueError("Impossible de sauvegarder : la liste de données est vide.")

    root = ET.Element(root_tag)

    for record in data:
        item = ET.SubElement(root, item_tag)
        for key, value in record.items():
            # Convertir toutes les valeurs en chaîne pour l'écriture XML
            value_str = "" if value is None else str(value)

            # Utiliser la balise pour le champ
            field = ET.SubElement(item, key)
            field.text = value_str

    # Créer l'arbre et sauvegarder
    tree = ET.ElementTree(root)
    # Utiliser un bel affichage pour la lisibilité
    ET.indent(tree, space="  ", level=0)
    tree.write(filepath, encoding='utf-8', xml_declaration=True)

    print(f"Succès : {len(data)} enregistrements sauvegardés au format XML dans '{filepath}'.")


def sauvegarder_donnees(data: DataList):
    """(J3/J9) Gère le sous-menu de sauvegarde."""
    if not data:
        print("\n[SOUS-MENU SAUVEGARDE] Aucune donnée à sauvegarder.")
        input("Appuyez sur Entrée pour continuer...")
        return

    while True:
        print("\n" + "-" * 50)
        print("          SOUS-MENU SAUVEGARDE")
        print("          Format(s) supporté(s) : 1, 2, 3, 4 (J9)")
        print("-" * 50)
        print("1. Sauvegarder en CSV")
        print("2. Sauvegarder en JSON")
        print("3. Sauvegarder en YAML (J9 - Activé)")
        print("4. Sauvegarder en XML (J9 - Activé)")
        print("0. Annuler et Retour au Menu Principal")
        print("-" * 50)

        choix = input("Votre choix de format : ").strip()

        if choix == '0':
            return

        if choix in ('1', '2', '3', '4'):
            filepath = input("Entrez le chemin du fichier de sortie : ").strip()
            if not filepath:
                print("Chemin du fichier non valide.")
                continue

            try:
                if choix == '1':
                    save_csv(data, filepath)
                elif choix == '2':
                    save_json(data, filepath)
                elif choix == '3':
                    save_yaml(data, filepath)
                elif choix == '4':
                    save_xml(data, filepath)

                input("Sauvegarde terminée. Appuyez sur Entrée pour continuer...")
                return
            except ValueError as ve:
                print(f"Erreur de données : {ve}")
            except Exception as e:
                print(f"Erreur lors de la sauvegarde du fichier ({type(e).__name__}): {e}")

        else:
            print("Choix invalide.")

        input("Appuyez sur Entrée pour continuer...")


# --- FONCTIONS DE MANIPULATION DES DONNÉES (J4+) ---

def afficher_donnees(data: DataList):
    """Affiche un aperçu des données actuellement chargées."""
    if not data:
        print("\n[APERÇU DES DONNÉES] Aucune donnée chargée.")
        return

    print(f"\n[APERÇU DES DONNÉES] {len(data)} enregistrement(s) chargé(s).")

    lignes_a_afficher = 5
    print("-" * 50)

    try:
        header = list(data[0].keys())
        print(" | ".join(header))
        print("-" * 50)

        for i, row in enumerate(data):
            if i >= lignes_a_afficher:
                break
            display_values = [repr(row.get(col, '')) for col in header]
            print(" | ".join(display_values))

        if len(data) > lignes_a_afficher:
            print(f"... ({len(data) - lignes_a_afficher} autres enregistrements)")

    except IndexError:
        print("Les données sont chargées mais la structure est vide ou incorrecte.")
    input("\nAppuyez sur Entrée pour continuer...")


def afficher_statistiques(data: DataList):
    """
    (J5/J6) Calcule et affiche les statistiques (Min/Max/Moyenne/Médiane/Mode/Écart-type)
    et la distribution des types pour chaque colonne.
    """
    print("\n[STATISTIQUES ET ANALYSE DE STRUCTURE] (Jour 6)")
    if not data:
        print("Veuillez d'abord charger les données.")
        input("Appuyez sur Entrée pour continuer...")
        return

    stats_numeriques: Dict[str, List[float]] = {}
    structure_types: Dict[str, Counter] = {}
    mode_results: Dict[str, List[Any]] = {}  # Utilisation de List[Any] pour stocker toutes les valeurs

    # 1. Collecter les valeurs
    for item in data:
        for key, value in item.items():

            if key not in structure_types:
                structure_types[key] = Counter()

            # Enregistrement des types pour l'analyse de structure
            type_name = 'None' if value is None else type(value).__name__
            structure_types[key][type_name] += 1

            # Collection pour les statistiques numériques
            if isinstance(value, (int, float)):
                if key not in stats_numeriques:
                    stats_numeriques[key] = []
                stats_numeriques[key].append(float(value))

                # Collection pour le Mode
            if key not in mode_results:
                mode_results[key] = []
            mode_results[key].append(value)

    # --- PARTIE J5/J6 : STATISTIQUES NUMÉRIQUES ---
    print("\n--- Statistiques de Tendance Centrale et de Dispersion (Numérique) ---")

    if not stats_numeriques:
        print("Aucune colonne purement numérique (int ou float) n'a été trouvée pour cette analyse.")
    else:
        header_num = f"{'Colonne':<20} | {'Min':<10} | {'Max':<10} | {'Moyenne':<10} | {'Médiane':<10} | {'Écart-type':<12} | {'Nbs Comptés':<12}"
        print("-" * len(header_num))
        print(header_num)
        print("-" * len(header_num))

        for key in sorted(stats_numeriques.keys()):
            values = stats_numeriques[key]
            if not values: continue

            count = len(values)
            minimum = min(values)
            maximum = max(values)
            moyenne = statistics.mean(values)
            mediane = statistics.median(values)

            try:
                ecart_type = statistics.stdev(values)
            except statistics.StatisticsError:
                ecart_type = float('nan')

            print(
                f"{key:<20} | {minimum:<10.2f} | {maximum:<10.2f} | {moyenne:<10.2f} | {mediane:<10.2f} | {ecart_type:<12.2f} | {count:<12}")

        print("-" * len(header_num))

    # --- PARTIE J6 : ANALYSE DE STRUCTURE ET MODE ---
    print("\n--- Analyse de la Structure des Données et Mode (Tous Types) ---")

    if not structure_types:
        print("Aucun enregistrement ou colonne trouvé pour l'analyse.")
    else:
        types_disponibles = ['int', 'float', 'bool', 'str', 'None', 'list', 'dict', 'autres']

        header_types = f"{'Colonne':<20} | " + " | ".join(
            f"{t:<6}" for t in types_disponibles) + " | Mode (Plus Fréquent)"
        print("-" * len(header_types))
        print(header_types)
        print("-" * len(header_types))

        for key in sorted(structure_types.keys()):
            output = f"{key:<20} | "

            all_values = mode_results[key]
            mode_counter = Counter(all_values)

            try:
                most_common = mode_counter.most_common(1)

                if most_common and most_common[0][1] > 0:
                    mode_value = most_common[0][0]
                    mode_count = most_common[0][1]

                    if mode_value is None:
                        mode_display = f"None ({mode_count})"
                    elif isinstance(mode_value, str) and len(mode_value) > 20:
                        mode_display = f"'{mode_value[:17]}...' ({mode_count})"
                    else:
                        mode_display = f"'{repr(mode_value)}' ({mode_count})"
                else:
                    mode_display = "N/A"

            except Exception:
                mode_display = "Erreur Mode"

            for type_name in types_disponibles:
                count = structure_types[key].get(type_name, 0)
                output += f"{count:<6} | "

            output += mode_display

            print(output)

        print("-" * len(header_types))

    input("Appuyez sur Entrée pour continuer...")


def gerer_filtrage(data: DataList) -> DataList:
    """(J7) Gère le sous-menu de filtrage simple."""
    print("\n" + "-" * 50)
    print("          SOUS-MENU FILTRAGE SIMPLE (J7)")
    print("-" * 50)

    if not data:
        print("Veuillez d'abord charger les données.")
        input("Appuyez sur Entrée pour continuer...")
        return data

    headers = get_all_headers(data)

    print("Colonnes disponibles pour le filtrage :")
    for i, header in enumerate(headers, 1):
        print(f"{i}. {header}")

    print("-" * 50)
    print("0. Annuler et Retour au Menu Principal")

    # --- Étape 1 : Choix de la Colonne ---
    try:
        choix_colonne = input("Choisissez le numéro de la colonne à filtrer (ou 0 pour annuler) : ").strip()
        if choix_colonne == '0':
            return data

        index_colonne = int(choix_colonne) - 1
        if not (0 <= index_colonne < len(headers)):
            print("Choix de colonne invalide.")
            input("Appuyez sur Entrée pour continuer...")
            return data

        cle_filtre = headers[index_colonne]
    except ValueError:
        print("Entrée invalide. Veuillez entrer un numéro.")
        input("Appuyez sur Entrée pour continuer...")
        return data

    # --- Étape 2 : Choix de l'Opérateur ---
    operateurs = {
        '1': '=',
        '2': '!=',
        '3': '>',
        '4': '<',
        '5': '>=',
        '6': '<=',
        '7': 'contient (texte)',
        '8': 'commence par (texte)',
    }

    print(f"\nOpérateurs disponibles pour la colonne '{cle_filtre}' :")
    for num, op in operateurs.items():
        print(f"{num}. {op}")

    choix_op = input("Choisissez le numéro de l'opérateur : ").strip()
    if choix_op not in operateurs:
        print("Opérateur invalide.")
        input("Appuyez sur Entrée pour continuer...")
        return data

    operateur = operateurs[choix_op]

    # --- Étape 3 : Saisie de la Valeur Cible ---
    valeur_cible_str = input(f"Entrez la valeur cible pour l'opération '{operateur}' : ").strip()

    valeur_cible_convertie = convertir_type(valeur_cible_str)

    print(f"\nApplication du filtre : {cle_filtre} {operateur} {repr(valeur_cible_convertie)}...")

    # --- Étape 4 : Application du Filtre ---
    donnees_filtrees = []
    nb_total = len(data)

    is_text_operator = operateur in ('contient (texte)', 'commence par (texte)')

    for item in data:
        valeur_item = item.get(cle_filtre)
        match = False

        try:
            # Opérateurs numériques et d'égalité
            if operateur == '=':
                match = (valeur_item == valeur_cible_convertie)

            elif operateur == '!=':
                match = (valeur_item != valeur_cible_convertie)

            elif operateur in ('>', '<', '>=', '<='):
                if isinstance(valeur_item, (int, float)) and isinstance(valeur_cible_convertie, (int, float)):
                    if operateur == '>':
                        match = (valeur_item > valeur_cible_convertie)
                    elif operateur == '<':
                        match = (valeur_item < valeur_cible_convertie)
                    elif operateur == '>=':
                        match = (valeur_item >= valeur_cible_convertie)
                    elif operateur == '<=':
                        match = (valeur_item <= valeur_cible_convertie)

            # Opérateurs de texte (recherche)
            elif is_text_operator:
                if isinstance(valeur_item, str):
                    cible_lower = valeur_cible_str.lower()
                    item_lower = valeur_item.lower()

                    if operateur == 'contient (texte)':
                        match = cible_lower in item_lower
                    elif operateur == 'commence par (texte)':
                        match = item_lower.startswith(cible_lower)

        except Exception:
            pass

        if match:
            donnees_filtrees.append(item)

    # --- Étape 5 : Résultat et Retour ---
    nb_filtre = len(donnees_filtrees)
    print(f"\nFiltre appliqué avec succès : {nb_filtre} enregistrement(s) conservé(s) sur {nb_total}.")

    if nb_filtre == 0:
        print("Aucun enregistrement ne correspond au critère de filtrage.")
        input("Appuyez sur Entrée pour continuer...")
        return data

    print("Les données ont été mises à jour avec le résultat du filtre.")
    input("Appuyez sur Entrée pour continuer...")
    return donnees_filtrees


def gerer_tri(data: DataList) -> DataList:
    """(J8) Gère le sous-menu de tri multicritère."""
    if not data:
        print("\n[SOUS-MENU TRI] Veuillez d'abord charger les données.")
        input("Appuyez sur Entrée pour continuer...")
        return data

    headers = get_all_headers(data)

    # Liste de tuples pour stocker les critères: [(clé_colonne, reverse_bool), ...]
    critere_tri: List[Tuple[str, bool]] = []

    while True:
        print("\n" + "-" * 50)
        print("          SOUS-MENU TRI (J8 - Multicritère et Linguistique)")

        # Afficher les critères déjà sélectionnés
        if critere_tri:
            print(f"Critères actuels ({len(critere_tri)}) :")
            for i, (cle, reverse) in enumerate(critere_tri, 1):
                direction = "DESC" if reverse else "ASC"
                print(f"  {i}. {cle} ({direction})")
            print("-" * 50)

        # Afficher les colonnes disponibles avec index
        print("Colonnes disponibles :")
        for i, header in enumerate(headers, 1):
            print(f"{i}. {header}")

        print("-" * 50)
        print("A. Ajouter un critère de tri (Niveau supérieur)")
        print("E. Exécuter le tri")
        print("0. Annuler et Retour au Menu Principal")
        print("-" * 50)

        choix_action = input("Votre choix (A, E, ou 0) : ").strip().upper()

        if choix_action == '0':
            return data

        if choix_action == 'E':
            if not critere_tri:
                print("Veuillez ajouter au moins un critère avant d'exécuter.")
                continue
            break  # Sortir de la boucle pour exécuter le tri

        if choix_action == 'A':
            # 1. Choix de la colonne
            choix_colonne = input("Choisissez le NUMÉRO de la colonne à ajouter : ").strip()
            try:
                index_colonne = int(choix_colonne) - 1
                if 0 <= index_colonne < len(headers):
                    cle_tri = headers[index_colonne]
                else:
                    print("Choix de colonne invalide.")
                    continue
            except ValueError:
                print("Entrée invalide. Veuillez entrer un numéro.")
                continue

            # 2. Choix de l'ordre
            choix_ordre = input(
                f"Sens du tri pour '{cle_tri}' (a/A pour Ascendant, d/D pour Descendant) : ").strip().lower()
            if choix_ordre not in ('a', 'd'):
                print("Ordre de tri invalide. Utilisez 'a' ou 'd'.")
                continue

            reverse_sort = (choix_ordre == 'd')

            # Ajout du critère à la liste
            critere_tri.append((cle_tri, reverse_sort))
            print(f"Critère '{cle_tri}' ajouté comme niveau {len(critere_tri)}.")

        else:
            print("Action invalide.")
            continue

    # --- Exécution du Tri Multicritère ---
    print(f"\nExécution du tri sur {len(critere_tri)} critère(s)...")

    # 1. Configuration de la locale pour le tri linguistique (si possible)
    use_locale_sort = False
    try:
        # Tenter de définir la locale pour un tri linguistique correct
        locale.setlocale(locale.LC_COLLATE, 'fr_FR.UTF-8')
        use_locale_sort = True
        print("Note: Tri linguistique (français) activé.")
    except locale.Error:
        try:
            locale.setlocale(locale.LC_COLLATE, 'fr_FR')
            use_locale_sort = True
            print("Note: Tri linguistique (français) activé (locale générique).")
        except locale.Error:
            use_locale_sort = False
            print("AVERTISSEMENT: Locale 'fr' non disponible. Retour au tri par défaut (Unicode).")
            locale.setlocale(locale.LC_COLLATE, 'C')

    # 2. Tri stable par critère (du moins important au plus important)
    # On commence avec une copie de la liste pour ne pas modifier l'originale
    data_triee = list(data)

    # Parcourir les critères en ordre INVERSE (du dernier critère au premier)
    # critere_tri[0] est le critère Primaire, critere_tri[-1] est le Dernier critère
    for cle_tri, reverse_sort in reversed(critere_tri):

        # Définition de la fonction clé pour la colonne actuelle
        def tri_key_multi(item):
            value = item.get(cle_tri)

            # La logique de tri par rang et type est cruciale pour la stabilité
            if isinstance(value, (int, float)):
                # Rang 0 : Numérique
                return (0, value)
            if isinstance(value, bool):
                # Rang 1 : Booléen
                return (1, value)
            if isinstance(value, str):
                # Rang 2 : Chaîne (avec tri linguistique si possible)
                if use_locale_sort:
                    return (2, locale.strxfrm(value))
                else:
                    return (2, value)
            if value is None:
                # Rang 3 : None (toujours à la fin)
                return (3, 0)

            # Rang 4 : Types complexes
            return (4, str(value))

        # Appliquer le tri sur le résultat du tri précédent.
        # Python's sorted() est stable, ce qui préserve l'ordre des éléments égaux.
        data_triee = sorted(data_triee, key=tri_key_multi, reverse=reverse_sort)

    print("Tri multicritère terminé. Les données ont été mises à jour.")
    input("Appuyez sur Entrée pour continuer...")
    return data_triee


def gerer_historique(data: DataList) -> DataList:
    """(J12) Gère les opérations Undo/Redo."""
    print("\n[HISTORIQUE - UNDO/REDO]")
    print("Fonctionnalité en cours de développement (J12).")
    input("Appuyez sur Entrée pour continuer...")
    return data


def gerer_champs(data: DataList) -> DataList:
    """(J12) Gère l'ajout ou le retrait de champs."""
    print("\n[GESTION DES CHAMPS]")
    if not data:
        print("Veuillez d'abord charger les données.")
        return data
    print("Fonctionnalité en cours de développement (J12).")
    input("Appuyez sur Entrée pour continuer...")
    return data


# --- BOUCLE PRINCIPALE DE L'APPLICATION ---

def main():
    data: DataList = []

    while True:
        # Affichage de l'état actuel des données
        etat = f"{len(data)} enregistrement(s)" if data else "Aucune donnée chargée"

        print("\n" + "=" * 50)
        print("          PROJET DATA FILTER - Menu Principal")
        print(f"          [État actuel : {etat}]")
        print("=" * 50)
        print("1. Charger les Données (CSV, JSON, YAML, XML) [J9 OK]")
        print("2. Afficher les Données (Aperçu)")
        print("3. Statistiques & Analyse de Structure (J6 - Complet)")
        print("4. Filtrage (J7 - Simple)")
        print("5. Tri (J8 - Multicritère)")
        print("6. Sauvegarder les Données (CSV, JSON, YAML, XML) [J9 OK]")
        print("-" * 50)
        print("7. Historique (Undo/Redo)")
        print("8. Gestion des Champs (Ajouter/Retirer)")
        print("0. Quitter")
        print("=" * 50)

        choix = input("Votre choix : ").strip()

        if choix == '1':
            new_data = charger_donnees()
            if new_data:
                data = new_data
                print(f"\nChargement terminé. {len(data)} enregistrement(s) prêts.")
        elif choix == '2':
            afficher_donnees(data)
        elif choix == '3':
            afficher_statistiques(data)
        elif choix == '4':
            data = gerer_filtrage(data)
        elif choix == '5':
            data = gerer_tri(data)
        elif choix == '6':
            sauvegarder_donnees(data)
        elif choix == '7':
            data = gerer_historique(data)
        elif choix == '8':
            data = gerer_champs(data)
        elif choix == '0':
            print("Merci d'avoir utilisé Data Filter. Au revoir!")
            sys.exit(0)
        else:
            print("Choix invalide. Veuillez entrer un numéro de 0 à 8.")


if __name__ == "__main__":
    main()