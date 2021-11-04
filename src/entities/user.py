from datetime import datetime

# re module provides support
# for regular expressions
import re


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
            self._name = name
        else:
            # TODO: Raise an exception
            pass

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str):
        # TODO: Check if the email is exists, and valid
        if self.validate_email(email):
            self._email = email
        else:
            raise RuntimeError('Invalid email was provided')

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str):
        # TODO: This string must contain at least five characters,
        #  at least one of which is a digit, such as ab4de
        self._password = password

    @property
    def birth_day(self):
        return self._dob

    @birth_day.setter
    def birth_day(self, dob: datetime):
        # TODO: Change the format of datetime to "dd-MM-yyyy"
        self._dob = dob

    @property
    def roles(self) -> list:
        return self._roles

    @roles.setter
    def roles(self, roles: list):
        # TODO: Make sure that these strings are not empty.
        #  Any value that is not an empty string will be considered valid
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

    def user_to_json(self) -> dict:
        return {
            "email": self.email,
            "name": self.name,
            "password": self.password,
            "roles": self.roles,
            "dob": self.birth_day
        }


