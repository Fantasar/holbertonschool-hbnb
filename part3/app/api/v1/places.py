from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1.users import admin_api

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

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@admin_api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @admin_api.expect(place_model)  # ← Ajouter la documentation
    @admin_api.response(200, 'Place updated successfully')
    @admin_api.response(400, 'Invalid input data')
    @admin_api.response(403, 'Admin privileges required')
    @admin_api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        claims = get_jwt()  # Récupère toutes les claims du JWT
        is_admin = claims.get('is_admin', False)
        
        # Vérifier si l'utilisateur est admin
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403

        place = facade.get_place(place_id)

        if not place:  # ← Vérifier si le place existe
            return {'error': 'Place not found'}, 404

        data = admin_api.payload
        
       # Logic to update the place 
        try:
            facade.update_place(place_id, data)
            return {'message': 'Place updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400




@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()  # Protège l'endpoint : seul un user connecté peut créer
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity()
        # Récupère l'ID du user connecté depuis le token JWT
        place_data = api.payload
        # Force l'owner_id à être le user connecté (sécurité)
        place_data['owner_id'] = current_user

        user = facade.user_repo.get_by_attribute('id', current_user)
        if not user:
            return {'error': 'Invalid input data'}, 400
        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict_list(), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()  # protège l'endpoint
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()  # récupère l'ID du user
        place_data = api.payload
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # vérifie que user connecté = propriétaire du place
        if place.owner.id != current_user:
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.update_place(place_id, place_data)
            return {'message': 'Place updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400


@api.route('/<place_id>/amenities')
class PlaceAmenities(Resource):
    @api.expect(amenity_model)
    @api.response(200, 'Amenities added successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def post(self, place_id):
        amenities_data = api.payload
        if not amenities_data or len(amenities_data) == 0:
            return {'error': 'Invalid input data'}, 400

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        for amenity in amenities_data:
            a = facade.get_amenity(amenity['id'])
            if not a:
                return {'error': 'Invalid input data'}, 400

        for amenity in amenities_data:
            place.add_amenity(amenity)
        return {'message': 'Amenities added successfully'}, 200


@api.route('/<place_id>/reviews/')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return [review.to_dict() for review in place.reviews], 200
