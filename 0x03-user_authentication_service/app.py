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
        response = make_response(redirect("/"))
        response.delete_cookie("session_id")
        return response
    abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    """GET /profile route to return user profile information."""
    session_id = request.cookies.get("session_id")

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user:
        return jsonify({"email": user.email}), 200

    abort(403)


@app.route("/reset_password", methods=["POST"])
def reset_password():
    """POST /reset_password route to handle password reset."""
    email = request.form.get("email")

    if not email:
        abort(400, description="Email is required")

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"reset_token": reset_token}), 200
    except ValueError:
        abort(403, description="Email not registered")


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """PUT /reset_password route to update the user's password."""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    if not email or not reset_token or not new_password:
        abort(400, description="Email, reset token, and new password are required")

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403, description="Invalid reset token")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
