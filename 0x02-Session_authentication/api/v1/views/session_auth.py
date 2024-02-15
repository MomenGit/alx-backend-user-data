#!/usr/bin/env python3
"""Module of session authentication views"""

from os import getenv
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Handles logging in for the Session authentication"""
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    elif password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({"email": email})
        if len(users) == 0 or not users:
            return jsonify({"error": "no user found for this email"}), 404
    except Exception as err:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            res = jsonify(user.to_json())
            res.set_cookie(getenv("SESSION_NAME"), session_id)
            return res

    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """Handles logging in for the Session authentication"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
