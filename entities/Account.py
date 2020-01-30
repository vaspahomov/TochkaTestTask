import uuid


class Account:
    def __init__(self, owner_name, balance=0, hold=0, is_open=0):
        self.account_number = uuid.uuid4()
        self.owner_name = owner_name
        self.balance = balance
        self.hold = hold
        self.is_open = is_open

    def add(self, addition) -> None:
        self.balance += addition

    def substract(self, substraction) -> None:
        result = self.balance - self.hold - substraction
        if result < 0:
            isPossible = False
        else:
            isPossible = True

        if not isPossible:
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
            'accountNumber': self.account_number,
            'ownerName': self.owner_name,
            'balance': self.balance,
            'hold': self.hold,
            'status': 'opened' if self.is_open else 'closed',
        }