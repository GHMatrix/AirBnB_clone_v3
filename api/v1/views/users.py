#!/usr/bin/python3
'''Creates the views for User'''

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Returns an empty dictionary with the status code 200"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Returns the new User with the status code 201"""
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")
    if new_user.get('email') is None:
        abort(400, "Missing email")
    if new_user.get('password') is None:
        abort(400, 'Missing password')

    user = User(**new_user)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Returns the User object with the status code 200"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    requset_body = request.get_json()
    if not requset_body:
        abort(400, "Not a JSON")

    for k, v in requset_body.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)

    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
