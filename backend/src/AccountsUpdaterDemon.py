from db_collections.AccountsCollection import AccountsCollection
import threading


class AccountsUpdaterDemon:
    def __init__(self, logger, collection: AccountsCollection, interval_in_seconds: int = 10 * 60):
        self._logger = logger
        self._collection: AccountsCollection = collection
        self._subscribers_ids = []
        self._is_running = False
        self._interval_in_seconds = interval_in_seconds
        self._demon_thread = None

    def subscribe_id(self, id) -> None:
        self._subscribers_ids.append(id)

    def start(self):
        if self._is_running:
            raise Exception('Demon is already running')
        self._is_running = True
        self._demon_thread = threading.Thread(target=self._run)
        self._demon_thread.setDaemon(True)
        self._logger.info('Starting AccountUpdaterDemon')
        self._demon_thread.start()

    def stop(self):
        self._is_running = False

    def _run(self):
        if not self._is_running:
            return
        self._logger.info('Starting update holds')
        worker = threading.Thread(target=self._update_balances)
        worker.start()
        threading.Timer(self._interval_in_seconds, self._run).start()

    def _update_balances(self):
        for subscriber_id in self._subscribers_ids:
            self._collection.substract_hold(subscriber_id)
