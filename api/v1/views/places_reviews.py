#!/usr/bin/python3
"""
---
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.city import City
from models.state import State
from models.review import Review

opt_route = {'strict_slashes': False}


@app_views.route('/places/<place_id>/reviews', methods=['GET'], **opt_route)
def get_reviews_by_place(place_id):
    """ Retrieves the list of all Review objects of a place """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]

    return jsonify(reviews), 200


@app_views.route('reviews/<review_id>', methods=['GET'], **opt_route)
def get_review(review_id):
    """ Retrieves a review object. """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'], **opt_route)
def delete_review(review_id):
    """ Deletes a review object. """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'], **opt_route)
def create_review(place_id):
    """ Creates a review """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    data = request.get_json()

    if not data:
        return make_response('Not a JSON', 400)

    data['place_id'] = place_id

    if not data.get('user_id'):
        return make_response('Missing user_id', 400)

    user = storage.get(User, data.get('user_id'))
    if not user:
        abort(404)

    if not data.get('text'):
        return make_response('Missing text', 400)

    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('reviews/<review_id>', methods=['PUT'], **opt_route)
def put_review(review_id):
    """ Updates a Review object """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    data = request.get_json()

    if not data:
        return make_response('Not a JSON', 400)

    for key, val in data.items():
        ignore_data = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

        if key not in ignore_data:
            setattr(review, key, val)

    storage.save()
    return jsonify(review.to_dict()), 200
