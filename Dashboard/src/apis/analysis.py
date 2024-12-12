from flask import Blueprint, jsonify
from src.services.sensor_readings import SensorReadingService
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import random

# Blueprint for Polling APIs
analysis = Blueprint('analysis', __name__, url_prefix='/analysis')


@analysis.route('/<int:sensor_id>', methods=['GET'])
def generate_time_series_graph(sensor_id):
    """
    Generate a time-series graph for the last minute of temperature readings of a specific sensor
    and save it locally as a PNG file.

    Parameters
    ----------
    sensor_id : int
        The ID of the sensor to generate the graph for.

    Returns
    -------
    Response
        JSON response indicating success or failure.
    """
    try:
        # Fetch sensor readings for the given sensor_id
        sensor_readings = SensorReadingService.get_sensor_readings_by_sensor_id(sensor_id)

        # Limit to the last 100 readings
        #sensor_readings = sensor_readings[-100:]
        sensor_readings = sensor_readings[-10:]

        # Check if sensor readings exist
        if not sensor_readings:
            raise ValueError("No sensor readings found for the given sensor ID")


        # Extract temperature and timestamp data
        temperatures = [reading['temperature'] for reading in sensor_readings]
        timestamps = [datetime.utcfromtimestamp(reading['timestamp']).strftime('%d.%m.%Y %H:%M:%S') for reading in sensor_readings]

        # Create the graph
        plt.figure(figsize=(12, 12))
        plt.plot(timestamps, temperatures, marker='o', linestyle='-', color='b', label='Temperature')
        plt.xticks(rotation=45, fontsize=6)
        # # Format the x-axis for dates in 'DD.MM.YYYY HH:MM' format
        # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y %H:%M'))
        # plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        # plt.gcf().autofmt_xdate()  # Rotate and align the x labels

        # Add labels, title, and grid
        plt.title(f'Temperature Readings for Sensor {sensor_id}', fontsize=14)
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Temperature', fontsize=12)
        plt.grid(True)

        # Add legend
        plt.legend()

        # Define the file path to save the graph
        output_dir = "saved_graphs"  # Directory to save the graph
        os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
        file_path = os.path.join(output_dir, f'sensor_{sensor_id}_graph.png')

        # Save the graph locally
        plt.savefig(file_path)
        plt.close()

        return jsonify({'message': f'Graph saved successfully at {file_path}'}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
