"""
Ce fichier définit le repository spécifique pour le modèle User,
héritant d'une classe générique SQLAlchemyRepository.

Il fournit une méthode supplémentaire pour récupérer un utilisateur
via son email unique, ainsi que les méthodes d'ajout et de sauvegarde
des objets User en base de données via SQLAlchemy.
"""
from app.models.user import User
from app.extensions import db
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

class BaseRepository:
    def add(self, obj):
        db.session.add(obj)
        db.session.commit()  # Sauvegarder immédiatement
        return obj

    def save(self, obj):
        db.session.commit()  # Sauvegarder les modifications
        return obj
