#!/usr/bin/env python3
""" setting up flask app """

from flask import Flask, jsonify, request, make_response, abort
from auth import Auth

app = Flask(__name__)

# Create an instance of the Auth class
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome():
    """GET route that returns a JSON payload."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """POST /users route to register a new user."""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        # sttempt to register the user
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        # If the user already exists, return an error message
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """Handle user login and create a session."""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        abort(400, description="Email and password are required")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    response = make_response(
            jsonify({"email": email, "message": "logged in"})
    )
    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Handle user logout by deleting the session."""
    # Get session_id from cookies
    session_id = request.cookies.get('session_id')

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user:
        AUTH.destroy_session(user.id)
        response = redirect("/")
        response.set_cookie("session_id", "", expires=0)
        return response
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
