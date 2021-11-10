from typing import Union
import requests
import os
from datetime import datetime

from src.entities.user import User
from src.exceptions.user_exception import UserException


class UserController:
    def __init__(self):
        self._api_url = os.getenv(
            'API_URL',
            'https://cloud-computing-afeka.herokuapp.com'
        )

    def store_user(self, data: dict) -> dict:
        """
        An action that receives data with information is used

        stores it for future use and returns it to the service operator.
        If there is already a user with the same email address in the system,
        error code 500 will be returned

        :param data: The user's details
        :return: A user record
        """
        user_to_store = User(
            data.get("email", ''),
            data.get("name", ''),
            data.get("password", ''),
            data.get("roles", []),
            data.get('birthdate', '')
        )
        user_from_db = requests.get(
            url=f'{self._api_url}/keyValue/{data.get("email")}'
        )
        if not user_from_db:
            return requests.post(url=f'{self._api_url}/keyValue',
                                 json=user_to_store.user_to_json()).json()
        else:
            raise UserException(UserException.USER_EXISTS)

    def delete_all_users(self) -> None:
        """
        An action that deletes all user information in the system
        and does not return anything
        """
        requests.delete(url=f'{self._api_url}/keyValue')

    def update_user(self, email: str, details: dict) -> None:
        """
        An action that updates a user's information

        if the user is already stored in the system and is identified by its
        email address. This action also receives updated details and
        returns nothing.
        If there is no such user, the method will return an appropriate error
        code.

        Note that this action cannot change the user's email address

        :param email: The user's email
        :param details: The user's details
        """
        user = self.get_user(email)
        if user:
            # Update the user value
            requests.put(url=f'{self._api_url}/keyValue/{email}', json=details)
        else:
            raise UserException(UserException.NO_USER)

    def get_user(self, email: str, password: bool = False) -> Union[
        dict, None]:
        """
        An action that returns user information that stored in the system

        In the absence of such a user, the method will return a suitable error
        code (404). Please note that this does not reveal the user's password,
        but returns all the information stored in the service,
        except for the password.

        :param email: The user's email
        :param password: Optional param, if set to True, returns the
        password, otherwise, delete the password and return the user
        :return: The user's record without the password field
        """
        try:
            user = requests.get(url=f'{self._api_url}/keyValue/{email}').json()
        except Exception:
            return None
        if not password:
            del user["content"]["password"]
        return user

    def login(self, email: str, password: str) -> Union[dict, None]:
        """
        An action that aims to verify that the correct password of the
        user has been entered for the service.

        If there is a user who is identified by the email transmitted to the
        service and if the password entered, as an optional parameter,
        is indeed correct, the operation returns the user's details,
        similar to the previous operation in this exercise

        In the absence of such a user, or the password transmitted to the
        service is incorrect, the method will return an appropriate error code

        Note that this action also does not reveal the user's password

        :param email: The user's email
        :param password: The user's password
        :return: If the user exists return the user's record without the
        password field, otherwise, return None.
        """
        user = self.get_user(email, password=True)
        if not user:
            raise UserException(UserException.NO_USER)
        if password != user['content'].get("password", None):
            raise UserException(UserException.LOGIN_FAILED)
        del user['content']['password']
        return user

    def get_all_users(self) -> list[dict]:
        return requests.get(url=f'{self._api_url}/keyValue').json()[0]

    def get_users_ordered(
            self,
            users: list[dict],
            sort_by: str,
            sort_order: str
    ) -> list[dict]:
        """
        An action that returns an array of all users already saved in the
        system.

        Pay attention to comments regarding sorting below the instructions.
        Note that this does not reveal user passwords either

        :param users:
        :param sort_by: What to sort by (Name, Date, Email)
        :param sort_order: The value of the sorting attribute
        :return: List of order records (without pagination)
        """
        if not sort_by or sort_by == 'email':
            sort_by = 'ID'
        if not sort_order:
            sort_order = 'ASC'

        if sort_order == 'ASC':
            sort_order = False
        else:
            sort_order = True

        if sort_by == 'ID':
            users = sorted(users, key=lambda d: d['ID'], reverse=sort_order)
        if sort_by == 'birthdate':
            users = sorted(
                users,
                key=lambda d: d['content']['birthdate'],
                reverse=sort_order
            )
        if sort_by == 'name':
            users = sorted(
                users,
                key=lambda d: f"{d['content']['name']['first']} "
                              f"{d['content']['name']['last']}",
                reverse=sort_order
            )
        return users

    def search_users(
            self,
            users: list[dict],
            criteria_type: str,
            criteria_value: str
    ) -> list[dict]:
        """
        An action that returns an array of users that a certain attribute
        passed as a value parameter.

        such as:
            1) Their email address belongs to a specific domain (DOMAIN)
            2) Were born in a particular year
            3) Role defined for them

        :param data: The records filtered by criteria
        :param criteria_type: TODO: Change to enum
        :param criteria_value: TODO: Change to enum
        :return:  List of filtered records by criteria (without pagination)
        """

        if criteria_type == 'byEmailDomain':
            return list(
                filter(
                    lambda e: e['ID'].split('@')[1] == criteria_value,
                    users
                )
            )
        if criteria_type == 'byBirthYear':
            return list(
                filter(
                    lambda e: e['content']['birthdate'].year == int(
                        criteria_value
                    ),
                    users
                )
            )
        if criteria_type == 'byRole':
            return list(
                filter(
                    lambda e: criteria_value in e['content']['roles'],
                    users
                )
            )
        return []

    @staticmethod
    def prepare_user_dates(users: list[dict]) -> None:
        for user in users:
            user['content']['birthdate'] = \
                UserController._convert_string_to_date(
                    user['content']['birthdate']
                )

    @staticmethod
    def convert_user_dates(users: list[dict]) -> None:
        for user in users:
            user['content']['birthdate'] = \
                UserController._convert_date_to_string(
                    user['content']['birthdate']
                )

    @staticmethod
    def _convert_date_to_string(date: datetime) -> str:
        return date.strftime("%d-%m-%Y")

    @staticmethod
    def _convert_string_to_date(date: str) -> datetime:
        return datetime.strptime(date, '%d-%m-%Y')
