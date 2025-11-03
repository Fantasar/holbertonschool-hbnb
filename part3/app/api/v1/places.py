from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request


places_api = Namespace('places', description='Place operations')

admin_places_api = Namespace('admin_places', description='Admin operations on places')


# Define the models for related entities
amenity_model = places_api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = places_api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = places_api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=False, description="List of amenities ID's")
})

@admin_places_api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @admin_places_api.expect(place_model)  # ← Ajouter la documentation
    @admin_places_api.response(200, 'Place updated successfully')
    @admin_places_api.response(400, 'Invalid input data')
    @admin_places_api.response(403, 'Admin privileges required')
    @admin_places_api.response(404, 'Place not found')
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

        data = request.get_json()
        if not data:
            return {'error': 'No input data provided'}, 400
        
       # Logic to update the place 
        try:
            updated_place = facade.update_place(place_id, data)
            return updated_place.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400




@places_api.route('/')
class PlaceList(Resource):
    @places_api.response(201, 'Place successfully created')
    @places_api.response(400, 'Invalid input data')
    @jwt_required()
    @places_api.expect(place_model)
    def post(self):
        """Register a new place"""
        place_data = request.get_json()
        if not place_data:
            return {'error': 'No input data provided'}, 400
        current_user_id = get_jwt_identity()
        # Force l'owner_id à être le user connecté (sécurité)
        place_data['owner_id'] = current_user_id
        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            print(f"Erreur détaillée: {str(e)}")
            return {'error': 'Failed to create place'}, 500

    @places_api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200


@places_api.route('/<place_id>')
class PlaceResource(Resource):
    @places_api.response(200, 'Place details retrieved successfully')
    @places_api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

    @places_api.expect(place_model)
    @places_api.response(200, 'Place updated successfully')
    @places_api.response(404, 'Place not found')
    @places_api.response(400, 'Invalid input data')
    @jwt_required()  # protège l'endpoint
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity() # récupère l'ID du user
        place_data = request.get_json()

         # Log pour débogage
        print("Données reçues :", place_data)

        if not place_data:
            return {'error': 'No input data provided'}, 400
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # vérifie que user connecté = propriétaire du place
        if place.owner_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        try:
            updated_place = facade.update_place(place_id, place_data)
            return updated_place.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            print("Erreur inattendue :", str(e))  # Log pour débogage
            return {'error': 'Failed to update place'}, 500

    @places_api.response(200, 'Place deleted successfully')
    @places_api.response(404, 'Place not found')
    @jwt_required()  # protège l'endpoint
    def delete(self, place_id):
        """Delete a place"""
        current_user = get_jwt_identity()  # récupère l'ID du user
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        try:
            facade.delete_place(place_id)
            return {'message': 'place deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400    


@places_api.route('/<place_id>/amenities')
class PlaceAmenities(Resource):
    @places_api.expect(amenity_model)
    @places_api.response(200, 'Amenities added successfully')
    @places_api.response(404, 'Place not found')
    @places_api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self, place_id):
        current_user = get_jwt_identity()
        amenities_data = request.get_json()
        if not amenities_data or not isinstance(amenities_data, list):
            return {'error': 'Invalid input data'}, 400

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        if place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        try:
            for amenity_id in amenities_data:
                amenity = facade.get_amenity(amenity_id)
                if not amenity:
                    return {'error': f'Amenity {amenity_id} not found'}, 400
                if amenity not in place.amenities:
                    place.amenities.append(amenity)
            db.session.commit()
            return {'message': 'Amenities added successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400


@places_api.route('/<place_id>/reviews/')
class PlaceReviewList(Resource):
    @places_api.response(200, 'List of reviews for the place retrieved successfully')
    @places_api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return [review.to_dict() for review in place.reviews], 200

api = places_api