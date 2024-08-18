#!/usr/bin/env python3
""" session auth routes module  """

from flask import Blueprint, request, jsonify, make_response
from models.user import User
from api.v1.app import auth  # Import auth where needed to avoid circular imports

session_auth = Blueprint('session_auth', __name__, url_prefix='/auth_session')


@session_auth.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """ Login method """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search(email)
    if user is None:
        return jsonify({"error": "no user found for this email"}), 404
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(key=request.environ.get('SESSION_NAME'), value=session_id)

    return response


@session_auth.route('/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """ Logout method """
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
