from http import HTTPStatus


class IdNotFoundError(Exception):
    ...


class InvalidValueError(Exception):
    ...


class InvalidEmailError(Exception):
    ...


class InvalidPasswordError(Exception):
    ...


class OrderKeysError(Exception):
    def __init__(self, invalid_keys, expected_keys):
        self.message = "invalid keys"
        self.invalid_keys = invalid_keys
        self.expected_keys = expected_keys
        self.status_code = HTTPStatus.BAD_REQUEST
