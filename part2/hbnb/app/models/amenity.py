from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place
from app.models.review import Review


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
# ------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not value:
            raise TypeError("il faut indiquer le nom de l'équipement")

        if type(value) not in (str):
            raise TypeError("L'équipement doit être une chaine de caractères")

        if len(value) > 50:
            raise TypeError(
                "Le nom de l'équipement ne peut pas depasser 50 caractères")
        else:
            self.__name = value
            self.save()
