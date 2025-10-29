from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request

users_api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = users_api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Passworld of the user')
})

admin_api = Namespace('admin', description='Admin operations')

# Modèle pour la mise à jour admin
admin_user_model = admin_api.model('AdminUser', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='Password of the user')
})


@admin_api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @admin_api.expect(admin_user_model)
    @admin_api.response(200, 'User updated successfully')
    @admin_api.response(403, 'Admin privileges required')
    @admin_api.response(404, 'User not found')
    @admin_api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, user_id):
        """Update any user (admin only)"""
        claims = get_jwt()  # Récupère toutes les claims du JWT
        is_admin = claims.get('is_admin', False)
        
        # Vérifier si l'utilisateur est admin
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403
        
        data = api.payload
        user = facade.get_user(user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        email = data.get('email')
        
        if email:
            # Check if email is already in use
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400
        
        # Logic to update user details, including email and password
        try:
            # Si un mot de passe est fourni, le hasher
            if 'password' in data:
                user.hash_password(data['password'])
                del data['password']  # Ne pas passer le password en clair
            
            # Mettre à jour les autres champs
            facade.update_user(user_id, data)
            return {'message': 'User updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400

@admin_api.route('/users/')
class AdminUserCreate(Resource):
    @admin_api.expect(admin_user_model)  # ← Documentation Swagger
    @admin_api.response(201, 'User created successfully')
    @admin_api.response(400, 'Invalid input data')
    @admin_api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):

        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        if not is_admin:
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        # Logic to create a new user
        try:
            new_user = facade.create_user(user_data)  # ← Utiliser facade, pas self
            new_user.hash_password(user_data['password'])  # ← Hasher le mot de passe
            return new_user.to_dict(), 201  # ← Code 201 pour création
        except Exception as e:
            return {'error': str(e)}, 400


@admin_api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @admin_api.expect(admin_user_model)  # ← Documentation Swagger
    @admin_api.response(200, 'User created successfully')
    @admin_api.response(400, 'Invalid input data')
    @admin_api.response(403, 'Admin privileges required')
    @admin_api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update any user (admin only)"""
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        if not is_admin:
            return {'error': 'Admin privileges required'}, 403

        data = admin_api.payload
        user = facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        email = data.get('email')

        # Ensure email uniqueness
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        # Logic to update user details
        try:
            if 'password' in data:
                user.hash_password(data['password'])
                del data['password']  # ← Ne pas passer le password en clair à update_user
            
            # Mettre à jour les autres champs
            facade.update_user(user_id, data)
            return {'message': 'User updated successfully'}, 200  # ← 200 pour update
        except Exception as e:
            return {'error': str(e)}, 400


@users_api.route('/')
class UserList(Resource):
    @users_api.expect(user_model, validate=True)
    @users_api.response(201, 'User successfully created')
    @users_api.response(409, 'Email already registered')
    @users_api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 409

        try:
            new_user = facade.create_user(user_data)
            new_user.hash_password(user_data['password'])
            return new_user.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @users_api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of users"""
        users = facade.get_users()
        return [user.to_dict() for user in users], 200


@users_api.route('/<user_id>')
class UserResource(Resource):
    @users_api.response(200, 'User details retrieved successfully')
    @users_api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @users_api.expect(user_model)
    @users_api.response(200, 'User updated successfully')
    @users_api.response(404, 'User not found')
    @users_api.response(400, 'Invalid input data')
    @jwt_required()  # protège l'endpoint
    def put(self, user_id):
        current_user = get_jwt_identity()  # récupère l'ID du user
        user_data = api.payload
        user = facade.get_user(user_id)

        # vérifie que user modifie uniquement ses propres données
        if user_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        # empêche modification email/password
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password'}, 400

        if not user:
            return {'error': 'User not found'}, 404
        try:
            facade.update_user(user_id, user_data)
            return user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
api = users_api