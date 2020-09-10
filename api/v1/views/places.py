#!/usr/bin/python3
"""
---
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models import Place
from models.city import City
from models.state import State

opt_route = {'strict_slashes': False}


@app_views.route('/cities/<city_id>/places', methods=['GET'], **opt_route)
def get_places_by_city(city_id):
    """ Retrieves the list of all Place objects of a city """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]

    return jsonify(places), 200


@app_views.route('/places/<place_id>', methods=['GET'], **opt_route)
def get_place(place_id):
    """ Retrieves a Place object. """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'], **opt_route)
def delete_place(place_id):
    """ Deletes a place object. """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'], **opt_route)
def create_place(city_id):
    """ Creates a Place """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    data = request.get_json()

    if not data:
        return make_response('Not a JSON', 400)

    data['city_id'] = city_id

    if not data.get('user_id'):
        return make_response('Missing user_id', 400)

    user = storage.get(User, data.get('user_id'))
    if not user:
        abort(404)    

    if not data.get('name'):
        return make_response('Missing name', 400)

    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], **opt_route)
def put_place(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    data = request.get_json()

    if not data:
        return make_response('Not a JSON', 400)

    for key, val in data.items():
        ignore_data = ['id', 'user_id','city_id' 'created_at', 'updated_at']

        if key not in ignore_data:
            setattr(place, key, val)

    storage.save()
    return jsonify(place.to_dict()), 200
