#!/usr/bin/env python3
"""
Route Module for the API
"""
from flask import Flask,  abort, jsonify,  redirect, request
from flask_cors import CORS
from auth import Auth

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
AUTH = Auth()


@app.route("/", strict_slashes=False)
def index():
    """Return a JSON payload"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """ POST
    User Registration route
    """
    email, password = request.form.get("email"), request.form.get("password")
    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """ POST
    User Login Route
    """
    email, password = request.form.get("email"), request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie("session_id", session_id)

    return res


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """ DELETE
    User Logout Route
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route("/profile", strict_slashes=False)
def profile():
    """ GET /profile
    Return user's profile
    """
    session_id = request.cookies.get("session_id")
    if session_id is not None:
        user = AUTH.get_user_from_session_id(session_id)
        if user is not None:
            return jsonify({"email": user.email})

    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """ GET /reset_password
    Generate a reset password token
    """
    email = request.form.get("email")

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError as err:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """ PUT /reset_password
    Reset a user's password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_pwd = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_pwd)
    except ValueError as err:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
