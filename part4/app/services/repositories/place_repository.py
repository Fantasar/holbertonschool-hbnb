"""
Ce fichier implémente le repository spécifique pour le modèle Place,
en héritant d’une classe générique SQLAlchemyRepository.

Il fournit des méthodes simples pour gérer la persistance des objets Place
en base de données via SQLAlchemy, notamment l’ajout et la sauvegarde
des modifications, encapsulant ainsi la logique d’accès aux données.
"""
from app.models.place import Place
from app.extensions import db
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

        def save(self, place):
            """Sauvegarde les modifications d'un Place en base de données."""
            db.session.commit()
class BaseRepository:
    def add(self, obj):
        db.session.add(obj)
        db.session.commit()  # Sauvegarder immédiatement
        return obj

    def save(self, obj):
        db.session.commit()  # Sauvegarder les modifications
        return obj
