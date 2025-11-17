from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

"""espace logic dans le quelle est stocker /protected"""
# Namespace pour les endpoints protégés
# Regroupe les routes nécessitant une authentification JWT
api = Namespace('protected', description='Protected endpoint')


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    # Sécurisation : l'utilisateur doit être authentifié via un jeton JWT
    def get(self):
        """Un point de terminaison protégé qui nécessite un jeton JWT valide"""
        print("jwt------")
        print(get_jwt_identity())
        # Récupération de l'identifiant de l'utilisateur depuis le token JWT
        current_user = get_jwt_identity()

        # Retourne un message d'accueil contenant l'ID utilisateur
        return {'message': f'Hello, user {current_user}'}, 200
