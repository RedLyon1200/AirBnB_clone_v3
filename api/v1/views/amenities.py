#!/usr/bin/python3
"""
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

opt_route = {'strict_slashes': False}


@app_views.route('/amenities/<amenity_id>', methods=['GET'], **opt_route)
@app_views.route('/amenities', methods=['GET'], **opt_route)
def get_amenities(amenity_id=None):
    """
    Retrieves the list of all Amenity objects
    or a specific Amenity by id
    """

    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)

        if not amenity:
            abort(404)
        return jsonify(amenity.to_dict())

    amenity_objs = storage.all(Amenity).values()
    amenities = [obj.to_dict() for obj in amenity_objs]

    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], **opt_route)
def delete_amenity(amenity_id):
    """ Deletes a Amenity object """
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], **opt_route)
def create_amenity():
    """ Creates a Amenity """
    data = request.get_json()

    if not data:
        return make_response('Not a JSON', 400)

    if not data.get('name'):
        return make_response('Missing name', 400)

    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], **opt_route)
def put_amenity(amenity_id):
    """ updates amenity """
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    data = request.get_json()

    if not data:
        return make_response('Not a JSON', 400)

    for key, val in data.items():
        ignore_data = ['id', 'created_at', 'updated_at']

        if key not in ignore_data:
            setattr(amenity, key, val)

    storage.save()
    return jsonify(amenity.to_dict()), 200
