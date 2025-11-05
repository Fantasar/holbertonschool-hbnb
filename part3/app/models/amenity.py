from .basemodel import BaseModel
from app.extensions import db
import uuid
from sqlalchemy.orm import validates, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from .place import Place

from app.models.place_amenity import place_amenity

class Amenity(BaseModel):
	__tablename__ = 'amenities'

	id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
	name = db.Column(db.String(50), nullable=False, index=True)

	places = db.relationship(
		'Place',
		secondary=place_amenity,
		back_populates='amenities'
	)

	def __init__(self, name):
		super().__init__()	
		self.name = name


	@validates('name')
	def validates_name(self, key,value):
		if not isinstance(value, str):
			raise TypeError("Name must be a string")
		if not value:
			raise ValueError("Name cannot be empty")
		super().is_max_length('Name', value, 50)
		return value

	def update(self, data):
		return super().update(data)
	
	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name
		}
