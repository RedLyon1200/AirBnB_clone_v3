#!/usr/bin/python3
"""
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


HBNB_API_HOST = getenv('HBNB_API_HOST', default="0.0.0.0")
HBNB_API_PORT = getenv('HBNB_API_PORT', default=5000)


conf = {'host': HBNB_API_HOST,
        'port': HBNB_API_PORT, 'threaded': True, 'debug': True}


@app.errorhandler(404)
def page_not_found(e):
    """handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_storage(e):
    """ tear down method"""
    storage.close()


if __name__ == "__main__":
    app.run(**conf)
