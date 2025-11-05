from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Définition du modèle d'avis (Review) pour la validation et la documentation Swagger
# Ce modèle définit la structure des avis avec validation des champs requis
# Le champ texte permet de décrire l'expérience de l'utilisateur
# Le champ rating doit être un nombre entier entre 1 et 5 (système d'étoiles)
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)')
})


@api.route('/')
class ReviewList(Resource):
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()  # Sécurisation: nécessite un token JWT valide pour accéder à cet endpoint
    @api.expect(review_model)
    def post(self):
        """Enregistrer un nouvel avis"""
        review_data = request.get_json()
        # Récupération de l'identifiant de l'utilisateur à partir du token JWT
        current_user = get_jwt_identity()  # ID de l'utilisateur authentifié
        # Vérifie l'existence du lieu
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 400
        user = facade.get_user(current_user)
        if not user:
            return {'error': 'User not found'}, 400
        # Vérifie que l'utilisateur n'est pas le propriétaire du lieu
        if place.owner.id == current_user:
            return {'error': 'You cannot review your own place'}, 400

        # Vérifie que l'utilisateur n'a pas déjà donné son avis sur ce lieu
        existing_reviews = [
            r for r in place.reviews if r.user.id == current_user]
        if existing_reviews:
            return {'error': 'You have already reviewed this place'}, 400

        # Association de l'avis avec l'utilisateur connecté pour la sécurité
        review_data['user_id'] = current_user  # Force l'attribution de l'avis à l'utilisateur authentifié

        try:
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Récupérer la liste de tous les avis"""
        return [review.to_dict() for review in facade.get_all_reviews()], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Obtenir les détails d'un avis par son ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()  # Sécurisation: requiert un token JWT valide pour la mise à jour
    def put(self, review_id):
        """Mettre à jour les informations d'un avis"""
        current_user = get_jwt_identity()  # Récupère l'ID de l'utilisateur connecté
        review_data = api.payload
        # Vérifie l'existence de l'avis
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        # vérifie que user connecté = auteur de la review
        if review.user.id != current_user:
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.update_review(review_id, review_data)
            return {'message': 'Review updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()  # Sécurisation: requiert un token JWT valide pour la suppression
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()  # récupère l'ID du user
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        # vérifie que user connecté = auteur de la review
        if review.user.id != current_user:
            return {'error': 'Unauthorized action'}, 403

        try:
            # Supprime l'avis de la base de données
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400
