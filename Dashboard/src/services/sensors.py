from src.app.app import db
from src.models.sensors import Sensor
from flask import jsonify

class SensorService:

    @staticmethod
    def create_sensor(house_id: int, status: str) -> tuple:
        """
        Create a new sensor associated with a specific house.

        Parameters
        ----------
        house_id : int
            The ID of the house to which the sensor will be associated.
        status : str, optional
            The status of the sensor (default is None).

        Returns
        -------
        tuple
            A tuple containing a JSON response with the sensor details and an HTTP status code.

        Raises
        ------
        Exception
            If there is an error during the database transaction.
        """
        sensor = Sensor(house_id=house_id, status=status)
        try:
            db.session.add(sensor)
            db.session.commit()
            return jsonify(sensor.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def get_sensors(sensor_id: int) -> tuple:
        """
        Retrieve all sensors or a specific sensor by its ID.

        Parameters
        ----------
        sensor_id : int, optional
            The ID of the sensor to retrieve. If None, retrieves all sensors.

        Returns
        -------
        tuple
            A tuple containing a JSON response with the sensor(s) details and an HTTP status code.


        """
        if sensor_id:
            sensor = Sensor.query.get(sensor_id)
            if sensor:
                return jsonify(sensor.to_dict()), 200
            else:
                return jsonify({"message": "Sensor not found"}), 404
        else:
            sensors = Sensor.query.all()
            return jsonify([sensor.to_dict() for sensor in sensors]), 200

    @staticmethod
    def update_sensor(sensor_id: int, status: str, house_id: int) -> tuple:
        """
        Update the details of an existing sensor by its ID.

        Parameters
        ----------
        sensor_id : int
            The ID of the sensor to update.
        status : str, optional
            The new status of the sensor.
        house_id : int, optional
            The new house ID to associate with the sensor.

        Returns
        -------
        tuple
            A tuple containing a JSON response with the updated sensor details and an HTTP status code.

        Raises
        ------
        None
        """
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            return jsonify({"message": "Sensor not found"}), 404
        if status:
            sensor.status = status
        if house_id:
            sensor.house_id = house_id

        try:
            db.session.commit()
            return jsonify(sensor.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def delete_sensor(sensor_id: int) -> tuple:
        """
        Delete a sensor by its ID.

        Parameters
        ----------
        sensor_id : int
            The ID of the sensor to delete.

        Returns
        -------
        tuple
            A tuple containing a JSON response with a success message and an HTTP status code.

        Raises
        ------
        None
        """
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            return jsonify({"message": "Sensor not found"}), 404

        try:
            db.session.delete(sensor)
            db.session.commit()
            return jsonify({"message": "Sensor deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
