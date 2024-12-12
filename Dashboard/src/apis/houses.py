from flask import Blueprint, request, jsonify
from src.services.houses import HouseService

# Blueprint for House APIs
house = Blueprint('houses', __name__, url_prefix='/houses')

@house.route('/', methods=['POST'])
def create_house_endpoint():
    """
    Create a new house.

    This endpoint allows the creation of a new house with the provided address details and owner ID.

    Request JSON Body
    -----------------
    street : str
        The street name of the house (required).
    house_number : str
        The house number (required).
    city : str
        The city where the house is located (required).
    pincode : str
        The postal code of the house (required).
    country : str
        The country where the house is located (required).
    owner_id : int
        The ID of the owner of the house (required).

    Returns
    -------
    Response
        JSON response with the created house's details and HTTP status 201, or an error message and HTTP status 400.
    """
    data = request.get_json()

    try:
        house = HouseService.create_house(data)
        return jsonify(house), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@house.route('/', methods=['GET'])
def get_all_houses():
    """
    Retrieve all houses.

    This endpoint retrieves all houses in the database.

    Returns
    -------
    Response
        JSON response with a list of house details and HTTP status 200.
    """
    try:
        houses = HouseService.get_all_houses()
        return jsonify(houses), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@house.route('/<int:house_id>', methods=['GET'])
def get_house_by_id(house_id):
    """
    Retrieve a specific house by ID.

    Path Parameters
    ----------------
    house_id : int
        The ID of the house to retrieve.

    Returns
    -------
    Response
        JSON response with the house details and HTTP status 200, or an error message and HTTP status 404 if the house is not found.
    """
    try:
        house = HouseService.get_house_by_id(house_id)
        return jsonify(house), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@house.route('/<int:house_id>', methods=['PUT'])
def update_house_endpoint(house_id):
    """
    Update an existing house by ID.

    This endpoint updates the details of an existing house.

    Path Parameters
    ----------------
    house_id : int
        The ID of the house to update.

    Request JSON Body
    -----------------
    street : str, optional
        The updated street name of the house.
    house_number : str, optional
        The updated house number.
    city : str, optional
        The updated city where the house is located.
    pincode : str, optional
        The updated postal code of the house.
    country : str, optional
        The updated country where the house is located.
    owner_id : int, optional
        The updated ID of the owner of the house.

    Returns
    -------
    Response
        JSON response with the updated house details and HTTP status 200, or an error message and HTTP status 404 if the house is not found.
    """
    data = request.get_json()

    try:
        updated_house = HouseService.update_house(house_id, data)
        return jsonify(updated_house), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@house.route('/<int:house_id>', methods=['DELETE'])
def delete_house_endpoint(house_id):
    """
    Delete a specific house by ID.

    Path Parameters
    ----------------
    house_id : int
        The ID of the house to delete.

    Returns
    -------
    Response
        JSON response with a success message and HTTP status 200, or an error message and HTTP status 404 if the house is not found.
    """
    try:
        HouseService.delete_house(house_id)
        return jsonify({'message': 'House deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@house.route('/delete_all', methods=['DELETE'])
def delete_all_houses():
    """
    Delete all houses in the database.

    This endpoint removes all houses from the database.

    Returns
    -------
    Response
        JSON response with the number of deleted houses and HTTP status 200.
    """
    try:
        deleted_count = HouseService.delete_all_houses()
        return jsonify({'message': f'{deleted_count} houses deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
