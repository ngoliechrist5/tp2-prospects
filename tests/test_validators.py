from datetime import date, timedelta
from app.validators import (
    valider_nom_prenom,
    valider_date_naissance,
    valider_email,
    valider_telephone,
    valider_secteur_activite,
)


# --- Nom / Prénom ---

def test_nom_valide():
    assert valider_nom_prenom("Ongandja") is None

def test_nom_trop_court_rejete():
    assert valider_nom_prenom("O") is not None

def test_nom_avec_chiffres_rejete():
    assert valider_nom_prenom("Kim123") is not None

def test_nom_vide_rejete():
    assert valider_nom_prenom("") is not None


# --- Date de naissance ---

def test_date_naissance_valide_majeur():
    date_valide = date.today() - timedelta(days=20*365)
    assert valider_date_naissance(date_valide) is None

def test_date_naissance_future_rejetee():
    date_future = date.today() + timedelta(days=1)
    assert valider_date_naissance(date_future) is not None

def test_date_naissance_mineur_rejetee():
    date_mineur = date.today() - timedelta(days=10*365)
    assert valider_date_naissance(date_mineur) is not None


# --- Email ---

def test_email_valide():
    assert valider_email("kim.ongandja@arcep.ga") is None

def test_email_sans_arobase_rejete():
    assert valider_email("kim.ongandjaarcep.ga") is not None

def test_email_vide_rejete():
    assert valider_email("") is not None


# --- Téléphone ---

def test_telephone_gabon_valide():
    assert valider_telephone("+241 74 12 34 56") is None

def test_telephone_international_valide():
    assert valider_telephone("+33612345678") is None

def test_telephone_invalide_rejete():
    assert valider_telephone("0612345") is not None

def test_telephone_vide_rejete():
    assert valider_telephone("") is not None


# --- Secteur d'activité ---

def test_secteur_valide():
    assert valider_secteur_activite("Banque/Finance") is None

def test_secteur_invalide_rejete():
    assert valider_secteur_activite("Secteur inexistant") is not None