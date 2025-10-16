from app.models.base_model import BaseModel
from app.models.user import User


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()  # Appelle le constructeur de la classe BaseModel
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        place.add_review(self)
        user.add_review(self)
# ------------------------------------------------------------------------

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if not value or not value.strip():
            raise ValueError("Le texte de l'avis ne peut pas être vide.")
        self.__text = value.strip()
        self.save()
# ------------------------------------------------------------------------

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("La note doit être un nombre.")
        if not 1 <= value <= 5:
            raise ValueError("La note doit être comprise entre 1 et 5.")
        self.__rating = value
        self.save()
# ------------------------------------------------------------------------

    @property
    def place(self):
        return self.__place
# Vérifie que la valeur donnée est liée a une place

    @place.setter
    def place(self, value):
        if not isinstance(value, BaseModel) or value.__class__.__name__ != "Place":
            raise TypeError("La place doit etre associé à un lieu valide")
        else:
            self.__place = value
            self.save()
# ------------------------------------------------------------------------

    @property
    def user(self):
        return self.__user
# Vérifie que la valeur donnée est liée a un user

    @user.setter
    def user(self, value):
        if not isinstance(value, User):
            raise TypeError("l'avis doit étre rédigé par un utilisateur")
        else:
            self.__user = value
            self.save()
