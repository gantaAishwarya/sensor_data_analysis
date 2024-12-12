from flask import Blueprint, request, jsonify
from src.services.sensors import SensorService

# Blueprint for Sensor APIs
sensor = Blueprint('sensors', __name__, url_prefix='/sensors')

@sensor.route('/', methods=['POST'])
def create_sensor_endpoint():
    """
    Create a new sensor.

    This endpoint allows the creation of a new sensor associated with a specific house.

    Request JSON Body
    -----------------
    house_id : int
        The ID of the house to associate the sensor with (required).
    status : str
        The status of the sensor.

    Returns
    -------
    Response
        JSON response with the created sensor's details and HTTP status 201, or an error message and HTTP status 400.
    """
    data = request.get_json()
    house_id = data.get('house_id')
    status = data.get('status')


    if not house_id:
        return jsonify({'error': 'Missing required fields: house_id'}), 400

    return SensorService.create_sensor(house_id, status)


@sensor.route('/', methods=['GET'])
def get_all_sensors():
    """
    Retrieve all sensors or a specific sensor by ID.

    Returns
    -------
    Response
        JSON response with the sensor(s) details and HTTP status 200, or an error message and HTTP status 404 if a specific sensor is not found.
    """
    sensor_id = request.args.get('sensor_id', type=int)
    return SensorService.get_sensors(sensor_id)


@sensor.route('/<int:sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    """
    Retrieve a specific sensor by ID.

    Path Parameters
    ----------------
    sensor_id : int
        The ID of the sensor to retrieve.

    Returns
    -------
    Response
        JSON response with the sensor details and HTTP status 200, or an error message and HTTP status 404 if the sensor is not found.
    """
    return SensorService.get_sensors(sensor_id)


@sensor.route('/<int:sensor_id>', methods=['PUT'])
def update_sensor_endpoint(sensor_id):
    """
    Update an existing sensor by ID.

    This endpoint updates the details of an existing sensor.

    Path Parameters
    ----------------
    sensor_id : int
        The ID of the sensor to update.

    Request JSON Body
    -----------------
    status : str, optional
        The updated status of the sensor.
    house_id : int, optional
        The updated house ID to associate the sensor with.

    Returns
    -------
    Response
        JSON response with the updated sensor details and HTTP status 200, or an error message and HTTP status 404 if the sensor is not found.
    """
    data = request.get_json()
    status = data.get('status')
    house_id = data.get('house_id')

    return SensorService.update_sensor(sensor_id, status=status, house_id=house_id)


@sensor.route('/<int:sensor_id>', methods=['DELETE'])
def delete_sensor_endpoint(sensor_id):
    """
    Delete a specific sensor by ID.

    Path Parameters
    ----------------
    sensor_id : int
        The ID of the sensor to delete.

    Returns
    -------
    Response
        JSON response with a success message and HTTP status 200, or an error message and HTTP status 404 if the sensor is not found.
    """
    return SensorService.delete_sensor(sensor_id)
