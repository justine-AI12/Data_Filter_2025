import sys
import csv
import json
from typing import List, Dict, Any
from collections import Counter

# Alias de type pour clarifier la structure des données internes
DataList = List[Dict[str, Any]]


# --- FONCTIONS UTILITAIRES POUR LA ROBUSTESSE (J2) ---

def convertir_type(value: Any) -> Any:
    """
    Tente de convertir une chaîne de caractères en int, float ou booléen.

    Correction J4: Convertit les chaînes vides et les indicateurs N/A communs
    en 'None' pour assurer leur placement correct (à la fin) lors du tri.
    """

    # 1. Gérer les valeurs déjà converties par JSON (int, float, bool, list) et None
    if value is None:
        return None  # Retourne None directement (pour les 'null' JSON)

    if isinstance(value, (int, float, bool, list)):
        return value

    # Si ce n'est pas None et ce n'est pas un type primitif, il DOIT être une chaîne
    if not isinstance(value, str):
        # Devrait seulement arriver si on a un objet complexe (dict/set) ici, on le retourne
        return value

    # À partir d'ici, 'value' est garanti être une chaîne (str)

    # Nettoyage et identification des valeurs manquantes (pour CSV/non-JSON)
    lower_value = value.strip().lower()

    # NOUVEAU: Traiter les chaînes vides ou les placeholders comme None (va au Rang 3 lors du tri)
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
        # L'appel à convertir_type gère maintenant les None
        nettoye = {k: convertir_type(v) for k, v in item.items()}
        donnees_nettoyees.append(nettoye)
    return donnees_nettoyees


# --- FONCTIONS DE CHARGEMENT (J2) ---

def load_json(filepath: str) -> DataList:
    """Charge les données depuis un fichier JSON."""
    with open(filepath, 'r', encoding='utf-8') as f:
        # json.load() lit directement l'objet JSON (liste ou dict)
        raw_data = json.load(f)

    # Si les données sont lues directement comme une liste de dict, on nettoie
    if isinstance(raw_data, list):
        print(f"Succès : {len(raw_data)} enregistrements JSON chargés.")
        return nettoyer_donnees(raw_data)
    else:
        # Gérer le cas où le JSON est un objet racine (ex: {"inventaire": [...]})
        raise ValueError("Format JSON invalide : La racine doit être une liste d'enregistrements.")


def load_csv(filepath: str) -> DataList:
    """Charge les données depuis un fichier CSV."""
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        # DictReader lit chaque ligne comme un dictionnaire (clé = en-tête)
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    print(f"Succès : {len(data)} enregistrements CSV chargés.")
    # Le nettoyage est essentiel pour CSV car toutes les valeurs sont des chaînes au départ
    return nettoyer_donnees(data)


def charger_donnees() -> DataList:
    """Gère le sous-menu pour le chargement des données (J2/J9)."""
    while True:
        print("\n" + "-" * 50)
        print("          SOUS-MENU CHARGEMENT")
        print("          Format(s) supporté(s) : 1, 2 (J2)")
        print("-" * 50)
        print("1. Charger un fichier CSV")
        print("2. Charger un fichier JSON")
        print("3. Charger un fichier YAML (J9 - Avancé)")
        print("4. Charger un fichier XML (J9 - Avancé)")
        print("0. Annuler et Retour au Menu Principal")
        print("-" * 50)

        choix = input("Votre choix de format : ").strip()

        if choix == '0':
            return []  # Retourne une liste vide pour indiquer qu'aucune donnée n'a été chargée

        if choix in ('1', '2'):
            filepath = input("Entrez le chemin du fichier : ").strip()
            if not filepath:
                print("Chemin du fichier non valide.")
                continue

            try:
                if choix == '1':
                    return load_csv(filepath)
                elif choix == '2':
                    return load_json(filepath)
            except FileNotFoundError:
                print(f"Erreur : Le fichier à l'emplacement '{filepath}' n'a pas été trouvé.")
            except Exception as e:
                # Afficher le type d'erreur pour aider au débogage
                print(f"Erreur lors du chargement ou du traitement du fichier ({type(e).__name__}): {e}")

        elif choix in ('3', '4'):
            print("Fonctionnalité YAML/XML sera implémentée au Jour 9 (Avancé).")
        else:
            print("Choix invalide.")

        input("Appuyez sur Entrée pour continuer...")


# --- FONCTIONS DE SAUVEGARDE (J3) ---

