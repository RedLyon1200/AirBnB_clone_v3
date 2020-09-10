#!/usr/bin/python3
"""
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

opt_route = {'strict_slashes': False}

classes = {"Amenity": "amenities", "City": "cities",
           "Place": "places", "Review": "reviews",
           "State": "states", "User": "users"}


@app_views.route('/status', **opt_route)
def status():
    """ return status """
    return jsonify({"status": "OK"})


@app_views.route('/stats', **opt_route)
def stats():
    """ data stats """
    stats = dict([(val, storage.count(cls)) for cls, val in classes.items()])
    return jsonify(stats)
