from flask import render_template
from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import Prospect
from app.validators import valider_prospect

prospects_bp = Blueprint('prospects', __name__)

@prospects_bp.route('/', methods=['GET'])
def afficher_formulaire():
    return render_template('index.html')

@prospects_bp.route('/prospects', methods=['POST'])
def creer_prospect():
    data = request.get_json()

    if not data:
        return jsonify({"erreurs": ["Corps de requête JSON manquant ou invalide."]}), 400

    # Étape 1 : validation de format (via validators.py)
    erreurs = valider_prospect(data)

    # Étape 2 : conversion et validation de la date de naissance
    try:
        date_naissance = datetime.strptime(data.get('date_naissance', ''), '%Y-%m-%d').date()
    except (ValueError, TypeError):
        erreurs.append("La date de naissance doit être au format AAAA-MM-JJ.")
        date_naissance = None

    if date_naissance:
        from app.validators import valider_date_naissance
        err = valider_date_naissance(date_naissance)
        if err:
            erreurs.append(err)

    # Étape 3 : validation d'unicité de l'e-mail (nécessite un accès base)
    if data.get('email') and Prospect.query.filter_by(email=data['email']).first():
        erreurs.append("Cet e-mail est déjà enregistré.")

    if erreurs:
        return jsonify({"erreurs": erreurs}), 400

    # Étape 4 : création en base
    nouveau_prospect = Prospect(
        nom=data['nom'],
        prenom=data['prenom'],
        date_naissance=date_naissance,
        lieu_naissance=data.get('lieu_naissance', ''),
        profession=data.get('profession', ''),
        secteur_activite=data['secteur_activite'],
        telephone=data['telephone'],
        email=data['email']
    )
    db.session.add(nouveau_prospect)
    db.session.commit()

    return jsonify(nouveau_prospect.to_dict()), 201


@prospects_bp.route('/prospects', methods=['GET'])
def lister_prospects():
    prospects = Prospect.query.all()
    return jsonify([p.to_dict() for p in prospects]), 200


@prospects_bp.route('/prospects/<int:prospect_id>', methods=['GET'])
def obtenir_prospect(prospect_id):
    prospect = Prospect.query.get(prospect_id)
    if not prospect:
        return jsonify({"erreur": "Prospect introuvable."}), 404
    return jsonify(prospect.to_dict()), 200


@prospects_bp.route('/prospects/<int:prospect_id>', methods=['PUT'])
def modifier_prospect(prospect_id):
    prospect = Prospect.query.get(prospect_id)
    if not prospect:
        return jsonify({"erreur": "Prospect introuvable."}), 404

    data = request.get_json()
    erreurs = valider_prospect(data)
    if erreurs:
        return jsonify({"erreurs": erreurs}), 400

    prospect.nom = data['nom']
    prospect.prenom = data['prenom']
    prospect.lieu_naissance = data.get('lieu_naissance', prospect.lieu_naissance)
    prospect.profession = data.get('profession', prospect.profession)
    prospect.secteur_activite = data['secteur_activite']
    prospect.telephone = data['telephone']
    prospect.email = data['email']

    db.session.commit()
    return jsonify(prospect.to_dict()), 200


@prospects_bp.route('/prospects/<int:prospect_id>', methods=['DELETE'])
def supprimer_prospect(prospect_id):
    prospect = Prospect.query.get(prospect_id)
    if not prospect:
        return jsonify({"erreur": "Prospect introuvable."}), 404

    db.session.delete(prospect)
    db.session.commit()
    return jsonify({"message": "Prospect supprimé avec succès."}), 200
