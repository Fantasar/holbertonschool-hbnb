# Module des extensions Flask utilisées par l'application
# Ce fichier crée des instances non initialisées (factories) des extensions
# - `bcrypt` : chiffrement des mots de passe (Flask-Bcrypt)
# - `db`     : ORM / gestion de la base de données (Flask-SQLAlchemy)
# - `jwt`    : gestion des tokens JWT (Flask-JWT-Extended)
# L'initialisation effective (`init_app`) est réalisée dans `app/__init__.py`
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Instances des extensions (sera initialisé dans create_app)
bcrypt = Bcrypt()
db = SQLAlchemy()
jwt = JWTManager()