from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# ------------------------------------------------------------
# Classe de façade principale : interface entre API et logique
# ------------------------------------------------------------

_user_repo = InMemoryRepository()
_place_repo = InMemoryRepository()
_review_repo = InMemoryRepository()
_amenity_repo = InMemoryRepository()


class HBnBFacade:

    """
    Classe de façade qui centralise l'accès aux dépôts mémoire
    pour les entités principales (User, Place, Review, Amenity).
    """

    def __init__(self):

        """
        Initialise les différents dépôts en mémoire.
        """

        self.user_repo = _user_repo
        self.place_repo = _place_repo
        self.review_repo = _review_repo
        self.amenity_repo = _amenity_repo

# ----------------------------------------
# ---------- USER METHODS ----------------
# ----------------------------------------

    def create_user(self, user_data):

        """
        Crée un nouvel utilisateur et l'ajoute au dépôt.
        """

        user = User(**user_data)
        user.save()
        self.user_repo.add(user)
        return user

# ------------------------------------------------------------

    def update_user(self, user_id, user_data):

        """
        Fonction pour mettre a jour un utilisateur.
        """

        user = self.get_user(user_id)
        # Mettez à jour les attributs
        user.save()
        self.user_repo.update(user_id, user)
        return user

# ------------------------------------------------------------

    def get_user(self, user_id):

        """
        Récupère un utilisateur par son ID.
        """

        return self.user_repo.get(user_id)

# ------------------------------------------------------------

    def get_user_by_email(self, email):

        """
        Récupère un utilisateur à partir de son email.
        """

        return self.user_repo.get_by_attribute('email', email)

# -------------------------------------------
# ---------- AMENITY METHODS ----------------
# -------------------------------------------

    def create_amenity(self, amenity_data):

        """
        Crée une commodité et l'ajoute au dépôt.
        """

        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

# ------------------------------------------------------------

    def get_amenity(self, amenity_id):

        """
        Récupère une commodité à partir de son ID.
        """

        return self.amenity_repo.get(amenity_id)

# ------------------------------------------------------------

    def get_all_amenities(self):

        """
        Retourne la liste de toutes les commodités.
        """

        return self.amenity_repo.get_all()

# ------------------------------------------------------------

    def update_amenity(self, amenity_id, amenity_data):

        """
        Met à jour les informations d'une commodité.
        """

        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        for key, value in amenity_data.items():
            setattr(amenity, key, value)

        self.amenity_repo.update(amenity_id, amenity)
        return amenity

# -----------------------------------------
# ---------- PLACE METHODS ----------------
# -----------------------------------------

    def create_place(self, place_data):

        """
        Crée un nouveau lieu avec ses attributs de base.
        """

        # Vérifier que le owner existe
        owner_id = place_data.get('owner_id')
        owner = self.user_repo.get(owner_id)

        if not owner:
            raise ValueError(f"Utilisateur avec l'ID {owner_id} introuvable")
        
        place_data['owner'] = owner
        place = Place(**place_data)
        place.save()
        self.place_repo.add(place)
        return place

# ------------------------------------------------------------

    def get_place(self, place_id):

        """
        Récupère un lieu par son ID.
        """

        return self.place_repo.get(place_id)

# ------------------------------------------------------------

    def get_all_places(self):

        """
        Retourne la liste de tous les lieux.
        """

        return self.place_repo.get_all()

# ------------------------------------------------------------

    def update_place(self, place_id, place_data):

        """
        Met à jour les informations d'un lieu existant.
        """

        place = self.place_repo.get(place_id)
        if not place:
            return None

        allowed_fields = ['title', 'description', 'price', 'latitude', 'longitude']

        try:
            for key in allowed_fields:
                if key in place_data:
                    setattr(place, key, place_data[key])
            place.save()
            self.place_repo.update(place_id, place)
            return place
        except (ValueError, TypeError) as e:
            raise e

# ------------------------------------------
# ---------- REVIEW METHODS ----------------
# ------------------------------------------

    def create_review(self, review_data):

        """
        Crée un nouvel avis et l'ajoute au dépôt.
        """

        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        user = self.user_repo.get(user_id)
        place = self.place_repo.get(place_id)

        if not user:
            raise ValueError(f"Utilisateur avec l'ID {user_id} introuvable")
        if not place:
            raise ValueError(f"Lieu avec l'ID {place_id} introuvable")
        
        review = Review(
            text=review_data.get("text"),
            rating=review_data.get("rating"),
            place=place,
            user=user
        )

        self.review_repo.add(review)
        return review

# ------------------------------------------------------------

    def get_review(self, review_id):

        """
        Récupère un avis à partir de son ID.
        """

        return self.review_repo.get(review_id)

# ------------------------------------------------------------

    def get_all_reviews(self):

        """
        Retourne la liste de tous les avis.
        """

        return self.review_repo.get_all()

# ------------------------------------------------------------

    def get_reviews_by_place(self, place_id):

        """
        Récupère tous les avis associés à un lieu donné.
        """

        all_reviews = self.review_repo.get_all()
        filtered_reviews = []
        for r in all_reviews:
            if r.place_id == place_id:
                filtered_reviews.append(r)

        return filtered_reviews

# ------------------------------------------------------------

    def update_review(self, review_id, review_data):

        """
        Met à jour un avis existant.
        """

        review = self.review_repo.get(review_id)
        if not review:
            return None
        for key, value in review_data.items():
            setattr(review, key, value)

        self.review_repo.update(review)
        return review

# ------------------------------------------------------------

    def delete_review(self, review_id):

        """
        Supprime un avis du dépôt.
        """

        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review_id)
        return review
# ------------------------------------------------------------
