import re
import hashlib
from app.models.base_model import BaseModel


class User(BaseModel):
    # Ensemble pour stocker tous les emails déjà utilisés
    __existing_emails = set()
# ------------------------------------------------------------------------

    def __init__(self, last_name, first_name, email, password, is_admin=False):
        super().__init__()  # Appelle le constructeur de la classe BaseModel
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

# ------------------------------------------------------------------------

    @property
    def last_name(self):
        return self.__last_name
    # recuperation du nom

    @last_name.setter
    def last_name(self, value):
        if not value:
            raise TypeError("un nom est obligatoire")
        elif len(value) > 50:
            raise TypeError("le nom doit contenir moins de 50 caractères")
        self.__last_name = value  # Stocke le nom

# ------------------------------------------------------------------------

    @property
    def first_name(self):
        return self.__first_name
    # recuperation du prenom

    @first_name.setter
    def first_name(self, value):
        if not value:
            raise TypeError("un prenom est obligatoire")
        elif len(value) > 50:
            raise TypeError("le prenom doit contenir moins de 50 caractéres")
        self.__first_name = value

# ------------------------------------------------------------------------

    @property
    def email(self):
        return self.__email
    # ajout et verification du email

    @email.setter
    def email(self, value):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, value):
            raise ValueError("Format email non respecté")

        if value in User.__existing_emails:
            if not hasattr(self, "_User__email") or self.__email != value:
                raise ValueError("Cet email est déjà utilisé.")

        # Si l'utilisateur a déjà un email le retirer des emails existants
        if hasattr(self, "_User__email") and self.__email != value:
            User.__existing_emails.discard(self.__email)

        self.__email = value
        User.__existing_emails.add(value)

# ------------------------------------------------------------------------

    @property
    def password(self):
        return self.__password
    # ajout et verification du mot de passe

    @password.setter
    def password(self, value):
        if not value or len(value) < 6:
            raise ValueError(
                "Le mot de passe doit contenir au moins 6 caractères.")
        # Hashage du mot de passe
        self.__password = hashlib.sha256(value.encode('utf-8')).hexdigest()

# ------------------------------------------------------------------------

    @property
    def is_admin(self):
        return self.__is_admin
    # ajout de admin en valeur bool

    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise TypeError("Le champ 'is_admin' doit être un booléen.")
        self.__is_admin = value

# ------------------------------------------------------------------------
    # Ajout de place et review

    def add_place(self, place):
        self.places.append(place)

    def add_review(self, review):
        self.reviews.append(review)
# ------------------------------------------------------------------------
    # supprimer un utilisateur

    def delete_user(self):
        if hasattr(self, "_User__email"):
            User.__existing_emails.discard(self.__email)
