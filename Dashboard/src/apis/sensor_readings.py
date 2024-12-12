from flask import Blueprint, request, jsonify
from src.services.sensor_readings import SensorReadingService
from src.models.sensor_readings import SensorReading

# Blueprint for SensorReading APIs
sensor_readings = Blueprint('sensor_readings', __name__, url_prefix='/sensor_readings')


@sensor_readings.route('/', methods=['GET'])
def get_all_sensor_readings():
    """
    Retrieve all sensor readings or a specific sensor by ID.

    Returns
    -------
    Response
        JSON response with the sensor(s) details and HTTP status 200, or an error message and HTTP status 404 if a specific sensor is not found.
    """
    try:
        sensor_readings = SensorReadingService.get_all_sensor_readings()
        return jsonify(sensor_readings), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@sensor_readings.route('/sensor/<int:sensor_id>', methods=['GET'])
def get_sensor_readings_by_id(sensor_id):
    try:
        sensor_reading = SensorReadingService.get_sensor_readings_by_sensor_id(sensor_id)
        return jsonify(sensor_reading), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
