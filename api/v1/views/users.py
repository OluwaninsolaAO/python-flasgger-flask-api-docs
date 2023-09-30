#!/usr/bin/env python3
"""Users URI Module"""

from flask import abort, g, request
from api.v1.views import (
    app_views, storage, jsonify, postdata,
    login_required, pagination,
)
from models.user import User, UserRole
from sqlalchemy.exc import IntegrityError
from typing import List, Dict
from flasgger import swag_from

DOC_PATH = 'docs/users/'


@app_views.route('/users', methods=['GET'])
@login_required()
@swag_from(DOC_PATH + 'get_users.yaml')
def get_users():
    """Return all users in storage"""

    detailed = request.args.get('detailed') == 'true'

    users: List[User] = storage.all(User).values()
    return jsonify({
        "status": "success",
        "message": "Users retrieved successfully",
        "data": pagination(
            items=users,
            func=lambda x: x.to_dict(detailed=detailed)
        )
    }), 200


@app_views.route('/users/<user_id>', methods=['GET'])
@login_required()
@swag_from(DOC_PATH + 'get_user.yaml')
def get_user(user_id):
    """Returns a User with a matching user_id"""
    detailed = request.args.get('detailed') == 'true'

    user: User = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify({
        "status": "success",
        "message": "User retrieved successfully",
        "data": user.to_dict(detailed=detailed)
    }), 200


@app_views.route('/users/me', methods=['GET'])
@login_required()
@swag_from(DOC_PATH + 'get_me.yaml')
def get_current_user():
    """Returns a User that is currently logged

    Query params:
    + detailed :
        = true : returns detailed data logged in User,
        including sensitive informations.
    """

    detailed = request.args.get('detailed', False) == 'true'
    user: User = g.user
    return jsonify({
        "status": "success",
        "message": "User retrieved successfully",
        "data": user.to_dict(detailed=detailed)
    }), 200


@app_views.route('/users', methods=['POST'])
# @login_required()
@swag_from(DOC_PATH + 'post_user.yaml')
def create_users():
    """Create a new User"""
    data = postdata()
    if data is None:
        abort(400)

    # Enum Classes Mapping
    enums: Dict[str, dict] = {
        'role': {v.to_dict(): v for v in list(UserRole)},
    }

    attrs = ['name', 'email', 'phone', 'address', 'role',
             'password']
    nullable = ['password', 'address']
    user_data: dict = {}
    for attr in attrs:
        if attr in data:
            # get enum attribute
            if attr in enums:
                enum = enums.get(attr)
                if data.get(attr) in enum:
                    user_data.update({attr: enum.get(data.get(attr))})
                else:
                    return jsonify({
                        "status": "error",
                        "message": "Enum " + attr + " does not have any attribute named " + data.get(attr),
                        "data": None
                    }), 400
            else:
                user_data.update({attr: data.pop(attr)})
        elif attr not in nullable:
            return jsonify({
                "status": "error",
                "message": "Missing required data: " + attr,
                "data": None
            }), 400
    try:
        user = User(**user_data)
        print(user.__dict__)
        user.save()
    except IntegrityError:
        storage.rollback()
        return jsonify({
            "status": "error",
            "message": "Data Intergrity Error: duplicate email or phone number found.",
            "data": None
        }), 422

    return jsonify({
        "status": "success",
        "message": "User created successfully",
        "data": user.to_dict()
    }), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
@login_required()
@swag_from(DOC_PATH + 'put_user.yaml')
def update_user(user_id):
    """Updates user with a matching user_id"""
    data = postdata()
    if data is None:
        abort(400)
    user: User = storage.get(User, user_id)
    if user is None:
        abort(404)

    # validates g.user's access to update user data
    # if g.user is not user:
    #     abort(401)

    # Enum Classes Mapping
    enums: Dict[str, dict] = {
        'role': {v.to_dict(): v for v in list(UserRole)},
    }

    attrs = ['name', 'email', 'phone', 'address', 'role',
             'password']
    user_data: dict = {}
    for attr in attrs:
        if attr in data:
            # get enum attribute
            if attr in enums:
                enum = enums.get(attr)
                if data.get(attr) in enum:
                    user_data.update({attr: enum.get(data.get(attr))})
                else:
                    return jsonify({
                        "status": "error",
                        "message": "Enum " + attr + " does not have any attribute named " + data.get(attr),
                        "data": None
                    }), 400
            else:
                user_data.update({attr: data.pop(attr)})

    try:
        for key, value in user_data.items():
            setattr(user, key, value)
        user.save()
    except IntegrityError:
        storage.rollback()
        return jsonify({
            "status": "error",
            "message": "Integrity Error: phone or email already registered with another account",
            "data": None
        }), 422

    return jsonify({
        "status": "success",
        "message": "User data updated successfully",
        "data": user.to_dict(detailed=True)
    }), 200


@app_views.route('/users/<user_id>', methods=['DELETE'])
@login_required([UserRole.admin])
@swag_from(DOC_PATH + 'delete_user.yaml')
def delete_user(user_id):
    """Delete from storage user with a matching user_id"""
    user: User = storage.get(User, user_id)
    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({
        "status": "success",
        "message": "User deleted successfully",
        "data": None
    }), 200
