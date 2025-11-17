"""
Ce fichier définit le repository spécifique pour le modèle Amenity
en utilisant une classe générique SQLAlchemyRepository.

Il fournit des méthodes pour ajouter et sauvegarder des instances
d'Amenity dans la base de données via SQLAlchemy, encapsulant
ainsi la logique d'accès aux données et facilitant la maintenance.
"""
from app.models.amenity import Amenity
from app.extensions import db
from app.persistence.repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)
class BaseRepository:
    def add(self, obj):
        db.session.add(obj)
        db.session.commit()  # Sauvegarder immédiatement
        return obj

    def save(self, obj):
        db.session.commit()  # Sauvegarder les modifications
        return obj
