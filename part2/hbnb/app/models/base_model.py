import uuid
from datetime import datetime


class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Mettre à jour le timestamp updated_at chaque fois que l’objet est modifié"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Mettre à jour les attributs de l’objet en fonction du dictionnaire fourni"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Mettre à jour le timestamp updated_at

    def get_id(self):
        return self.id

    def get_created_at(self):
        return self.created_at

    def get_updated_at(self):
        return self.updated_at
