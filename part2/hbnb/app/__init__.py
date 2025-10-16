# ------------------------------------------------------------

"""
Fichier principal pour la création et la configuration de l'application Flask.

Ce module initialise l'application HBnB, configure les endpoints 
(API REST) et enregistre les différents espaces de noms (users, 
amenities, places, reviews).
"""

# ------------------------------------------------------------

from flask import Flask
from flask_restx import Api

# Importation des namespaces (points d'entrée des routes API)
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

# ------------------------------------------------------------

def create_app():

    """
    Crée et configure l'application Flask HBnB.
    """

    app = Flask(__name__)
    
    # Initialisation de la documentation Swagger / API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

# ------------------------------------------------------------

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')

    # Register the amenities namespace
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    # Register the places namespace
    api.add_namespace(places_ns, path='/api/v1/places')

    # Register the review namespace
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

# ------------------------------------------------------------

    return app

# ------------------------------------------------------------
