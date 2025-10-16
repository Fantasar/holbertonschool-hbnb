from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.services.facade import HBnBFacade

# ------------------------------------------------------------
# Fichier : places.py
# Description :
#   Ce fichier définit les endpoints liés aux lieux ("places")
#   dans l’application HBnB. Il permet de :
#     - Créer un nouveau lieu (POST)
#     - Lister tous les lieux (GET)
#     - Consulter un lieu spécifique (GET /<place_id>)
#     - Mettre à jour un lieu existant (PUT)
# ------------------------------------------------------------

facade = HBnBFacade()
api = Namespace('places', description='Place operations')

# ------------------------------------------------------------
# Modèles de données utilisés pour la validation et la documentation
# ------------------------------------------------------------


# Informations sur les commodités associées à un lieu
amenity_model = api.model(
    'PlaceAmenity',
    {
        'id': fields.String(description='Amenity ID'),
        'name': fields.String(description='Name of the amenity')
    }
)

# ------------------------------------------------------------

# Informations sur le propriétaire du lieu
user_model = api.model(
    'PlaceUser',
    {
        'id': fields.String(description='User ID'),
        'first_name': fields.String(
            description='First name of the owner'
        ),
        'last_name': fields.String(
            description='Last name of the owner'
        ),
        'email': fields.String(
            description='Email of the owner'
        )
    }
)

# ------------------------------------------------------------

# Ajout du modèle pour les avis liés à un lieu
review_model = api.model(
    'PlaceReview',
    {
        'id': fields.String(description='Review ID'),
        'text': fields.String(description='Text of the review'),
        'rating': fields.Integer(
            description='Rating of the place (1-5)'
        ),
        'user_id': fields.String(description='ID of the user')
    }
)

# ------------------------------------------------------------

# Modèle principal pour un lieu
place_model = api.model(
    'Place',
    {
        'title': fields.String(
            required=True,
            description='Title of the place'
        ),
        'description': fields.String(
            description='Description of the place'
        ),
        'price': fields.Float(
            required=True,
            description='Price per night'
        ),
        'latitude': fields.Float(
            required=True,
            description='Latitude of the place'
        ),
        'longitude': fields.Float(
            required=True,
            description='Longitude of the place'
        ),
        'owner_id': fields.String(
            required=True,
            description='ID of the owner'
        ),
        'owner': fields.Nested(
            user_model,
            description='Owner of the place'
        ),
        'amenities': fields.List(
            fields.Nested(amenity_model),
            description='List of amenities'
        ),
        'reviews': fields.List(
            fields.Nested(review_model),
            description='List of reviews'
        )
    }
)

# ------------------------------------------------------------


@api.route('/')
class PlaceList(Resource):

    """
    Création de la classe PlaceList qui est une enfant de
    Ressource. La classe contient les méthodes pour :
     - Ajouter un nouveau lieux
     - Récupérer une listes de lieux
    """

    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):

        """
        Créer un nouveau lieux, avec les codes erreur :
         - 400 : Erreur le lieux existe déjà
         - 201 : Création avec succès
        """

        place_data = api.payload
        existing_place = facade.place_repo.get_all()
        if any(p.title == place_data['title'] for p in existing_place):
            return {'error': 'Place already registered'}, 400

        new_place = facade.create_place(place_data)
        return {
            'id': new_place.id,
            'title': new_place.title
        }, 201

# ------------------------------------------------------------

    @api.response(200, 'List of places retrieved successfully')
    def get(self):

        """
        Récupérer la liste de tous les lieux enregistrés.
        Retourne uniquement les informations principales :
        id, titre, prix et propriétaire.
        """

        places = facade.get_all_places()
        return [
            {
                'id': p.id,
                'title': p.title,
                'price': p.price,
                'owner_id': p.owner_id
            }for p in place
        ], 200

# ------------------------------------------------------------


@api.route('/<place_id>')
class PlaceResource(Resource):

    """
    Création de la classe PlaceResource qui est une enfant de
    Ressource, elle contient les méthodes qui permette de :
     - Récupérer le détails d'un appartement avec un ID
     - Mettre à jour les informations d'un appartement
    """

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):

        """
        Obtenir les détails complets d'un lieu spécifique.
        Inclut les informations du propriétaire et des commodités.
        """

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': getattr(place, 'description', None),
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
                {
                    'id': a.id,
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

        """
        Mettre à jour les informations d'un lieu existant.
        Si le lieu n'existe pas → erreur 404.
        """

        data = api.payload
        updated_place = facade.update_place(place_id, data)

        if not updated_place:
            return {'error': 'Place not found'}, 404

        return {
            'id': updated_place.id,
            'title': updated_place.title,
            'price': updated_place.price,
            'latitude': updated_place.latitude,
            'longitude': updated_place.longitude
        }, 200

# ------------------------------------------------------------
