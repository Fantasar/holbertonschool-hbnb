"""
Ce fichier définit le repository spécifique pour le modèle Review,
héritant d'une classe générique SQLAlchemyRepository.

Il contient des méthodes pour gérer l'ajout, la sauvegarde et la récupération
d'objets Review en base de données via SQLAlchemy,
fournissant ainsi une couche d'abstraction facilitant la gestion des données.
"""
from app.models.review import Review
from app.extensions import db
from app.persistence.repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

class BaseRepository:
    def add(self, obj):
        db.session.add(obj)
        db.session.commit()  # Sauvegarder immédiatement
        return obj

    def save(self, obj):
        db.session.commit()  # Sauvegarder les modifications
        return obj
