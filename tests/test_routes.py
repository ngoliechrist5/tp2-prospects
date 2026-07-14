def test_creer_prospect_valide(client):
    reponse = client.post('/prospects', json={
        "nom": "Ongandja",
        "prenom": "Kim",
        "date_naissance": "2000-05-15",
        "lieu_naissance": "Libreville",
        "profession": "Ingénieur Système",
        "secteur_activite": "Télécommunications",
        "telephone": "+241 74 12 34 56",
        "email": "kim.test@arcep.ga"
    })
    assert reponse.status_code == 201
    assert reponse.get_json()["email"] == "kim.test@arcep.ga"


def test_creer_prospect_email_invalide(client):
    reponse = client.post('/prospects', json={
        "nom": "Ongandja",
        "prenom": "Kim",
        "date_naissance": "2000-05-15",
        "lieu_naissance": "Libreville",
        "profession": "Ingénieur",
        "secteur_activite": "Télécommunications",
        "telephone": "+241 74 12 34 56",
        "email": "email-invalide"
    })
    assert reponse.status_code == 400
    assert "erreurs" in reponse.get_json()


def test_creer_prospect_email_deja_existant(client):
    payload = {
        "nom": "Ongandja",
        "prenom": "Kim",
        "date_naissance": "2000-05-15",
        "lieu_naissance": "Libreville",
        "profession": "Ingénieur",
        "secteur_activite": "Télécommunications",
        "telephone": "+241 74 12 34 56",
        "email": "duplicate@arcep.ga"
    }
    premiere_reponse = client.post('/prospects', json=payload)
    assert premiere_reponse.status_code == 201

    deuxieme_reponse = client.post('/prospects', json=payload)
    assert deuxieme_reponse.status_code == 400
    assert "déjà enregistré" in str(deuxieme_reponse.get_json())


def test_creer_prospect_mineur_rejete(client):
    reponse = client.post('/prospects', json={
        "nom": "Ongandja",
        "prenom": "Kim",
        "date_naissance": "2015-05-15",  # mineur
        "lieu_naissance": "Libreville",
        "profession": "Étudiant",
        "secteur_activite": "Éducation",
        "telephone": "+241 74 12 34 56",
        "email": "mineur@arcep.ga"
    })
    assert reponse.status_code == 400


def test_lister_prospects_vide(client):
    reponse = client.get('/prospects')
    assert reponse.status_code == 200
    assert reponse.get_json() == []


def test_obtenir_prospect_inexistant(client):
    reponse = client.get('/prospects/999')
    assert reponse.status_code == 404


def test_supprimer_prospect(client):
    creation = client.post('/prospects', json={
        "nom": "Test",
        "prenom": "Suppr",
        "date_naissance": "1995-01-01",
        "lieu_naissance": "Libreville",
        "profession": "Test",
        "secteur_activite": "Autre",
        "telephone": "+241 60 00 00 00",
        "email": "suppr@arcep.ga"
    })
    prospect_id = creation.get_json()["id"]

    suppression = client.delete(f'/prospects/{prospect_id}')
    assert suppression.status_code == 200

    verification = client.get(f'/prospects/{prospect_id}')
    assert verification.status_code == 404