from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# ------------------------------------------------------------

facade = HBnBFacade()
api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# ------------------------------------------------------------

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload
        new_review = facade.create_review(review_data)
        return {
            'id': new_review.id,
            'text': new_review.text,
            'rating': new_review.rating,
            'user_id': new_review.user_id,
            'place_id': new_review.place_id,
            'created_at': getattr(new_review, 'created_at', None)
        }, 201

# ------------------------------------------------------------

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return[
            {
                'id': r.id,
                'text': r.text,
                'rating': r.rating,
                'user_id': r.user_id,
                'place_id': r.place_id
            }for r in reviews
        ], 200

# ------------------------------------------------------------

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        # Placeholder for the logic to retrieve a review by ID
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': getattr(review, 'text', None),
            'rating': getattr(review, 'rating', None),
            'user_id': review.user_id,
            'place_id': review.place_id 
        }, 200

# ------------------------------------------------------------

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        # Placeholder for the logic to update a review by ID
        data = api.payload

        updated_review = facade.update_review(review_id, data)
        if not updated_review:
            return {'error': 'Place not found'}, 404

        return {
            'id': update_review.id,
            'text': update_review.text,
            'rating': update_review.rating,
            'user_id': update_review.user_id,
            'place_id': update_review.place_id
        }, 200

# ------------------------------------------------------------

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        # Placeholder for the logic to delete a review
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200

# ------------------------------------------------------------

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # Placeholder for logic to return a list of reviews for a place
        reviews = facade.get_reviews_by_place(place_id)
        return [
            {
                'id': r.id,
                'text': r.text,
                'rating': r.rating,
                'user_id': r.user_id
            }for r in reviews
        ], 200

# ------------------------------------------------------------
