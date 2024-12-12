from src.app.app import db
from sqlalchemy import Index
from sqlalchemy.orm import relationship

class Sensor(db.Model):
    __tablename__ = 'sensors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(50), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'), nullable=False)

    # Index for frequently queried columns
    __table_args__ = (
        Index('ix_sensor_status', 'status'),
    )

    def __init__(self, house_id, status):

        self.status = status
        self.house_id = house_id

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "house_id": self.house_id
        }
