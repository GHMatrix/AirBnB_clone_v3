#!/usr/bin/python3
'''api app module script'''

import os

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
CORS(app, resources={'/*': {'origins': app_host}})


@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    '''Handling 404 HTTP error code.'''
    code = error.__str__().split()[0]
    description = error.description
    message = {'error': description}
    return make_response(jsonify(message), code)


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
