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


class MissingKeysError(Exception):
    def __init__(self, missing_keys, received_keys):
        self.message = "missing keys"
        self.missing_keys = missing_keys
        self.received_keys = received_keys
        self.status_code = HTTPStatus.BAD_REQUEST


class TypeFieldError(Exception):
    def __init__(self, expected_type,key):
        self.expected_type = expected_type
        self.status_code = HTTPStatus.BAD_REQUEST
        self.message = f"field {key} must be a {expected_type}"
