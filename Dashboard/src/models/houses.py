from src.app.app import db
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship


class House(db.Model):
    __tablename__ = 'houses'

    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # House attributes
    street = db.Column(db.String(200), nullable=False)
    house_number = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(200), nullable=False)


    # Use string reference for the ForeignKey relationship to User
    owner_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)


    # Unique constraint to prevent duplicate house addresses for the same owner
    __table_args__ = (
        UniqueConstraint('street', 'house_number', 'owner_id', name='unique_house_per_owner'),
        db.Index('idx_house_owner', 'owner_id'),
    )

    def __init__(self, street, house_number, city, pincode, country, owner_id):
        """
        Initialize a House object with the given data.
        """
        self.street = street
        self.house_number = house_number
        self.city = city
        self.pincode = pincode
        self.country = country
        self.owner_id = owner_id

    def to_dict(self):
        """
        Convert the House object to a dictionary.
        """
        return {
            "id": self.id,
            "street": self.street,
            "house_number": self.house_number,
            "city": self.city,
            "pincode": self.pincode,
            "country": self.country,
            "owner_id": self.owner_id,
        }

    def save(self):
        """
        Save a House instance to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def rollback():
        """
        Rollback the current database session.
        """
        db.session.rollback()

    @staticmethod
    def delete_all():
        """
        Delete all records from the House table.
        """
        try:
            deleted_count = db.session.query(House).delete()
            db.session.commit()
            return deleted_count
        except Exception as e:
            db.session.rollback()
            raise e
