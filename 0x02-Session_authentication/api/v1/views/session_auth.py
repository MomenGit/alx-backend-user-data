#!/usr/bin/env python3
"""Module of session authentication views"""

from os import getenv
from flask import jsonify, request
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
        user = User.search({"email": email})[0]
    except Exception as err:
        return jsonify({"error": "no user found for this email"}), 404

    if user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    res = jsonify(user.to_json())
    res.set_cookie(getenv("SESSION_NAME"), session_id)
    return res
