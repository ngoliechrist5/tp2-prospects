import re
from datetime import date

# Référentiel fermé des secteurs d'activité (à adapter selon ton contexte)
SECTEURS_AUTORISES = [
    "Banque/Finance", "Télécommunications", "Administration publique",
    "Commerce", "Éducation", "Santé", "Industrie", "Agriculture", "Autre"
]

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
TELEPHONE_GABON_REGEX = re.compile(r'^\+241\s?\d{2}\s?\d{2}\s?\d{2}\s?\d{2}$')
TELEPHONE_INTL_REGEX = re.compile(r'^\+\d{7,15}$')


def valider_nom_prenom(valeur, nom_champ="nom"):
    """Règle : obligatoire, alphabétique, au moins 2 caractères"""
    if not valeur or len(valeur.strip()) < 2:
        return f"Le {nom_champ} est obligatoire et doit contenir au moins 2 caractères."
    if not valeur.replace(" ", "").replace("-", "").isalpha():
        return f"Le {nom_champ} ne doit contenir que des lettres."
    return None


def valider_date_naissance(date_naissance):
    """Règle : non future, majorité 18 ans révolus"""
    if date_naissance > date.today():
        return "La date de naissance ne peut pas être dans le futur."

    age = date.today().year - date_naissance.year - (
        (date.today().month, date.today().day) < (date_naissance.month, date_naissance.day)
    )
    if age < 18:
        return "Le prospect doit être majeur (18 ans révolus)."
    return None


def valider_email(email):
    """Règle : format conforme (l'unicité est vérifiée séparément en base)"""
    if not email or not EMAIL_REGEX.match(email):
        return "L'adresse e-mail n'est pas valide."
    return None


def valider_telephone(telephone):
    """Règle : format Gabon (+241 XX XX XX XX) ou format international valide"""
    if not telephone:
        return "Le numéro de téléphone est obligatoire."
    telephone_nettoye = telephone.replace(" ", "")
    if TELEPHONE_GABON_REGEX.match(telephone) or TELEPHONE_INTL_REGEX.match(telephone_nettoye):
        return None
    return "Le téléphone doit être au format Gabon (+241 XX XX XX XX) ou international valide."


def valider_secteur_activite(secteur):
    """Règle : appartient à une liste fermée"""
    if secteur not in SECTEURS_AUTORISES:
        return f"Le secteur d'activité doit être l'un des suivants : {', '.join(SECTEURS_AUTORISES)}."
    return None


def valider_prospect(data):
    """Fonction centrale : valide toutes les règles, retourne une liste d'erreurs"""
    erreurs = []

    err = valider_nom_prenom(data.get('nom'), "nom")
    if err:
        erreurs.append(err)

    err = valider_nom_prenom(data.get('prenom'), "prénom")
    if err:
        erreurs.append(err)

    err = valider_email(data.get('email'))
    if err:
        erreurs.append(err)

    err = valider_telephone(data.get('telephone'))
    if err:
        erreurs.append(err)

    err = valider_secteur_activite(data.get('secteur_activite'))
    if err:
        erreurs.append(err)

    return erreurs
