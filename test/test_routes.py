import unittest
from skeleton_python_system import create_app


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.app = app.test_client()

    def test_root(self):
        response = self.app.get("/")
        assert b"Skeleton" in response.data


if __name__ == "__main__":
    unittest.main()
