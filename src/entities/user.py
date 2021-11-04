from datetime import datetime


class User:
    def __init__(
            self,
            email: str = '',
            name: dict = None,
            password: str = '',
            roles: list[str] = None,
            dob: datetime = datetime.now()
    ):
        if name:
            name = {}
        if roles:
            roles = []
        self._email = email
        self._name = name
        self._password = password
        self._dob = dob
        self._roles = roles

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
        self._email = email

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