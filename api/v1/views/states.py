#!/usr/bin/python3
"""
"""

from flask import jsonify, abort
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
