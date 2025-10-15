import re
import hashlib
from app.models.base_model import BaseModel


class User(BaseModel):
    __emails_existants = set()  # Ensemble pour stocker tous les emails déjà utilisés
# ------------------------------------------------------------------------

    def __init__(self, nom, prenom, email, mot_de_passe, is_admin=False):
        super().__init__()  # Appelle le constructeur de la classe BaseModel
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.__mot_de_passe = mot_de_passe
        self.is_admin = is_admin
        # Vérifie que nom, prenom et email ne sont pas vides
        if not nom or not prenom or not email:
            raise TypeError("nom, prenom et email sont obligatoires")
# ------------------------------------------------------------------------

    @property
    def set_nom(self):
        return self.__nom
#

    @set_nom.setter
    def set_nom(self, value):
        if not value:
            raise TypeError("un nom est obligatoire")
        elif len(value) > 50:
            raise TypeError("le nom doit contenir moins de 50 caractères")
        self.__nom = value  # Stocke le nom
        self.save()
# ------------------------------------------------------------------------

    @property
    def set_prenom(self):
        return self.__prenom

    @set_prenom.setter
    def set_prenom(self, value):
        if not value:
            raise TypeError("un prenom est obligatoire")
        elif len(value) > 50:
            raise TypeError("le prenom doit contenir moins de 50 caractéres")
        self.__prenom = value
        self.save()
# ------------------------------------------------------------------------

    @property
    def set_email(self):
        return self.__email

    @set_email.setter
    def set_email(self, valeur):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, valeur) or not valeur.endswith('.com'):
            raise TypeError("Format email non respecté")

        if valeur in User.__emails_existants:
            raise ValueError("Cet email est déjà utilisé.")

        if hasattr(self, '_User__email'):
            User.__emails_existants.discard(self.__email)

        self.__email = valeur
        User.__emails_existants.add(valeur)
        self.save()
# ------------------------------------------------------------------------

    @property
    def set_mot_de_passe(self):
        return self.__mot_de_passe

    @set_mot_de_passe.setter
    def set_mot_de_passe(self, valeur):
        if not valeur:
            raise ValueError("Le mot de passe ne peut pas être vide.")
        self.__mot_de_passe = hashlib.sha256(
            valeur.encode('utf-8')).hexdigest()
        self.save()
# ------------------------------------------------------------------------

    @property
    def set_admin(self):
        return self.__is_admin

    @set_admin.setter
    def set_admin(self, valeur):
        if not isinstance(valeur, bool):
            raise TypeError("admin doit etre en booléen")
        self.__is_admin = valeur
        self.save()
