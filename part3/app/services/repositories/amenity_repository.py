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
