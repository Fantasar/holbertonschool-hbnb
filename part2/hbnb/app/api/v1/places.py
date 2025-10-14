from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.services.facade import HBnBFacade

# ------------------------------------------------------------

facade = HBnBFacade()
api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# ------------------------------------------------------------

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

# ------------------------------------------------------------

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        existing_place = facade.place_repo.get_all()
        if any(p.title == place_data['title'] for p in existing_place):
            return {'error': 'Place already registered'}, 400

        new_place = facade.create_place(place_data)
        return {
            'id': new_place.id,
            'name': new_place.name
        }, 201

# ------------------------------------------------------------

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        place = facade.get_all.places()
        return [
            {
                'id': p.id,
                'title': p.title
            }for p in place
        ], 200

# ------------------------------------------------------------

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'descritption': getattr(place, 'description', None),
            'price': getattr(place, 'price', None),
            'latitude': getattr(place, 'latitude', None),
            'longitude': getattr(place, 'longitude', None),
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            }
            if getattr(place, 'owner', None) else None,
            'amenities': [
                {'id': a.id,
                'name': a.name
                }
                for a in getattr(place, 'amenities', [])
            ]
        }, 200

# ------------------------------------------------------------

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        data = api.payload
        updated_place = facade.update_place(place_id, data)

        if not updated_place:
            return {'error': 'Place not found'}, 404

        return {
            'id': updated_place.id,
            'title': updated_place.title
        }, 200

# ------------------------------------------------------------
