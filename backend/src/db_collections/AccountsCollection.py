from threading import Lock

from entities.Account import Account
from exceptions.NotEnoughMoneyException import NotEnoughMoneyException


class AccountsCollection:
    def __init__(self, db, logger):
        self._accounts_collection = db.accounts_collection
        self._locks = []
        self.logger = logger

    def create_new_account(self, account: Account) -> None:
        self._accounts_collection.insert_one(account.serialize())

    def get_account(self, id: str) -> Account:
        account_json = self._accounts_collection.find_one({'id': id})
        return Account.deserialize(account_json)

    def increment_balance(self, id, increment) -> None:
        self._accounts_collection.update_one(
            {'id': id},
            {"$inc": {'balance': increment}}
        )

    def decrement_balance(self, id, decrement) -> None:
        if id in self._locks:
            lock = self._locks[id]
        else:
            lock = Lock()

        with lock:
            account = self.get_account(id)
            result = account.balance - account.hold - decrement
            if result < 0:
                is_possible = False
            else:
                is_possible = True

            if not is_possible:
                raise NotEnoughMoneyException('Not enough money!')
            self._accounts_collection.update_one(
                {'id': id},
                {"$inc": {'hold': decrement}}
            )

    def get_all_accounts(self) -> []:
        accounts = self._accounts_collection.find({})
        return [Account.deserialize(a) for a in accounts]

    def substract_hold(self, id) -> None:
        account = self.get_account(id)
        account.balance -= account.hold
        account.hold = 0
        self._accounts_collection.update_one({'id': id}, {"$set": account.serialize()})
