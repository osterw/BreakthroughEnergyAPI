import unittest
from fastapi.testclient import TestClient
from src.main import app


class TestHelloWorld(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_hello_world(self):
        response = self.client.get("/helloworld")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '"Hello World!"')


if __name__ == "__main__":
    unittest.main()
