from threading import Lock

from entities import Account
from exceptions.NotEnoughMoneyException import NotEnoughMoneyException


class AccountsCollection:
    def __init__(self, db, logger):
        self._accounts_collection = db.accounts_collection
        self._locks = {}
        self.logger = logger

    def create_new_account(self, account: Account) -> None:
        self._accounts_collection.insert_one(account.serialize())

    def delete_account(self, account_id: str) -> None:
        self._accounts_collection.delete_one({'id': account_id})

    def get_account(self, account_id: str) -> Account:
        account_json = self._accounts_collection.find_one({'id': account_id})
        return Account.deserialize(account_json)

    def increment_balance(self, account_id: str, increment) -> None:
        self._accounts_collection.update_one(
            {'id': account_id},
            {"$inc": {'balance': increment}}
        )

    def decrement_balance(self, account_id: str, decrement: int) -> None:
        if account_id in self._locks:
            lock = self._locks[account_id]
        else:
            lock = Lock()
            self._locks[account_id] = lock

        with lock:
            account = self.get_account(account_id)
            result = account.balance - account.hold - decrement
            if result < 0:
                is_possible = False
            else:
                is_possible = True

            if not is_possible:
                raise NotEnoughMoneyException('Not enough money!')
            self._accounts_collection.update_one(
                {'id': account_id},
                {"$inc": {'hold': decrement}}
            )

    def get_all_accounts(self) -> []:
        accounts = self._accounts_collection.find({})
        return [Account.deserialize(a) for a in accounts]

    def substract_hold(self, account_id: str) -> None:
        account = self.get_account(account_id)
        account.balance -= account.hold
        account.hold = 0
        self._accounts_collection.update_one({'id': account_id}, {"$set": account.serialize()})
