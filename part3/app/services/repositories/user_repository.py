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
