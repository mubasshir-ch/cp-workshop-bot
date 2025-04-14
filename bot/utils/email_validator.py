import re


def is_valid_email(email: str) -> bool:
    """
    Validate the email address format.
    :param email: The email address to validate.
    :return: True if the email is valid, False otherwise.
    """

    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not email:
        return False

    if not re.match(regex, email):
        return False

    return True
