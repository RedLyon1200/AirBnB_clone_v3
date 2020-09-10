#!/usr/bin/python3
"""
---
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State

opt_route = {'strict_slashes': False}


@app_views.route('/states/<state_id>/cities', methods=['GET'], **opt_route)
def get_cities_by_state(state_id):
    """ Retrieves the list of all City objects of a State """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]

    return jsonify(cities), 200


@app_views.route('/cities/<city_id>', methods=['GET'], **opt_route)
def get_city(city_id):
    """ Retrieves a City object. """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'], **opt_route)
def delete_city(city_id):
    """ Deletes a City object. """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'], **opt_route)
def create_city(state_id):
    """ Creates a State """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    try:
        data = request.get_json()
        data['state_id'] = state_id
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if not data.get('name'):
        return make_response(jsonify({'error': 'Missing name'}), 400)

    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], **opt_route)
def put_city(city_id):
    """ Updates a City object """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, val in data.items():
        ignore_data = ['id', 'created_at', 'updated_at']

        if key not in ignore_data:
            setattr(city, key, val)

    storage.save()
    return jsonify(city.to_dict()), 200
