from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request
from app.api.v1.users import admin_api

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@admin_api.route('/')
class AmenityList(Resource):
    @admin_api.expect(amenity_model)
    @admin_api.response(201, 'Amenity successfully created')
    @admin_api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        is_admin = claims.get('is_admin', False)
        existing_amenity = facade.amenity_repo.get_by_attribute('name', amenity_data.get('name'))
        if existing_amenity:
            return {'error': 'Invalid input data'}, 400
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @admin_api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

@admin_api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @admin_api.expect(amenity_model)
    @admin_api.response(200, 'Amenity successfully created')
    @admin_api.response(400, 'Invalid input data')
    @admin_api.response(403, 'Admin privileges required')
    @admin_api.response(404, 'Amenity not found')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity (admin only)"""
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        if not is_admin:
            return {'error': 'Admin privileges required'}, 403

        amenity = facade.get_amenity(amenity_id)  # ← Récupérer l'amenity

        if not amenity:
            return {'error': 'Amenity not found'}, 404

        amenity_data = admin_api.payload

        # Logic to update an amenity
        try:
            facade.update_amenity(amenity_id, amenity_data)
            return {'message': 'Amenity updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400

@admin_api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @admin_api.expect(amenity_model)  # ← Documentation Swagger
    @admin_api.response(201, 'amenity created successfully')
    @admin_api.response(400, 'Invalid input data')
    @admin_api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        claims = get_jwt()
    
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = admin_api.payload

        # Logic to create a new amenity
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, amenity_id):
        amenity_data = api.payload
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        try:
            facade.update_amenity(amenity_id, amenity_data)
            return {"message": "Amenity updated successfully"}, 200
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Amenities deleted successfully')
    @api.response(404, 'Amenities not found')
  # protège l'endpoint
    @jwt_required()
    def delete(self, amenity_id):
        """Delete a Amenities"""
          # récupère l'ID du user
        current_user = get_jwt_identity()
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenities not found'}, 404
        # vérifie que user connecté = auteur de la review
        if amenity.user.id != current_user:
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.delete_amenity(amenity_id)
            return {'message': 'amenities deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400
@api.route('/')
class AmenityListResource(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')

    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        
        existing_amenity = facade.amenity_repo.get_by_attribute('name', amenity_data.get('name'))
        if existing_amenity:
            return {'error': 'Invalid input data'}, 400
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400