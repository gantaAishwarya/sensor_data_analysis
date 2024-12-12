import requests
from datetime import datetime
from src.models.sensor_readings import SensorReading
from src.app.app import db
from sqlalchemy.sql import func

class PollingService:
    EXTERNAL_API_URL = "http://host.docker.internal:5000/measurements"

    @staticmethod
    def poll_and_update_sensor_readings():
        """
        Poll the external service to fetch new sensor data and insert it into the 'sensor_readings' table.
        
        Returns
        -------
        int
            The number of sensor readings inserted into the database.
        """
        # Define the time range for polling (last 2 minutes)
        end_time = int(datetime.utcnow().timestamp())
        start_time = end_time - 120  # 2 minutes ago
        
        # Fetch the data from the external API
        response = requests.get(PollingService.EXTERNAL_API_URL, params={'start_time': start_time, 'end_time': end_time})

        #print(response.text)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from external API. Status code: {response.status_code}")
        
        data = response.json()
        
        # Prepare the data to be inserted into the database
        readings_to_insert = []

        for entry in data['measurements']:

            sensor_id = entry.get('sensor_id')
            temperature = entry.get('temperature')
            timestamp = entry.get('time')
            

            if sensor_id and temperature is not None:
                reading = SensorReading(
                    sensor_id=sensor_id,
                    temperature=temperature,
                    timestamp=timestamp
                )

                readings_to_insert.append(reading)

        # Batch insert into the database
        if readings_to_insert:
            db.session.bulk_save_objects(readings_to_insert)
            db.session.commit()
            return len(readings_to_insert)
        else:
            return 0

    @staticmethod
    def get_readings_by_time_range(start_time, end_time):
        """
        Fetch sensor readings based on a time range.
        
        Parameters
        ----------
        start_time : int
            The start Unix timestamp.
        end_time : int
            The end Unix timestamp.
        
        Returns
        -------
        list
            A list of dictionaries with sensor reading details.
        """
        # Convert start_time and end_time from Unix timestamp to datetime
        start_datetime = datetime.utcfromtimestamp(start_time)
        end_datetime = datetime.utcfromtimestamp(end_time)

        
        readings = SensorReading.query.filter(
            func.to_timestamp(SensorReading.timestamp) >= start_datetime,
            func.to_timestamp(SensorReading.timestamp) <= end_datetime
        ).all()


        print(readings)

        # Format the results as a list of dictionaries
        readings_data = [{
            "sensor_id": reading.sensor_id,
            "temperature": reading.temperature,
            "timestamp": reading.timestamp.isoformat()
        } for reading in readings]

        return readings_data
