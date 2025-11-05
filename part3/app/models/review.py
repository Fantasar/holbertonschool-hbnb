from .basemodel import BaseModel
from app.extensions import db
from .user import User
import uuid
from sqlalchemy.orm import validates, relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .place import Place
    from .user import User

class Review(BaseModel):
	__tablename__ = 'reviews'

	id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
	text = db.Column(db.String(120), nullable=False, index=True)
	rating = db.Column(db.Float(), nullable=False, index=True)

	place_id = db.Column(
		db.String(36),
		db.ForeignKey('places.id'),
		nullable=False,
	)
	
	user_id = db.Column(
		db.String(36),
		db.ForeignKey('users.id'),
		nullable=False
	)

	place = db.relationship(
		'Place',
		back_populates='reviews'
	)
	user = db.relationship(
		'User',
		back_populates='reviews'
	)

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
		if not isinstance(value, (int, float)):
			raise TypeError("Rating must be an integer")
		value = float(value)
		if not 1.0 <= value <= 5.0:
			raise ValueError("Rating must be between 1 and 5")
		return value


	def to_dict(self):
		return {
			'id': self.id,
			'text': self.text,
			'rating': self.rating,
			'place_id': self.place.id,
			'user_id': self.user.id,
        	'created_at': self.created_at.isoformat() if self.created_at else None,
        	'updated_at': self.updated_at.isoformat() if self.updated_at else None
		}
