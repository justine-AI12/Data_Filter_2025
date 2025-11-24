import sys


# --- FONCTIONS STUBS (À implémenter aux Jours suivants) ---

def charger_donnees():
    """Gère le sous-menu pour le chargement des données (J2/J9)."""
    print("\n[SOUS-MENU CHARGEMENT]")
    print("Fonctionnalité en cours de développement (J2).")
    input("Appuyez sur Entrée pour continuer...")
    # Ici, nous aurons la logique pour choisir CSV, JSON, YAML, XML


def afficher_donnees(data):
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
        print(" | ".join(header))
        print("-" * 50)

        # Afficher les données
        for i, row in enumerate(data):
            if i >= lignes_a_afficher:
                break
            # Convertir les valeurs en chaînes pour l'affichage
            display_values = [str(row.get(col, '')) for col in header]
            print(" | ".join(display_values))

        if len(data) > lignes_a_afficher:
            print(f"... ({len(data) - lignes_a_afficher} autres enregistrements)")

    except IndexError:
        print("Les données sont chargées mais la structure est vide ou incorrecte.")
    input("\nAppuyez sur Entrée pour continuer...")


def afficher_statistiques(data):
    """(J5/J6) Calcule et affiche les statistiques."""
    print("\n[STATISTIQUES ET STRUCTURE]")
    if not data:
        print("Veuillez d'abord charger les données.")
        return
    print("Fonctionnalité en cours de développement (J5/J6).")
    input("Appuyez sur Entrée pour continuer...")


def gerer_filtrage(data):
    """(J7/J8/J11) Gère le sous-menu de filtrage."""
    print("\n[SOUS-MENU FILTRAGE]")
    if not data:
        print("Veuillez d'abord charger les données.")
        return
    print("Fonctionnalité en cours de développement (J7/J8/J11).")
    input("Appuyez sur Entrée pour continuer...")
    return data  # Retourne les données filtrées (ou inchangées)


def gerer_tri(data):
    """(J4/J10) Gère le sous-menu de tri."""
    print("\n[SOUS-MENU TRI]")
    if not data:
        print("Veuillez d'abord charger les données.")
        return
    print("Fonctionnalité en cours de développement (J4/J10).")
    input("Appuyez sur Entrée pour continuer...")
    return data  # Retourne les données triées (ou inchangées)


def sauvegarder_donnees(data):
    """(J3/J9) Gère le sous-menu de sauvegarde."""
    print("\n[SOUS-MENU SAUVEGARDE]")
    if not data:
        print("Veuillez d'abord charger les données.")
        return
    print("Fonctionnalité en cours de développement (J3/J9).")
    # Ici, nous aurons la logique pour choisir le format de sortie
    input("Appuyez sur Entrée pour continuer...")


def gerer_historique(data):
    """(J12) Gère les opérations Undo/Redo."""
    print("\n[HISTORIQUE - UNDO/REDO]")
    print("Fonctionnalité en cours de développement (J12).")
    input("Appuyez sur Entrée pour continuer...")
    return data


def gerer_champs(data):
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
    # Liste pour stocker les données (liste de dictionnaires)
    # Nous allons la pré-remplir avec des données de test pour le J1
    data = [
        {'firstname': 'Alice', 'lastname': 'Martin', 'age': '20', 'price': '99.99', 'apprentice': 'True'},
        {'firstname': 'Bob', 'lastname': 'Dupont', 'age': '22', 'price': '450.00', 'apprentice': 'False'},
        {'firstname': 'Charlie', 'lastname': 'Leblanc', 'age': '19', 'price': '15.00', 'apprentice': 'True'},
    ]

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
        print("3. Statistiques & Structure (Min/Max/Moyenne)")
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
            charger_donnees()
        elif choix == '2':
            afficher_donnees(data)
        elif choix == '3':
            afficher_statistiques(data)
        elif choix == '4':
            data = gerer_filtrage(data)  # On met à jour 'data' avec le résultat du filtrage
        elif choix == '5':
            data = gerer_tri(data)  # On met à jour 'data' avec le résultat du tri
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