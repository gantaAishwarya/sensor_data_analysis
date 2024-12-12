from src.models.houses import House
from src.app.app import db


class HouseService:
    """
    Service class for managing house-related operations.
    """

    @staticmethod
    def create_house(data: dict) -> dict:
        """
        Create a new house with the provided data.

        Parameters
        ----------
        data : dict
            A dictionary containing the details of the house to create.
            Required keys: 'street', 'house_number', 'city', 'pincode', 'country', 'owner_id'.

        Returns
        -------
        dict
            A dictionary representation of the newly created house.

        Raises
        ------
        ValueError
            If required fields are missing in the provided data.
        Exception
            If an error occurs during the database transaction.
        """
        required_fields = ['street', 'house_number', 'city', 'pincode', 'country', 'owner_id']
        if not all(field in data for field in required_fields):
            raise ValueError("All address fields and owner_id are required")

        new_house = House(
            street=data['street'],
            house_number=data['house_number'],
            city=data['city'],
            pincode=data['pincode'],
            country=data['country'],
            owner_id=data['owner_id']
        )
        try:
            db.session.add(new_house)
            db.session.commit()
            return new_house.to_dict()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error creating house: {str(e)}")

    @staticmethod
    def get_all_houses() -> list[dict]:
        """
        Retrieve all houses.

        Returns
        -------
        list[dict]
            A list of dictionaries representing all houses.

        Raises
        ------
        Exception
            If an error occurs during the database query.
        """
        try:
            houses = House.query.all()
            return [house.to_dict() for house in houses]
        except Exception as e:
            raise Exception(f"Error retrieving houses: {str(e)}")

    @staticmethod
    def get_house_by_id(house_id: int) -> dict:
        """
        Retrieve a house by its ID.

        Parameters
        ----------
        house_id : int
            The ID of the house to retrieve.

        Returns
        -------
        dict
            A dictionary representation of the house.

        Raises
        ------
        ValueError
            If the house with the given ID is not found.
        Exception
            If an error occurs during the database query.
        """
        try:
            house = House.query.get(house_id)
            if not house:
                raise ValueError("House not found")
            return house.to_dict()
        except Exception as e:
            raise Exception(f"Error retrieving house: {str(e)}")

    @staticmethod
    def update_house(house_id: int, data: dict) -> dict:
        """
        Update the details of a house by its ID.

        Parameters
        ----------
        house_id : int
            The ID of the house to update.
        data : dict
            A dictionary containing the updated house details.

        Returns
        -------
        dict
            A dictionary representation of the updated house.

        Raises
        ------
        ValueError
            If the house with the given ID is not found.
        Exception
            If an error occurs during the database transaction.
        """
        try:
            house = House.query.get(house_id)
            if not house:
                raise ValueError("House not found")

            house.street = data.get('street', house.street)
            house.house_number = data.get('house_number', house.house_number)
            house.city = data.get('city', house.city)
            house.pincode = data.get('pincode', house.pincode)
            house.country = data.get('country', house.country)
            house.owner_id = data.get('owner_id', house.owner_id)

            db.session.commit()
            return house.to_dict()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error updating house: {str(e)}")

    @staticmethod
    def delete_house(house_id: int):
        """
        Delete a house by its ID.

        Parameters
        ----------
        house_id : int
            The ID of the house to delete.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the house with the given ID is not found.
        Exception
            If an error occurs during the database transaction.
        """
        try:
            house = House.query.get(house_id)
            if not house:
                raise ValueError("House not found")
            db.session.delete(house)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error deleting house: {str(e)}")

    @staticmethod
    def delete_all_houses():
        """
        Delete all houses in the database.

        Returns
        -------
        int
            The number of houses deleted.

        Raises
        ------
        Exception
            If an error occurs during the database transaction.
        """
        try:
            deleted_count = db.session.query(House).delete()
            db.session.commit()
            return deleted_count
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error deleting all houses: {str(e)}")
