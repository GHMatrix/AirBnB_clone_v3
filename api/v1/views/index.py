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
    if request.method == 'GET':
        classes = {"User": 'users', "Place": 'places',
                   "City": 'cities', "Amenity": 'amenities',
                   "Review": 'reviews', "State": 'states'}
        stats = {}

        for cls_name, value in classes:
            cls = getattr(storage.all(), cls_name)
            stats[value] = storage.count(cls)

        return jsonify(stats)