def get_all_headers(data: DataList) -> List[str]:
    """
    Récupère l'ensemble des clés (en-têtes) présentes dans toutes les lignes de données.
    Ceci est essentiel pour créer le header du CSV.
    """
    headers = set()
    for row in data:
        headers.update(row.keys())

    # Retourne les en-têtes dans un ordre stable pour la lisibilité
    if data:
        # Utiliser l'ordre de la première ligne comme base
        ordered_headers = list(data[0].keys())
        # Ajouter les autres en-têtes triés alphabétiquement
        for h in sorted(list(headers - set(ordered_headers))):
            ordered_headers.append(h)
        return ordered_headers

    return list(sorted(list(headers)))


def save_json(data: DataList, filepath: str):
    """Sauvegarde les données au format JSON."""
    # Note: json.dump gère automatiquement les types Python (int, float, bool, None)
    with open(filepath, 'w', encoding='utf-8') as f:
        # Utilisation de indent=4 pour une meilleure lisibilité du fichier sauvegardé
        json.dump(data, f, indent=4)
    print(f"Succès : {len(data)} enregistrements sauvegardés au format JSON dans '{filepath}'.")


def save_csv(data: DataList, filepath: str):
    """Sauvegarde les données au format CSV."""
    if not data:
        raise ValueError("Impossible de sauvegarder : la liste de données est vide.")

    # 1. Récupérer tous les en-têtes possibles
    headers = get_all_headers(data)

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        # Utilisation de DictWriter pour écrire les dictionnaires
        # fieldnames = l'ordre des colonnes ; extrasaction='ignore' ignore les clés non spécifiées dans headers
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')

        # Écrire l'en-tête (la première ligne du CSV)
        writer.writeheader()

        # Écrire les lignes de données
        # Les valeurs None (null) seront écrites comme des chaînes vides par défaut
        writer.writerows(data)

    print(f"Succès : {len(data)} enregistrements sauvegardés au format CSV dans '{filepath}'.")


def sauvegarder_donnees(data: DataList):
    """(J3/J9) Gère le sous-menu de sauvegarde."""
    if not data:
        print("\n[SOUS-MENU SAUVEGARDE] Aucune donnée à sauvegarder.")
        input("Appuyez sur Entrée pour continuer...")
        return

    while True:
        print("\n" + "-" * 50)
        print("          SOUS-MENU SAUVEGARDE")
        print("          Format(s) supporté(s) : 1, 2 (J3)")
        print("-" * 50)
        print("1. Sauvegarder en CSV")
        print("2. Sauvegarder en JSON")
        print("3. Sauvegarder en YAML (J9 - Avancé)")
        print("4. Sauvegarder en XML (J9 - Avancé)")
        print("0. Annuler et Retour au Menu Principal")
        print("-" * 50)

        choix = input("Votre choix de format : ").strip()

        if choix == '0':
            return  # Retour au menu principal

        if choix in ('1', '2'):
            filepath = input("Entrez le chemin du fichier de sortie : ").strip()
            if not filepath:
                print("Chemin du fichier non valide.")
                continue

            try:
                if choix == '1':
                    save_csv(data, filepath)
                elif choix == '2':
                    save_json(data, filepath)
                # Sortir de la boucle de sauvegarde après succès
                input("Sauvegarde terminée. Appuyez sur Entrée pour continuer...")
                return
            except Exception as e:
                print(f"Erreur lors de la sauvegarde du fichier ({type(e).__name__}): {e}")

        elif choix in ('3', '4'):
            print("Fonctionnalité YAML/XML sera implémentée au Jour 9 (Avancé).")
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

    # Afficher les 5 premières lignes pour la démo
    lignes_a_afficher = 5
    print("-" * 50)

    # Afficher l'en-tête (les clés du premier dictionnaire)
    try:
        header = list(data[0].keys())
        # Afficher la ligne d'en-tête
        print(" | ".join(header))
        print("-" * 50)

        # Afficher les données
        for i, row in enumerate(data):
            if i >= lignes_a_afficher:
                break
            # Utilisation de repr() pour bien afficher les types (True/False/Nombres)
            display_values = [repr(row.get(col, '')) for col in header]
            print(" | ".join(display_values))

        if len(data) > lignes_a_afficher:
            print(f"... ({len(data) - lignes_a_afficher} autres enregistrements)")

    except IndexError:
        print("Les données sont chargées mais la structure est vide ou incorrecte.")
    input("\nAppuyez sur Entrée pour continuer...")


