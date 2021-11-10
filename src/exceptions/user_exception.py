class UserException(Exception):
    USER_EXISTS = 'User already exists'
    NO_USER = 'No such user found'
    PASSWORD_ILLEGAL = 'Password must contain at least five characters, ' \
                       'at least one of which is a digit, such as ab4de.'
    NAME_INVALID = 'The name field need to be formatted as {first: <first ' \
                   'name>, last: <last name>}.'
    EMPTY_NAME = 'At least one of the name fields is empty,the field need ' \
                 'to be formatted as {first: <first name>, last: <last name>}.'
    EMAIL_INVALID = 'The email is not formatted right.'
    ROLE_INVALID = 'At least one of the roles are empty, please check the ' \
                   'roles.'
    NO_PASSWORD = 'No password provided'
    LOGIN_FAILED = 'Access denied'

    def __init__(self, error: str):
        self.error = error
        super(self.__class__)
