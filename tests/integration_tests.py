import unittest
import requests

backend_url = 'http://backend:5000'


class ApiTests(unittest.TestCase):
    def setUp(self) -> None:
        resp = requests.post(f'{backend_url}/api/create', json={'name': 'Test User'})
        print("Creating test user")
        assert resp.status_code == 200
        self.test_user_id = resp.json()['addition']['id']

    def tearDown(self) -> None:
        resp = requests.post(f'{backend_url}/api/delete', json={'accountNumber': self.test_user_id})
        print("Removing test user")
        assert resp.status_code == 200
        self.test_user_id = None

    def test_guid_validation(self) -> None:
        resp = requests.post(f'{backend_url}/api/add', json={'accountNumber': '', 'addition': 100})
        assert resp.status_code == 400

    def test_invalid_guid(self) -> None:
        resp = requests.post(f'{backend_url}/api/add',
                             json={'accountNumber': '1ca8cdda-daa8-4133-921a-3fbe03f9c0c4', 'addition': 100})
        assert resp.status_code == 404

    def test_api_ping(self) -> None:
        url = f'{backend_url}/api/ping'
        resp = requests.get(url)

        assertion = {
            'status': 200,
            'result': True,
            'addition': 'Service works well.',
            'description': 'Current service status.'
        }

        assert resp.status_code == 200
        assert resp.json() == assertion

    def test_api_add_substruct(self) -> None:
        ApiTests._assert_balance(self.test_user_id, 0, 0)
        resp = requests.post(f'{backend_url}/api/add', json={'accountNumber': self.test_user_id, 'addition': 100})
        assert resp.status_code == 200
        ApiTests._assert_balance(self.test_user_id, 100, 0)
        resp = requests.post(f'{backend_url}/api/substract',
                             json={'accountNumber': self.test_user_id, 'substraction': 100})
        assert resp.status_code == 200
        ApiTests._assert_balance(self.test_user_id, 100, 100)

    @staticmethod
    def _assert_balance(account_id: str, balance: int, hold: int) -> None:
        status_url = f'{backend_url}/api/status'
        resp = requests.get(status_url, params={'accountNumber': account_id})

        assert resp.status_code == 200
        assert resp.json() == {
            'addition': {'balance': balance,
                         'hold': hold,
                         'id': account_id,
                         'ownerName': 'Test User',
                         'status': 'opened'},
            'description': 'Account status.',
            'result': True,
            'status': 200
        }
