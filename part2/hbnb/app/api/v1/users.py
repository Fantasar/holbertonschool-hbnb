from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# ------------------------------------------------------------
# Initialisation de la façade et du namespace Flask-RestX
# ------------------------------------------------------------

facade = HBnBFacade()
api = Namespace('users', description='User operations')

# ------------------------------------------------------------
# Modèle pour la validation des entrées et la documentation Swagger
# ------------------------------------------------------------

user_model = api.model(
    'User',
    {
        'first_name': fields.String(
            required=True,
            description='First name of the user'
        ),
        'last_name': fields.String(
            required=True,
            description='Last name of the user'
        ),
        'email': fields.String(
            required=True,
            description='Email of the user'
        ),
    }
)

# ------------------------------------------------------------
# Ressource : /users
# ------------------------------------------------------------


@api.route('/')
class UserList(Resource):

    """
    Class Users qui est un enfant de Ressource, elle contient
    tout les intéractions possible avec l'utilisateur.
    """

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    def post(self):

        """
        Méthodes qui permet de créer un nouvel utilisateur.
        Les codes erreurs sont :
         - 201 : Succès retour du détails du nouvelle utilisateur.
         - 400 : Erreur si jamais l'email n'existe pas.
        """

        user_data = api.payload

        # Vérifie si l'email existe déjà
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Crée un nouvel utilisateur
        new_user = facade.create_user(user_data)
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

# ------------------------------------------------------------

    @api.response(200, 'List of users retrieved successfully')
    def get(self):

        """
        Méthode qui permet de récupérer la liste
        de tous les utilisateurs.
        - 200 : Succès retour du détails de
        la listes des utilisateurs.
        """

        users = facade.user_repo.get_all()
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }for user in users
        ], 200

# ------------------------------------------------------------
# Ressource : /users/<user_id>
# ------------------------------------------------------------


@api.route('/<user_id>')
class UserResource(Resource):

    """
    Classe UserResource qui est l'enfant de Ressource.
    Elle permet le travails avec l'ID d'un utilisateur.
    """

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):

        """
        Méthode qui permet de récupérer les détails
        d'un utilisateur par ID.
        Les codes erreurs sont :
         - 200 : Succès retour du détails de ID utilisateur.
         - 400 : Erreur si jamais l'ID n'existe pas.

        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

# ------------------------------------------------------------

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):

        """
        Méthode qui permet de mettre à jour un
        utilisateur par son ID.
        Les codes erreurs sont :
         - 200 : Succès retour l'utilisateur vient d'être
         mis à jour.
         - 400 : Erreur si jamais l'ID n'existe pas.
        """

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Met à jour les champs avec les nouvelles données
        data = api.payload
        for key, value in data.items():
            setattr(user, key, value)

        # Enregistre les modifications
        facade.user_repo.update(user)
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

# ------------------------------------------------------------
