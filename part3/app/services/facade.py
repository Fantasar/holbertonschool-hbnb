"""
Ce fichier définit la classe HBnBFacade qui centralise et simplifie 
l'accès aux différentes opérations CRUD sur les utilisateurs, lieux, équipements et avis. 

Cette façade agit comme une interface unique entre la logique métier 
et les repositories, facilitant la gestion des données et la coordination des relations entre modèles.
"""

from app.services.repositories.user_repository import UserRepository
from app.services.repositories.amenity_repository import AmenityRepository
from app.services.repositories.place_repository import PlaceRepository
from app.services.repositories.review_repository import ReviewRepository
from app.extensions import db

from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.amenity_repo = AmenityRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.user_repo = UserRepository()

    # UTILISATEUR
    # Méthodes liées à la gestion des utilisateurs (CRUD basique via UserRepository)
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user
    
    def get_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)
    
    def update_user(self, user_id, user_data):
        if 'password' in user_data:
            user = self.user_repo.get(user_id)
            if user:
                user.hash_password(user_data['password'])
                del user_data['password']
        self.user_repo.update(user_id, user_data)

    def delete_user(self, user_id):
        user = self.user_repo.get(user_id)
        
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        self.user_repo.delete(user_id)
        return True

    # ÉQUIPEMENT
    # Méthodes pour gérer les équipements/commodités (amenities)
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)
    
    def delete_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError(f"Amenity with id {amenity_id} not found")
        
        self.amenity_repo.delete(amenity_id)
        return True

    # LIEU
    # Méthodes pour gérer les lieux (places) et les relations avec owners et amenities
    def create_place(self, place_data):
        user = self.user_repo.get(place_data['owner_id'])
        if not user:
            raise ValueError('User not found')

    # Crée l'objet Place sans fournir l'attribut owner au constructeur
        place = Place(
            title=place_data['title'],
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            description=place_data.get('description')
        )
        place.owner = user

    # Gestion des amenities (si présentes)
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if amenity:
                    place.amenities.append(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Place with id {place_id} not found")
        # Ne pas permettre la modification de owner_id ou id (sécurité/conservation d'intégrité)
        if 'owner_id' in place_data:
            del place_data['owner_id']
        if 'id' in place_data:
            del place_data['id']

         # Mise à jour des champs simples
        for key, value in place_data.items():
            if hasattr(place, key) and key not in ['created_at', 'updated_at']:
                setattr(place, key, value)

    # Mise à jour des amenities si présent dans place_data
        if 'amenities' in place_data:
            # Réinitialiser la liste des amenities
            place.amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if amenity:
                    place.amenities.append(amenity)

    # Persistance des changements en base de données
        db.session.commit()
        return place

    def delete_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Place with id {place_id} not found")
        
        # SQLAlchemy gère automatiquement les cascades
        self.place_repo.delete(place_id)
        return True

    # AVIS
    # Méthodes pour gérer les avis (reviews) associés aux lieux
    def create_review(self, review_data):        
        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise ValueError('Place not found')
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise ValueError('Invalid user_id: user not found')
        del review_data['user_id']
        review_data['user'] = user
        del review_data['place_id']
        review_data['place'] = place


        review = Review(**review_data)
        self.review_repo.add(review)

        return review
        
    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError('Place not found')
        return place.reviews

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review with id {review_id} not found")
        
        self.review_repo.delete(review_id)
        return True
