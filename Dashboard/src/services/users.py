from src.models.users import User
from src.app.app import db
from sqlalchemy.exc import SQLAlchemyError


class UserService:
    @staticmethod
    def create_user(data: dict) -> dict:
        """
        Create a new user in the database.

        This method accepts user details, validates required fields, and stores the 
        user information in the database.

        Parameters
        ----------
        data : dict
            A dictionary containing user details with keys `first_name`, `last_name`, and `email`.

        Returns
        -------
        dict
            A dictionary representation of the created user.

        Raises
        ------
        ValueError
            If any required fields are missing in the input data.
        Exception
            For any errors occurring during the database transaction.
        """
        required_fields = ['first_name', 'last_name', 'email']
        if not all(field in data for field in required_fields):
            raise ValueError("First name, last name, and email are required")

        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email']
        )
        try:
            db.session.add(user)
            db.session.commit()
            return user.to_dict()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error creating user: {str(e)}")

    @staticmethod
    def get_all_users() -> list[dict]:
        """
        Retrieve all users from the database.

        This method queries the database and fetches all user records.

        Returns
        -------
        list[dict]
            A list of dictionaries representing all users in the database.
        """
        users = User.query.all()
        return [user.to_dict() for user in users]

    @staticmethod
    def get_user_by_id(user_id: int) -> dict:
        """
        Retrieve a user by their ID.

        This method fetches user details based on the provided user ID.

        Parameters
        ----------
        user_id : int
            The unique identifier of the user.

        Returns
        -------
        dict
            A dictionary representation of the user.

        Raises
        ------
        ValueError
            If no user is found with the provided ID.
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        return user.to_dict()

    @staticmethod
    def update_user(user_id: int, data: dict) -> dict:
        """
        Update an existing user's information.

        This method updates the specified fields of a user in the database.

        Parameters
        ----------
        user_id : int
            The unique identifier of the user to update.
        data : dict
            A dictionary containing the user fields to update.

        Returns
        -------
        dict
            A dictionary representation of the updated user.

        Raises
        ------
        ValueError
            If no user is found with the provided ID.
        Exception
            For any errors occurring during the database transaction.
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)

        try:
            db.session.commit()
            return user.to_dict()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error updating user: {str(e)}")

    @staticmethod
    def delete_user(user_id: int):
        """
        Delete a user by their ID.

        This method removes a user from the database based on the provided ID.

        Parameters
        ----------
        user_id : int
            The unique identifier of the user to delete.

        Raises
        ------
        ValueError
            If no user is found with the provided ID.
        Exception
            For any errors occurring during the database transaction.
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Error deleting user: {str(e)}")
