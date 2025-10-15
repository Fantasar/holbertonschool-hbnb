from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()  # Appelle le constructeur de la classe BaseModel
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []
# ------------------------------------------------------------------------

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if not value:
            raise TypeError("il faut un titre")

        if len(value) > 100:
            raise TypeError("il ne faut pas dépasser les 100 caractères")
        self.__title = value
        self.save()
# ------------------------------------------------------------------------

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value
        self.save()
# ------------------------------------------------------------------------

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if type(value) not in (int, float):
            raise TypeError("le prix doit être un nombre")
        if value < 0:
            raise ValueError("Le prix doit être positif")
        self.__price = value
        self.save()
# ------------------------------------------------------------------------

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        if type(value) not in (int, float):
            raise TypeError("La latitude doit être un nombre")

        if value < -90.0 or value > 90.0:
            raise TypeError(
                "La latitude doit être comprise entre -90.0 et 90.0")
        self.__latitude = value
        self.save()
# ------------------------------------------------------------------------

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        if type(value) not in (int, float):
            raise TypeError("La longitude doit être un nombre")

        if value < -180.0 or value > 180.0:
            raise TypeError(
                "La longitude doit être comprise entre -180.0 et 180.0")
        self.__longitude = value
        self.save()
# ------------------------------------------------------------------------
# Definir propriétaire de la place

    @property
    def owner(self):
        return self.__owner
# verifie que le propriétaire est un uilisateur valide

    def owner(self, value):
        if not isinstance(value, User):
            raise TypeError("Le propriétaire doit être un utilisateur valide")
        self.__owner = value
        self.save()
# ------------------------------------------------------------------------
# Classe le prix de la place

    def classify_prices(self):
        if self.__price <= 40:
            return "Economique"
        elif self.__price <= 80:
            return "Moyen"
        else:
            return "cher"
# ------------------------------------------------------------------------

    def delete_offer(self, value):
        # Dictionnaire pour faire le lien entre les noms et les attributs privé
        correspondance_fields = {
            "title": "_Place__title",
            "description": "_Place__description",
            "price": "_Place__price",
            "latitude": "_Place__latitude",
            "longitude": "_Place__longitude",
            "owner": "_Place__owner"
        }
# Si le champ existe dans le dictionnaire récupérer le nom de l'attribut privé
        if value in correspondance_fields:
            private_attribute_name = correspondance_fields[value]

            # Vérifie si l'objet possède cet attribut
            if hasattr(self, private_attribute_name):
                delattr(self, private_attribute_name)
                self.save()  # On met à jour la date de modification
                print(f"Le champ '{value}' a bien été supprimé.")
            else:
                print(f"{value} n'a pas pu être supprimé")
            self.save()
# ------------------------------------------------------------------------

    def add_review(self, review):
        """Ajouter un avis sur le lieu."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Ajoutez une commodité à l’endroit."""
        self.amenities.append(amenity)
