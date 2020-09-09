#!/usr/bin/python3
"""
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


HBNB_API_HOST = getenv('HBNB_API_HOST', default="0.0.0.0")
HBNB_API_PORT = getenv('HBNB_API_PORT', default=5000)


conf = {'host': HBNB_API_HOST, 'port': HBNB_API_PORT, 'threaded': True}

@app.teardown_appcontext 
def teardown_storage():
    """ tear down method"""
    storage.close()

if __name__ == "__main__":
    app.run(**conf)
