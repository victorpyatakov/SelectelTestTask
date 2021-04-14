import json
import requests
from app import app
import unittest


class BasicTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_post_dif(self):
        data = {
            "args": [1, 2, 3, 4],
            "last_arg_multiplier": 2,
            "reverse": "False"
        }
        url = "http://0.0.0.0:5005/api/dif"
        resp = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        expect = {
            "result": -12
        }
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(expect, resp.json())

    def test_post_sum(self):
        data = {
            "args": [1, 2, 3, 4],
            "last_arg_multiplier": 2,
            "reverse": "False"
        }
        url = "http://0.0.0.0:5005/api/sum"
        resp = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        expect = {
            "result": 14
        }
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(expect, resp.json())

    def test_post_prod(self):
        data = {
            "args": [1, 2, 3, 4],
            "last_arg_multiplier": 2,
            "reverse": "False"
        }
        url = "http://0.0.0.0:5005/api/prod"
        resp = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        expect = {
            "result": 48
        }
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(expect, resp.json())

    def test_post_div(self):
        data = {
            "args": [1, 2, 3, 4],
            "last_arg_multiplier": 3,
            "reverse": "True"
        }
        url = "http://0.0.0.0:5005/api/div"
        resp = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        expect = {
            "result": 2.0
        }
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(expect, resp.json())

    def test_get_rooms(self):
        url = "http://0.0.0.0:5005/api/rooms"
        resp = requests.get(url)
        expect = {
            "rooms": [
                {
                    "id": 1,
                    "name": "Room1"
                },
                {
                    "id": 2,
                    "name": "Room2"
                },
                {
                    "id": 3,
                    "name": "Room3"
                },
                {
                    "id": 4,
                    "name": "Room4"
                }
            ]
        }
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(expect, resp.json())

    def test_get_customers(self):
        url = "http://0.0.0.0:5005/api/customers"
        resp = requests.get(url)
        expect = {
            "customers": [
                {
                    "id": 1,
                    "name": "Client-1"
                },
                {
                    "id": 2,
                    "name": "Client-2"
                },
                {
                    "id": 3,
                    "name": "Client-3"
                }
            ]
        }
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(expect, resp.json())

    def test_get_rack(self):
        url = "http://0.0.0.0:5005/api/racks/1"
        resp = requests.get(url)
        expect = {
            "customer_id": 1,
            "id": 1,
            "name": "Rack1",
            "room_id": 1,
            "size": 42,
            "state": "occupied"
        }
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(expect, resp.json())

    def test_get_busy_racks(self):
        url = "http://0.0.0.0:5005/api/busy_racks"
        resp = requests.get(url)
        expect = {
            "0": {
                "customer_name": "Client-1",
                "rack_id": 1,
                "rack_name": "Rack1",
                "room_name": "Room1"
            },
            "1": {
                "customer_name": "Client-2",
                "rack_id": 2,
                "rack_name": "Rack2",
                "room_name": "Room1"
            },
            "2": {
                "customer_name": "Client-1",
                "rack_id": 4,
                "rack_name": "Rack4",
                "room_name": "Room2"
            },
            "3": {
                "customer_name": "Client-1",
                "rack_id": 7,
                "rack_name": "Rack7",
                "room_name": "Room3"
            },
            "4": {
                "customer_name": "Client-1",
                "rack_id": 8,
                "rack_name": "Rack8",
                "room_name": "Room3"
            }
        }
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(expect, resp.json())

    def test_get_racks_with_max_size(self):
        url = "http://0.0.0.0:5005/api/racks_with_max_size"
        resp = requests.get(url)
        expect = {
            "0": {
                "rack_id": 6,
                "rack_size": 47,
                "room_id": 3
            },
            "1": {
                "rack_id": 4,
                "rack_size": 42,
                "room_id": 2
            },
            "2": {
                "rack_id": 1,
                "rack_size": 42,
                "room_id": 1
            }
        }
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(expect, resp.json())

    def test_get_customers_in_rooms(self):
        url = "http://0.0.0.0:5005/api/customers_in_rooms"
        resp = requests.get(url)
        expect = {
            "0": {
                "customers_id": [
                    1,
                    2
                ],
                "room_id": 1,
                "room_name": "Room1"
            },
            "1": {
                "customers_id": [
                    1
                ],
                "room_id": 2,
                "room_name": "Room2"
            },
            "2": {
                "customers_id": [
                    1
                ],
                "room_id": 3,
                "room_name": "Room3"
            }
        }
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(expect, resp.json())


if __name__ == '__main__':
    unittest.main()
