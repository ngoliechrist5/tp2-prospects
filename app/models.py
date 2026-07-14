from app import db
from datetime import datetime


class Prospect(db.Model):
    __tablename__ = 'prospects'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    lieu_naissance = db.Column(db.String(150), nullable=False)
    profession = db.Column(db.String(150), nullable=False)
    secteur_activite = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'date_naissance': self.date_naissance.isoformat(),
            'lieu_naissance': self.lieu_naissance,
            'profession': self.profession,
            'secteur_activite': self.secteur_activite,
            'telephone': self.telephone,
            'email': self.email,
            'date_creation': self.date_creation.isoformat()
        }
