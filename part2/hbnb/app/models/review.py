from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()  # Appelle le constructeur de la classe BaseModel
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
# ------------------------------------------------------------------------

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if not value:
            raise TypeError("Le texte doit contenir un avis")
        else:
            self.__text = value
            self.save()
# ------------------------------------------------------------------------

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        if type(value) not in (float, int):
            raise TypeError("la note doit etre un nombre")
        if value < 0 or value > 5:
            raise TypeError("la note doit etre comprise entre 0 et 5")
        self.__rating = value
        self.save()
# ------------------------------------------------------------------------

    @property
    def place(self):
        return self.__place
# Vérifie que la valeur donnée est liée a une place

    @place.setter
    def place(self, value):
        if not isinstance(value, Place):
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
