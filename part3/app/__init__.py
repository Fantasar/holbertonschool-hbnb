from flask import Flask
from flask_restx import Api
from app.extensions import bcrypt, db, jwt
from app.api.v1.users import users_api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.protected import api as protected_ns
from app.api.v1.users import admin_api as admin_ns


# Module d'initialisation de l'application Flask
# Ce fichier crée l'application, initialise les extensions (bcrypt, jwt, db)
# et enregistre les différents namespaces de l'API (users, amenities, places, reviews, auth, protected, admin)


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialisation des extensions : chiffrement, gestion JWT et base de données
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Création de l'objet Api de Flask-RESTX (génère la doc Swagger)
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API')

    # Enregistrement des namespaces (groupes de routes) exposés par l'API
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(protected_ns, path='/api/v1/protected')
    api.add_namespace(admin_ns, path='/api/v1/admin')

    # Création automatique des tables si elles n'existent pas (exécuté dans le contexte de l'application)
    with app.app_context():
        db.create_all()

    return app