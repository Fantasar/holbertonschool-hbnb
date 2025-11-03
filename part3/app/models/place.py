from .basemodel import BaseModel
from sqlalchemy.orm import validates, relationship
import uuid
from app.extensions import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .review import Review
    from .amenity import Amenity

from app.models.place_amenity import place_amenity


class Place(BaseModel):
    __tablename__ = 'places'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float(), nullable=False, index=True)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)

    owner_id = db.Column(
        db.String(36),
        db.ForeignKey('users.id'),
        nullable=False
    )

    owner = db.relationship(
        'User', 
        back_populates='places'
    )
    
    reviews = db.relationship(
        'Review',
        back_populates='place',
        lazy=True,
        cascade='all, delete-orphan'
    )

    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity,
        lazy='subquery',
        back_populates='places'
    )
    
    def __init__(self, title, price, latitude, longitude, owner=None, description=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        
    
    @validates('title')
    def validates_title(self, key, value):
        if not value:
            raise ValueError("Title cannot be empty")
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        super().is_max_length('title', value, 100)
        return value

    
    @validates('price')
    def validates_price(self, key, value):
        if not isinstance(value, (float, int)):
            raise TypeError("Price must be a float or int")
        if value <= 0:
            raise ValueError("Price must be positive.")
        return float(value)

    
    @validates('latitude')
    def validates_latitude(self, key, value):
        if not isinstance(value, (float, int)):
            raise TypeError("Latitude must be a float")
        value = float(value)
        if not -90.0 <= value <= 90.0:
            raise ValueError("Latitude must be between -90 and 90")
        return value
    
    
    @validates('longitude')
    def validates_longitude(self, key, value):
        if not isinstance(value, float):
            raise TypeError("Longitude must be a float")
        value = float(value)
        if not -180.0 <= value <= 180.0:
            raise ValueError("Longitude must be between -180 and 180")
        return value

    


    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)
    
    def delete_review(self, review):
        """Add an amenity to the place."""
        self.reviews.remove(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
        }
        if include_owner and self.owner:
            result['owner'] = self.owner.to_dict(include_places=False)  # ✅ Évite la boucle
        if include_reviews:
            result['reviews'] = [review.to_dict() for review in self.reviews]
        if include_amenities:
            result['amenities'] = [amenity.to_dict() for amenity in self.amenities]
        return result
    
    def to_dict_list(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': self.owner.to_dict(),
            'amenities': self.amenities,
            'reviews': self.reviews
        }
