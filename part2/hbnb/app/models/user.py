import re
import hashlib
from app.models.base_model import BaseModel


class User(BaseModel):
    # Ensemble pour stocker tous les emails déjà utilisés
    __existing_email = set()
# ------------------------------------------------------------------------

    def __init__(self, last_name, first_name, email, mot_de_passe, is_admin=False):
        super().__init__()  # Appelle le constructeur de la classe BaseModel
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.__mot_de_passe = mot_de_passe
        self.is_admin = is_admin
        self.place = []
        self.reviews = []
        # Vérifie que nom, prenom et email ne sont pas vides
        if not last_name or not first_name or not email:
            raise TypeError("nom, prenom et email sont obligatoires")
# ------------------------------------------------------------------------

    @property
    def set_last_name(self):
        return self.__last_name
    # recuperation du nom

    @set_last_name.setter
    def set_last_name(self, value):
        if not value:
            raise TypeError("un nom est obligatoire")
        elif len(value) > 50:
            raise TypeError("le nom doit contenir moins de 50 caractères")
        self.__last_name = value  # Stocke le nom
        self.save()
# ------------------------------------------------------------------------

    @property
    def set_first_name(self):
        return self.__first_name
    # recuperation du prenom

    @set_first_name.setter
    def set_first_name(self, value):
        if not value:
            raise TypeError("un prenom est obligatoire")
        elif len(value) > 50:
            raise TypeError("le prenom doit contenir moins de 50 caractéres")
        self.__first_name = value
        self.save()
# ------------------------------------------------------------------------

    @property
    def set_email(self):
        return self.__email
    # ajout et verification du email

    @set_email.setter
    def set_email(self, valeur):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, valeur) or not valeur.endswith('.com'):
            raise TypeError("Format email non respecté")

        if valeur in User.__existing_email:
            raise ValueError("Cet email est déjà utilisé.")

        # Si l'utilisateur a déjà un email le retirer des emails existants
        if hasattr(self, '_User__email'):
            User.__existing_email.discard(self.__email)

        self.__email = valeur
        User.__existing_email.add(valeur)
        self.save()
# ------------------------------------------------------------------------

    @property
    def set_mot_de_passe(self):
        return self.__mot_de_passe
    # ajout et verification du mot de passe

    @set_mot_de_passe.setter
    def set_mot_de_passe(self, valeur):
        if not valeur:
            raise ValueError("Le mot de passe ne peut pas être vide.")
        # Hashage du mot de passe
        self.__mot_de_passe = hashlib.sha256(
            valeur.encode('utf-8')).hexdigest()
        self.save()
# ------------------------------------------------------------------------

    @property
    def set_admin(self):
        return self.__is_admin
# ajout de admin en valeur bool

    @set_admin.setter
    def set_admin(self, valeur):
        if not isinstance(valeur, bool):
            raise TypeError("admin doit etre en booléen")
        self.__is_admin = valeur
        self.save()
# ------------------------------------------------------------------------
    # Ajout de place et review

    def add_place(self, place):
        self.place.append(place)

    def add_review(self, review):
        self.reviews.append(review)
# ------------------------------------------------------------------------
    # supprimer un utilisateur

    def supp_user(self):
        if hasattr(self, "_User__email"):
            User.__existing_email.discard(self.__email)

        if hasattr(self, "_User__first_name"):
            del self.__first_name

        if hasattr(self, '_User__last_name'):
            del self.__last_name
