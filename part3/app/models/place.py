from .basemodel import BaseModel
from .user import User
from sqlalchemy.orm import validates
import uuid
from app.extensions import db

class Place(BaseModel):
    __tablename__ = 'places'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.String(250), nullable=True)
    price = db.Column(db.Float(), nullable=False, index=True)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)    
    
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    owner = db.relationship('User', backref='places', lazy=True)


    def __init__(self, title, price, latitude, longitude, owner, description=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        
        reviews = relationship('Review', backref='place', cascade='all, delete-orphan')
        amenities = relationship('Amenity', secondary='place_amenities', backref='places')
        
    
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
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError("Price must be a float")
        if value <= 0:
            raise ValueError("Price must be positive.")
        return value

    
    @validates('latitude')
    def validates_latitude(self, key, value):
        if not isinstance(value, float):
            raise TypeError("Latitude must be a float")
        super().is_between("latitude", value, -90, 90)
        return value
    
    
    @validates('longitude')
    def validates_longitude(self, key, value):
        if not isinstance(value, float):
            raise TypeError("Longitude must be a float")
        super().is_between("longitude", value, -180, 180)
        return value

    
    @validates('owner')
    def validates_owner(self, key, value):
        if not isinstance(value, User):
            raise TypeError("Owner must be a user instance")
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
            'owner_id': self.owner_id
        }
    
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
