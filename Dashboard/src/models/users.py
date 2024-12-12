from src.app.app import db
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'users'

    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # User attributes
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    
    # Use string reference for the relationship to House
    house = db.relationship('House', backref='owner', lazy=True)

    #TODO: Check if this is really required??
    # Index
    __table_args__ = (
        db.Index('idx_user_name', 'first_name', 'last_name'),
    )

    def __init__(self, first_name= None, last_name=None, email=None):
        """
        Initialize a User object with the given data.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def to_dict(self):
        """
        Convert the User object to a dictionary.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }

    def save(self):
        """
        Save a User instance to the database.
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
