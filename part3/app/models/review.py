from .basemodel import BaseModel
from .place import Place
from app.extensions import db
from .user import User
import uuid
from sqlalchemy.orm import validates

class Review(BaseModel):
	__tablename__ = 'reviews'

	id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
	text = db.Column(db.String(120), nullable=False, index=True)
	rating = db.Column(db.Float(), nullable=False, index=True)
	place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False, index=True)
	user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)

	place = db.relationship('Place', backref='reviews', lazy=True)
	user = db.relationship('User', backref='reviews', lazy=True)

	def __init__(self, text, rating, place, user):
		super().__init__()
		self.text = text
		self.rating = rating
		self.place = place
		self.user = user
	

	
	@validates('text')
	def validates_text(self, key, value):
		if not value:
			raise ValueError("Text cannot be empty")
		if not isinstance(value, str):
			raise TypeError("Text must be a string")
		return value

	
	@validates('rating')
	def validates_rating(self, key, value):
		if not isinstance(value, int, float):
			raise TypeError("Rating must be an integer")
		super().is_between('Rating', value, 1, 6)
		return value

	
	@validates('place')
	def validates_place(self, key ,value):
		if not isinstance(value, Place):
			raise TypeError("Place must be a place instance")
		return value


	@validates('user')
	def validates_user(self, key ,value):
		if not isinstance(value, User):
			raise TypeError("User must be a user instance")
		return value

	def to_dict(self):
		return {
			'id': self.id,
			'text': self.text,
			'rating': self.rating,
			'place_id': self.place.id,
			'user_id': self.user.id
		}
