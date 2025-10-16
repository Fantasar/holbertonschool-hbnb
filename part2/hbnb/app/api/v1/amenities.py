from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.services.facade import HBnBFacade


# ------------------------------------------------------------
# Fichier : amenities.py
# Description :
#   Ce fichier contient les points de terminaison (endpoints) de l’API
#   liés à la gestion des équipements (Amenity).
#   Il permet de :
#     - Créer un nouvel équipement (POST)
#     - Lister tous les équipements (GET)
#     - Consulter un équipement spécifique (GET /<amenity_id>)
#     - Mettre à jour un équipement existant (PUT)
# ------------------------------------------------------------

facade = HBnBFacade()
api = Namespace('amenities', description='Amenity operations')

# ------------------------------------------------------------
# Modèle de données utilisé pour la validation et la documentation
# ------------------------------------------------------------

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# ------------------------------------------------------------


@api.route('/')
class AmenityList(Resource):

    """
    Création de la class AmenityLists qui est une enfant
    de Ressource:
    La classe contient les méthodes pour :
      - Ajouter un nouvelle équipement
    """

    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):

        """
        Construction de la fonction pour créer un ajouter
        un nouvelle équipement, code retour possible :
         - 400 = Erreur, équipement déja présent.
         - 201 = Succès, nouvelle équipement.
        """

        amenity_data = api.payload
        existing_amenities = facade.amenity_repo.get_all()
        if any(a.name == amenity_data['name'] for a in existing_amenities):
            return {'error': 'Amenity already registered'}, 400

        new_amenity = facade.create_amenity(amenity_data)
        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201

# ------------------------------------------------------------

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):

        """
        Récupérer la liste de tous les équipements.
        Appelle la méthode `get_all_amenities()` de la façade.
        Retourne un tableau JSON contenant les équipements.
        """

        amenities = facade.get_all_amenities()
        return [
            {
                'id': a.id,
                'name': a.name
            }for a in amenities
        ], 200

# ------------------------------------------------------------


@api.route('/<amenity_id>')
class AmenityResource(Resource):

    """
    Création de la classe AmenityResource qui est une enfant de
    Ressource.
    Elle contient la méthodes qui permet de rechercher un équipement
    en utilisant l'ID, les codes de retours possibles sont :
      - 404 : code erreur équipement non trouvé.
      - 200 : code de succès
    """

    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):

        """
        Récupérer un équipement spécifique par son ID.
        """

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

# ------------------------------------------------------------

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):

        """
        Mettre à jour les informations d'un équipement.
        Si l'équipement n'existe pas → erreur 404.
        Sinon → met à jour les champs fournis.
        """

        data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, data)

        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404

        return {
            'id': updated_amenity.id,
            'name': updated_amenity.name
        }, 200

# ------------------------------------------------------------
