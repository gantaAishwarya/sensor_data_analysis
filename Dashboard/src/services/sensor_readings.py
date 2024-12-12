from src.app.app import db
from src.models.sensor_readings import SensorReading
from flask import jsonify

class SensorReadingService:

    @staticmethod
    def get_sensor_readings_by_sensor_id(sensor_id: int):
        """
        Retrieve all sensor readings for a given sensor ID.

        Parameters
        ----------
        sensor_id : int
            The ID of the sensor to retrieve readings for.

        Returns
        -------
        list
            A list of dictionaries, each representing a sensor reading.

        Raises
        ------
        ValueError
            If no sensor readings are found.
        """
        # Use SQLAlchemy query with filter and all()
        sensor_readings = SensorReading.query.filter(SensorReading.sensor_id == sensor_id).all()

        # Check if records were found
        if sensor_readings:
            return [reading.to_dict() for reading in sensor_readings]
        else:
            raise ValueError("No sensor readings found for the given sensor ID")


    @staticmethod
    def get_all_sensor_readings():
        sensor_readings = SensorReading.query.all()
        return [sensor_reading.to_dict() for sensor_reading in sensor_readings]

