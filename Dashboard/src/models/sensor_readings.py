import time
from src.app.app import db
from sqlalchemy import Index, ForeignKey
from sqlalchemy.orm import relationship

class SensorReading(db.Model):
    __tablename__ = 'sensor_readings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sensor_id = db.Column(db.Integer,  nullable=False, default = 1)
    temperature = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.Integer, default=lambda: int(time.time()), index=True)  # Store Unix timestamp
  

    def __init__(self, sensor_id, temperature, timestamp=None):
        self.sensor_id = sensor_id
        self.temperature = temperature
        if timestamp:
            self.timestamp = timestamp

    def to_dict(self):
        """
        Convert the SensorReading object to a dictionary.
        """
        return {
            "id": self.id,
            "sensor_id": self.sensor_id,
            "temperature": self.temperature,
            "timestamp": self.timestamp,
        }

    def save(self):
        """
        Save a SensorReading instance to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def batch_save(readings):
        """
        Bulk insert a batch of SensorReading instances.
        """
        try:
            db.session.bulk_save_objects(readings)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e