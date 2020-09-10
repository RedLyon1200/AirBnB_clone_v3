#!/usr/bin/python3
"""
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User

opt_route = {'strict_slashes': False}


@app_views.route('/users/<user_id>', methods=['GET'], **opt_route)
@app_views.route('/users', methods=['GET'], **opt_route)
def get_users(user_id=None):
    """ Retrieves the list of all User objects or a specific User by id """

    if user_id:
        user = storage.get(User, user_id)

        if not user:
            abort(404)
        return jsonify(user.to_dict())

    users_obj = storage.all(User).values()
    users = [obj.to_dict() for obj in users_obj]

    return make_response(jsonify(users), 200)


@app_views.route('/users/<user_id>', methods=['DELETE'], **opt_route)
def delete_user(user_id):
    """  """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], **opt_route)
def create_user():
    """ Creates a User """
    data = request.get_json()

    if not data:
        return make_response('Not a JSON', 400)
    elif not data.get('email'):
        return make_response('Missing email', 400)
    elif not data.get('password'):
        return make_response('Missing password', 400)

    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], **opt_route)
def put_user(user_id):
    """ updates user """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    data = request.get_json()

    if not data:
        return make_response('Not a JSON', 400)

    for key, val in data.items():
        ignore_data = ['id', 'created_at', 'updated_at', 'email']

        if key not in ignore_data:
            setattr(user, key, val)

    user.save()
    return jsonify(user.to_dict()), 200
