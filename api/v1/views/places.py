#!/usr/bin/python3
'''Creates the views for places'''
from flask import abort, jsonify, make_response, request
import requests
from api.v1.views import app_views
from api.v1.views.amenities import amenities
from api.v1.views.places_amenities import place_amenities
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
import json
from os import getenv


@app_views.route('cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify([obj.to_dict() for obj in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Returns an empty dictionary with the status code 200"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Returns the new Place with the status code 201"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    new_place = request.get_json()
    if not new_place:
        abort(400, 'Not a JSON')
    if new_place.get('user_id') is None:
        abort(400, "Missing user_id")
    user_id = new_place['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if new_place.get('name') is None:
        abort(400, "Missing name")

    place = Place(**new_place)
    setattr(place, 'city_id', city_id)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Returns the Place object with the status code 200"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")

    for k, v in request_body.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, k, v)

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    retrieves all Place objects depending
    of the JSON in the body of the request
    """
    request_body = request.get_json()
    if request_body is None:
        abort(400, "Not a JSON")

    reuest_bodyq = request.get_json()
    if request_body is None or (
        request_body.get('states') is None and
        request_body.get('cities') is None and
        request_body.get('amenities') is None
    ):
        places = storage.all(Place)
        return jsonify([place.to_dict() for place in places.values()])

    places = []

    if request_body.get('states'):
        states = []
        for ids in request_body.get('states'):
            states.append(storage.get(State, ids))

        for state in states:
            for city in state.cities:
                for place in city.places:
                    places.append(place)

    if request_body.get('cities'):
        cities = []
        for ids in request_body.get('cities'):
            cities.append(storage.get(City, ids))

        for city in cities:
            for place in city.places:
                if place not in places:
                    places.append(place)

    if not places:
        places = storage.all(Place)
        places = [place for place in places.values()]

    if request_body.get('amenities'):
        obj_am = [storage.get(Amenity, id) for id in
                  request_body.get('amenities')]
        i = 0
        limit = len(places)
        HBNB_API_HOST = getenv('HBNB_API_HOST')
        HBNB_API_PORT = getenv('HBNB_API_PORT')

        port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
        first_url = "http://0.0.0.0:{}/api/v1/places/".format(port)
        while i < limit:
            place = places[i]
            url = first_url + '{}/amenities'
            request_body = url.format(place.id)
            response = requests.get(request_body)
            place_am = json.loads(response.text)
            amenities = [storage.get(Amenity, obj['id']) for obj in place_am]
            for amenity in obj_am:
                if amenity not in amenities:
                    places.pop(i)
                    i -= 1
                    limit -= 1
                    break
            i += 1

    return jsonify([obj.to_dict() for obj in places])