def afficher_statistiques(data: DataList):
    """
    (J5/Début J6) Calcule et affiche les statistiques (Min/Max/Moyenne)
    et la distribution des types pour chaque colonne.
    """
    print("\n[STATISTIQUES ET ANALYSE DE STRUCTURE]")
    if not data:
        print("Veuillez d'abord charger les données.")
        input("Appuyez sur Entrée pour continuer...")
        return

    stats_numeriques: Dict[str, List[float]] = {}
    structure_types: Dict[str, Counter] = {}

    # 1. Collecter les valeurs numériques et les types pour chaque colonne
    for item in data:
        for key, value in item.items():

            # Initialisation pour la colonne
            if key not in structure_types:
                structure_types[key] = Counter()

            # Enregistrement des types pour l'analyse de structure (J6)
            if value is None:
                structure_types[key]['None'] += 1
            elif isinstance(value, bool):
                structure_types[key]['bool'] += 1
            elif isinstance(value, int):
                structure_types[key]['int'] += 1
            elif isinstance(value, float):
                structure_types[key]['float'] += 1
            elif isinstance(value, str):
                structure_types[key]['str'] += 1
            else:
                # Pour les listes, dicts, etc.
                structure_types[key]['autres'] += 1

            # Collection pour les statistiques numériques (J5)
            if isinstance(value, (int, float)):
                if key not in stats_numeriques:
                    stats_numeriques[key] = []
                stats_numeriques[key].append(float(value))

                # --- PARTIE J5 : STATISTIQUES NUMÉRIQUES DE BASE (Min/Max/Moyenne) ---
    print("\n--- Statistiques Min/Max/Moyenne (Colonnes Numériques) ---")

    if not stats_numeriques:
        print("Aucune colonne purement numérique (int ou float) n'a été trouvée pour cette analyse.")
    else:
        print("-" * 75)
        # 75 = 20 (col) + 3*10 (min/max/moy) + 15 (compte) + 4*2 (séparateurs)
        print(f"{'Colonne':<20} | {'Min':<10} | {'Max':<10} | {'Moyenne':<10} | {'Nombres comptés':<15}")
        print("-" * 75)

        # Calculer et afficher les statistiques
        for key in sorted(stats_numeriques.keys()):
            values = stats_numeriques[key]
            if not values: continue

            count = len(values)
            minimum = min(values)
            maximum = max(values)
            moyenne = sum(values) / count

            # Afficher les résultats avec une précision de 2 décimales pour les flottants
            print(f"{key:<20} | {minimum:<10.2f} | {maximum:<10.2f} | {moyenne:<10.2f} | {count:<15}")

        print("-" * 75)

    # --- PARTIE DÉBUT J6 : ANALYSE DE STRUCTURE ET TYPES ---
    print("\n--- Analyse de la Structure des Données (Distribution des Types) ---")

    if not structure_types:
        print("Aucun enregistrement ou colonne trouvé pour l'analyse.")
    else:
        # Définir l'ordre des types pour un affichage cohérent
        types_disponibles = ['int', 'float', 'bool', 'str', 'None', 'autres']

        # Déterminer la largeur d'affichage
        header_line = f"{'Colonne':<20} | " + " | ".join(f"{t:<10}" for t in types_disponibles)
        print("-" * len(header_line))
        print(header_line)
        print("-" * len(header_line))

        # Afficher la distribution pour chaque colonne
        for key in sorted(structure_types.keys()):
            output = f"{key:<20} | "
            total_count = sum(structure_types[key].values())

            for type_name in types_disponibles:
                count = structure_types[key].get(type_name, 0)
                # Afficher le compte ou le pourcentage si on voulait plus de détail
                output += f"{count:<10} | "

            print(output.strip(" | "))

        print("-" * len(header_line))

    print("\n[NOTE] La colonne 'note_list' est principalement (ou totalement) de type 'str'.")
    print("Pour inclure ses valeurs numériques dans les statistiques, une fonction d'extraction/conversion")
    print("de listes depuis une chaîne sera nécessaire (Fonctionnalité Avancée).")
    input("Appuyez sur Entrée pour continuer...")


def gerer_filtrage(data: DataList) -> DataList:
    """(J7/J8/J11) Gère le sous-menu de filtrage."""
    print("\n[SOUS-MENU FILTRAGE]")
    if not data:
        print("Veuillez d'abord charger les données.")
        return
    print("Fonctionnalité en cours de développement (J7/J8/J11).")
    input("Appuyez sur Entrée pour continuer...")
    return data  # Retourne les données filtrées (ou inchangées)


