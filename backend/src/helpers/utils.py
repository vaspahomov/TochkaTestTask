from uuid import UUID

from db_collections import AccountsCollection
from exceptions.InvalidUserException import InvalidUserException


def is_valid_uuid(uuid_to_test: str, version=4) -> bool:
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_to_test


def account_is_in_db(accounts_collection, account_id):
    try:
        AccountsCollection.get_account(accounts_collection, account_id)
    except InvalidUserException:
        return False

    return True
