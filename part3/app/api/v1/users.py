from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


users_api = Namespace('users', description='User operations')
admin_api = Namespace('admin', description='Admin operations')


# Définition du modèle utilisateur pour la validation des requêtes et la documentation Swagger
# Ce modèle définit les champs obligatoires pour la création et la mise à jour des utilisateurs
user_model = users_api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Passworld of the user')
})

# Modèle utilisateur pour les opérations administratives
# Ce modèle étend le modèle utilisateur de base avec des privilèges administratifs supplémentaires
# et permet la modification de tous les attributs utilisateur, y compris le statut administrateur
admin_user_model = admin_api.model('AdminUser', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='Password of the user'),
    'is_admin': fields.Boolean(description='Admin status')

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
        """Mettre à jour n'importe quel utilisateur (admin uniquement)"""
        claims = get_jwt()  # Récupère toutes les revendications du token JWT
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
            # Hache le mot de passe s'il est fourni dans la requête
            # Supprime le mot de passe en texte clair avant la mise à jour
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

    @admin_api.response(200, 'user deleted successfully')
    @admin_api.response(404, 'user not found')
    @jwt_required()  # protège l'endpoint
    def delete(self, user_id):
        """Supprimer un utilisateur"""
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        if not is_admin:
            return {'error': 'Admin privileges required'}, 403
        
        try:
            facade.delete_user(user_id)
            return {'message': 'User deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400         


@users_api.route('/')
class UserList(Resource):
    @users_api.expect(user_model, validate=True)
    @users_api.response(201, 'User successfully created')
    @users_api.response(409, 'Email already registered')
    @users_api.response(400, 'Invalid input data')
    def post(self):
        """Enregistrer un nouvel utilisateur"""
        user_data = users_api.payload

        # Vérifie l'unicité de l'email avant la création de l'utilisateur
        # Empêche les adresses email en double dans le système
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 409

        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @users_api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Récupérer la liste des utilisateurs"""
        users = facade.get_users()
        return [user.to_dict() for user in users], 200


@users_api.route('/<user_id>')
class UserResource(Resource):
    @users_api.response(200, 'User details retrieved successfully')
    @users_api.response(404, 'User not found')
    def get(self, user_id):
        """Obtenir les détails d'un utilisateur par son ID"""
        try:
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            return user.to_dict(), 200
            
        except Exception as e:
            print(f"ERROR: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'error': 'Internal server error'}, 500
    @users_api.expect(user_model)
    @users_api.response(200, 'User updated successfully')
    @users_api.response(404, 'User not found')
    @users_api.response(400, 'Invalid input data')
    @jwt_required()  # protège l'endpoint
    def put(self, user_id):
        current_user = get_jwt_identity()  # Get authenticated user's ID from JWT
        user_data = users_api.payload

        # S'assure que les utilisateurs ne peuvent modifier que leurs propres données
        # Vérification de sécurité pour empêcher les modifications non autorisées
        if user_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Empêche la modification des champs sensibles (email/mot de passe)
        # Ces champs nécessitent des points de terminaison/processus spéciaux pour la sécurité
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password'}, 400

        try:
            facade.update_user(user_id, user_data)
            updated_user = facade.get_user(user_id)
            return updated_user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400

    @users_api.response(200, 'Review deleted successfully')
    @users_api.response(404, 'Review not found')
    @jwt_required()  # protège l'endpoint
    def delete(self, user_id):
        """Supprimer un utilisateur"""
        current_user = get_jwt_identity()  # Récupère l'ID de l'utilisateur authentifié depuis le JWT

        if user_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        try:
            facade.delete_user(user_id)
            return {'message': 'User deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400        
api = users_api