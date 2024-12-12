from flask import Blueprint, jsonify, request
from datetime import datetime
from src.services.polling import PollingService

# Blueprint for Polling APIs
polling = Blueprint('polling', __name__, url_prefix='/polling')


@polling.route('/success', methods=['GET'])
def success():
    return jsonify({'success': "call"}), 200


@polling.route('/poll', methods=['GET'])
def poll_and_update():
    """
    Poll the external service and update the sensor readings in the database.

    This endpoint is triggered to poll the external service and insert the received data into the 'sensor_readings' table.

    Returns
    -------
    Response
        JSON response with the number of updated sensor readings or an error message.
    """
    try:
        # Trigger the polling and update of sensor readings
        result = PollingService.poll_and_update_sensor_readings()
        return jsonify({"message": f"{result} sensor readings updated."}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


@polling.route('/readings', methods=['GET'])
def get_readings():
    """
    Retrieve sensor readings based on the start and end time range.

    This endpoint retrieves sensor readings between the provided 'start_time' and 'end_time'.

    Query Parameters
    -----------------
    start_time : int
        The start Unix timestamp (required).
    end_time : int
        The end Unix timestamp (required).

    Returns
    -------
    Response
        JSON response with a list of sensor readings or an error message.
    """
    start_time = request.args.get('start_time', type=int)
    end_time = request.args.get('end_time', type=int)

    if not start_time or not end_time:
        return jsonify({"error": "start_time and end_time are required"}), 400

    try:
        # Fetch the sensor readings based on the time range
        readings = PollingService.get_readings_by_time_range(start_time, end_time)
        return jsonify(readings), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
