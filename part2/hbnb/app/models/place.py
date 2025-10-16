from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity


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
        if not value or not value.strip():
            raise ValueError("Le titre du lieu ne peut pas être vide.")
        if len(value.strip()) > 100:
            raise ValueError("Le titre ne doit pas dépasser 100 caractères.")
        self.__title = value.strip()
        self.save()
# ------------------------------------------------------------------------

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        if value is not None:
            self.__description = value.strip()
        else:
            self.__description = None
        self.save()
# ------------------------------------------------------------------------

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Le prix doit être un nombre.")
        if value <= 0:
            raise ValueError("Le prix doit être une valeur positive.")
        self.__price = float(value)
        self.save()
# ------------------------------------------------------------------------

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("La latitude doit être un nombre.")
        if not -90.0 <= value <= 90.0:
            raise ValueError(
                "La latitude doit être comprise entre -90.0 et 90.0.")
        self.__latitude = float(value)
        self.save()
# ------------------------------------------------------------------------

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("La longitude doit être un nombre.")
        if not -180.0 <= value <= 180.0:
            raise ValueError(
                "La longitude doit être comprise entre -180.0 et 180.0.")
        self.__longitude = float(value)
        self.save()
# ------------------------------------------------------------------------
# Definir propriétaire de la place

    @property
    def owner(self):
        return self.__owner
# verifie que le propriétaire est un uilisateur valide

    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise TypeError("Le propriétaire doit être un utilisateur valide")
        self.__owner = value
        self.save()
# ------------------------------------------------------------------------
# Classe le prix de la place

    def classify_prices(self):
        if self.__price <= 40:
            return "économique"
        elif self.__price <= 80:
            return "Business"
        else:
            return "haut de gamme"
# ------------------------------------------------------------------------

    def delete_offer(self, field_name):
        """Supprime un attribut du lieu s'il existe."""
        fields = {
            "title": "_Place__title",
            "description": "_Place__description",
            "price": "_Place__price",
            "latitude": "_Place__latitude",
            "longitude": "_Place__longitude",
            "owner": "_Place__owner"
        }

        if field_name not in fields:
            raise ValueError(f"Le champ '{field_name}' n'existe pas.")

        private_attr = fields[field_name]
        if hasattr(self, private_attr):
            delattr(self, private_attr)
            self.save()
        else:
            raise AttributeError(
                f"Impossible de supprimer le champ '{field_name}'.")
# ------------------------------------------------------------------------

    def add_review(self, review):
        if not isinstance(review, Review):
            raise TypeError("L'objet ajouté doit être une instance de Review.")
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise TypeError(
                "L'objet ajouté doit être une instance de Amenity.")
        self.amenities.append(amenity)
        self.save()
