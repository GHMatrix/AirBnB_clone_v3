#!/usr/bin/python3
'''api app module'''

import os

from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.errorhandler(error)
def not_found_error(error):
    '''Handling 404 HTTP error code.'''
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
