from .basemodel import BaseModel
from app.extensions import db
import uuid
from sqlalchemy.orm import validates

class Amenity(BaseModel):
	__tablename__ = 'amenities'

	id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
	name = db.Column(db.String(50), nullable=False, index=True)

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
