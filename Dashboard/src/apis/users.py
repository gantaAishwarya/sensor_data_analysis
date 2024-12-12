from flask import Blueprint, request, jsonify
from src.services.users import UserService

# Blueprint for User APIs
user = Blueprint('users', __name__, url_prefix='/users')

@user.route('/', methods=['POST'])
def create_user_endpoint():
    """
    Create a new user.

    This endpoint allows the creation of a new user with the provided details.

    Request JSON Body
    -----------------
    first_name : str
        The first name of the user (required).
    last_name : str
        The last name of the user (required).
    email : str
        The email of the user (required, must be unique).

    Returns
    -------
    Response
        JSON response with the created user's details and HTTP status 201, or an error message and HTTP status 400.
    """
    data = request.get_json()

    try:
        user = UserService.create_user(data)
        return jsonify(user), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user.route('/', methods=['GET'])
def get_all_users():
    """
    Retrieve all users.

    This endpoint retrieves all users in the database.

    Returns
    -------
    Response
        JSON response with a list of user details and HTTP status 200.
    """
    try:
        users = UserService.get_all_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """
    Retrieve a specific user by ID.

    Path Parameters
    ----------------
    user_id : int
        The ID of the user to retrieve.

    Returns
    -------
    Response
        JSON response with the user details and HTTP status 200, or an error message and HTTP status 404 if the user is not found.
    """
    try:
        user = UserService.get_user_by_id(user_id)
        return jsonify(user), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user.route('/<int:user_id>', methods=['PUT'])
def update_user_endpoint(user_id):
    """
    Update an existing user by ID.

    This endpoint updates the details of an existing user.

    Path Parameters
    ----------------
    user_id : int
        The ID of the user to update.

    Request JSON Body
    -----------------
    first_name : str, optional
        The updated first name of the user.
    last_name : str, optional
        The updated last name of the user.
    email : str, optional
        The updated email of the user (must be unique).

    Returns
    -------
    Response
        JSON response with the updated user details and HTTP status 200, or an error message and HTTP status 404 if the user is not found.
    """
    data = request.get_json()

    try:
        updated_user = UserService.update_user(user_id, data)
        return jsonify(updated_user), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user.route('/<int:user_id>', methods=['DELETE'])
def delete_user_endpoint(user_id):
    """
    Delete a specific user by ID.

    Path Parameters
    ----------------
    user_id : int
        The ID of the user to delete.

    Returns
    -------
    Response
        JSON response with a success message and HTTP status 200, or an error message and HTTP status 404 if the user is not found.
    """
    try:
        UserService.delete_user(user_id)
        return jsonify({'message': 'User deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
