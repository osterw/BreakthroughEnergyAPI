import unittest
from fastapi.testclient import TestClient
from src.main import app, flatten


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_hello_world_default(self):
        response = self.client.get("/helloworld")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Hello World!")

    def test_hello_world_json(self):
        response = self.client.get(
            "/helloworld",
            headers={"Accept": "application/json"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello World!"})

    def test_hello_world_with_timezone(self):
        response = self.client.get("/helloworld?tz=America/New_York")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello World! It is", response.json())
        self.assertIn("in timezone: America/New_York", response.json())

    def test_unravel_endpoint(self):
        test_data = {
            "key1": {"keyA": ["foo", 0, "bar"]},
            "some other key": 2,
            "finally": "end",
        }
        expected = [
            "key1", "keyA", "foo", 0, "bar",
            "some other key", 2, "finally", "end"
        ]
        response = self.client.post("/unravel", json=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_unravel_single_string(self):
        test_data = "test"
        expected = ["test"]
        response = self.client.post("/unravel", json=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_unravel_list(self):
        test_data = [1, "test", 2]
        expected = test_data
        response = self.client.post("/unravel", json=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)


class TestFlattenJson(unittest.TestCase):
    def test_flatten(self):
        test_cases = [
            ({"a": 1}, ["a", 1]),
            ({"a": [1, 2]}, ["a", 1, 2]),
            ({"a": {"b": "c"}}, ["a", "b", "c"]),
        ]
        
        for input_data, expected in test_cases:
            with self.subTest(input=input_data):
                self.assertEqual(flatten(input_data), expected)


if __name__ == "__main__":
    unittest.main()
