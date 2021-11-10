from datetime import datetime

import re
from src.exceptions.user_exception import UserException


class User:
    _email: str
    _name: dict
    _password: str
    _dob: datetime
    _roles: list[str]

    def __init__(
            self,
            email: str = '',
            name: dict = None,
            password: str = '',
            roles: list[str] = None,
            dob: datetime = datetime.now()
    ):
        if not name:
            name = {}
        if not roles:
            roles = []
        self.email = email
        self.name = name
        self.password = password
        self.birth_day = dob
        self.roles = roles

    @property
    def name(self) -> dict:
        return self._name

    @name.setter
    def name(self, name: dict):
        if all(att in name.keys() for att in ['first', 'last']):
            if not name['first'] or not name['last']:
                raise UserException(UserException.EMPTY_NAME)
            self._name = name
        else:
            raise UserException(UserException.NAME_INVALID)

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str):
        if self.validate_email(email):
            self._email = email
        else:
            raise UserException(UserException.EMAIL_INVALID)

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str):
        if len(password) < 5 or not self._check_digit(password):
            raise UserException(UserException.PASSWORD_ILLEGAL)
        self._password = password

    @property
    def birth_day(self):
        return self._dob

    @birth_day.setter
    def birth_day(self, dob: datetime):
        self._dob = dob

    @property
    def roles(self) -> list:
        return self._roles

    @roles.setter
    def roles(self, roles: list):
        for role in roles:
            if not role:
                raise UserException(UserException.ROLE_INVALID)
        self._roles = roles

    @staticmethod
    def validate_email(email: str) -> bool:
        # Make a regular expression
        # for validating an Email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if re.fullmatch(regex, email):
            return True
        else:
            return False

    @staticmethod
    def _check_digit(password: str) -> bool:
        for char in password:
            if char.isdigit():
                return True
        return False

    def user_to_json(self) -> dict:
        return {
            "email": self.email,
            "name": self.name,
            "password": self.password,
            "roles": self.roles,
            "birthdate": self.birth_day
        }
