#!/usr/bin/python3
'''index module'''

from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    '''returns the status code'''
    if request.method == 'GET':
        return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'])
def get_stats():
    """Retrieve the number of objects by type."""
    if request.method == "GET":
        stats = {}
        classes = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        for cls_name, cls_value in classes.items():
            stats[cls_value] = storage.count(cls_name)
        return jsonify(stats)
