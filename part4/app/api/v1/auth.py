from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Modèle pour la validation des données d'entrée
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authentifier l’utilisateur et renvoyer un jeton JWT"""
        credentials = api.payload  # Obtenir l’email et le mot de passe

        # Étape 1 : Récupérer l’utilisateur en fonction de l’email fourni
        user = facade.get_user_by_email(credentials['email'])

        # Étape 2 : Vérifiez si l’utilisateur existe et si le mot de passe est correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Étape 3 : création du token JWT
        # Le token contient l'identité de l'utilisateur et un claim additionnel 'is_admin'
        # Ce claim permet de distinguer les privilèges administrateur côté API
        access_token = create_access_token(
            identity=str(user.id),   # seul l’identifiant utilisateur est stocké comme identité
            additional_claims={"is_admin": user.is_admin}
        )

        # Etape 4 : Retourner le jeton JWT au client
        return {'access_token': access_token}, 200