def gerer_tri(data: DataList) -> DataList:
    """(J4/J10) Gère le sous-menu de tri."""
    if not data:
        print("\n[SOUS-MENU TRI] Veuillez d'abord charger les données.")
        input("Appuyez sur Entrée pour continuer...")
        return data

    # Récupération des en-têtes disponibles pour le tri
    headers = get_all_headers(data)

    while True:
        print("\n" + "-" * 50)
        print("          SOUS-MENU TRI (J4 - Monocritère)")
        print("-" * 50)

        # Afficher les colonnes disponibles avec index
        print("Colonnes disponibles pour le tri :")
        for i, header in enumerate(headers, 1):
            print(f"{i}. {header}")

        print("-" * 50)
        print("0. Annuler et Retour au Menu Principal")

        # 1. Choix de la colonne
        choix_colonne = input("Choisissez le numéro de la colonne à trier (ou 0 pour annuler) : ").strip()
        if choix_colonne == '0':
            return data

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
        choix_ordre = input("Sens du tri (a/A pour Ascendant, d/D pour Descendant) : ").strip().lower()
        if choix_ordre not in ('a', 'd'):
            print("Ordre de tri invalide. Utilisez 'a' ou 'd'.")
            continue

        reverse_sort = (choix_ordre == 'd')

        # 3. Exécution du tri
        print(f"\nTri en cours sur la colonne '{cle_tri}' ({'Descendant' if reverse_sort else 'Ascendant'})...")

        try:
            # FONCTION CLÉ DE TRI AMÉLIORÉE (Gère les types incohérents et place None à la fin)
            def tri_key(item):
                value = item.get(cle_tri)

                # Assignation d'un rang pour gérer la comparaison de types incompatibles (str vs float)
                # L'ordre des rangs garantit que les types sont triés entre eux

                if isinstance(value, (int, float)):
                    # Rang 0 : Types numériques (triés en premier)
                    return (0, value)

                if isinstance(value, bool):
                    # Rang 1 : Types booléens
                    return (1, value)

                if isinstance(value, str):
                    # Rang 2 : Types chaîne (pour les noms, descriptions, etc.)
                    return (2, value)

                if value is None:
                    # Rang 3 : Toujours à la fin (grâce à la conversion des N/A et chaînes vides en None)
                    return (3, 0)

                # Rang 4 : Types complexes (listes, dictionnaires, etc.)
                return (4, str(value))

            # FIN DE LA FONCTION CLÉ DE TRI AMÉLIORÉE

            # Python's sorted() retourne une nouvelle liste triée
            data_triee = sorted(data, key=tri_key, reverse=reverse_sort)

            print("Tri terminé. Les données ont été mises à jour.")
            input("Appuyez sur Entrée pour continuer...")
            return data_triee

        except TypeError as e:
            # Cette erreur devrait maintenant être beaucoup plus rare
            print(f"Erreur de tri : Impossible de comparer les types de données dans la colonne '{cle_tri}'.")
            print(
                "Vérifiez que toutes les valeurs sont comparables (ex: pas de mélange de nombres et de chaînes complexes).")
            print(f"Détail de l'erreur: {e}")
            input("Appuyez sur Entrée pour continuer...")
            return data  # Retourne les données non triées en cas d'erreur
        except Exception as e:
            print(f"Une erreur inattendue est survenue lors du tri : {e}")
            input("Appuyez sur Entrée pour continuer...")
            return data


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
        return
    print("Fonctionnalité en cours de développement (J12).")
    input("Appuyez sur Entrée pour continuer...")
    return data


# --- BOUCLE PRINCIPALE DE L'APPLICATION ---

def main():
    # Suppression des données de test du J1. 'data' est initialement vide.
    data: DataList = []

    # Nous aurons besoin de l'historique au J12, mais on le prépare ici
    # historique = [] # Pile d'états de données pour Undo/Redo

    while True:
        # Affichage de l'état actuel des données
        etat = f"{len(data)} enregistrement(s)" if data else "Aucune donnée chargée"

        print("\n" + "=" * 50)
        print("          PROJET DATA FILTER - Menu Principal")
        print(f"          [État actuel : {etat}]")
        print("=" * 50)
        print("1. Charger les Données (CSV, JSON, YAML, XML)")
        print("2. Afficher les Données (Aperçu)")
        print("3. Statistiques & Analyse de Structure (J6 - Mediane/Mode/Distribution)")
        print("4. Filtrage (Critères simples et avancés)")
        print("5. Tri (Monocritère et Multi-critères)")
        print("6. Sauvegarder les Données (CSV, JSON, YAML, XML)")
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
            # Maintenant gère les stats de base (J5) et l'analyse de structure (début J6)
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