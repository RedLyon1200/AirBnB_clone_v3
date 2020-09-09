#!/usr/bin/python3
"""
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

classes = {"Amenity": "amenities", "City": "cities",
           "Place": "places", "Review": "reviews",
           "State": "states", "User": "users"}


@app_views.route('/status')
def status():
    """ return status """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """ data stats """
    stats = dict([(val, storage.count(cls)) for cls, val in classes.items()])
    return jsonify(stats)
