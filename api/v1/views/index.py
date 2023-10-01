#!/usr/bin/python3
'''index module'''

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    '''returns the status code'''
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'])
def get_stats():
    """Retrieve the number of objects by type."""
    classes = ["User", "Place", "City", "Amenity", "Review", "State"]
    stats = {}

    for cls_name in classes:
        cls = getattr(storage.all(), cls_name)
        stats[cls_name] = storage.count(cls)

    return jsonify(stats)
