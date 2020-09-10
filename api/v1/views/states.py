#!/usr/bin/python3
"""
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/<state_id>', methods=['GET'])
@app_views.route('/states', methods=['GET'])
def get_states(state_id=None):
    """ Retrieves the list of all State objects or a specific State by id """

    if state_id:
        state = storage.get(State, state_id)

        if not state:
            abort(404)
        return jsonify(state.to_dict())

    states_obj = storage.all('State').values()
    states = [obj.to_dict() for obj in states_obj]

    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """  """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return {}, 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """ Creates a State """
    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}))

    if not data.get('name'):
        return make_response(jsonify({'error': 'Missing name'}))

    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    """ updates state """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        abort(400, description='Not a JSON')

    for key, val in data.items():
        ignore_data = ['id', 'created_at', 'updated_at']

        if key not in ignore_data:
            setattr(state, key, val)

    storage.save()
    return jsonify(state.to_dict()), 200
