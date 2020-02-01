import uuid

from exceptions.InvalidUserException import InvalidUserException


class Account:
    def __init__(self, owner_name, balance=0, hold=0, is_open=0, id=None):
        self.id = id if id else str(uuid.uuid4())
        self.owner_name = owner_name
        self.balance = balance
        self.hold = hold
        self.is_open = is_open

    def add(self, addition) -> None:
        self.balance += addition

    def substract(self, substraction) -> None:
        result = self.balance - self.hold - substraction
        if result < 0:
            is_possible = False
        else:
            is_possible = True

        if not is_possible:
            raise Exception('Not enough money!')

        self.balance -= substraction

    def status(self) -> {}:
        return {
            'balance': self.balance,
            'hold': self.hold,
            'status': 'opened' if self.is_open else 'closed'
        }

    def serialize(self):
        return {
            'id': self.id,
            'ownerName': self.owner_name,
            'balance': self.balance,
            'hold': self.hold,
            'status': 'opened' if self.is_open else 'closed',
        }

    @staticmethod
    def deserialize(json: dict):
        try:
            id = json['id']
            owner_name = json['ownerName']
            balance = json['balance']
            hold = json['hold']
            status = json['status']
            return Account(owner_name, balance, hold, status, id)
        except:
            raise InvalidUserException()
