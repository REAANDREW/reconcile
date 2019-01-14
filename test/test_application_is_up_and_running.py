import urllib
from flask_testing import LiveServerTestCase
from skeleton_python_system import create_app as new_app

# Testing with LiveServer
class MyTest(LiveServerTestCase):
    # if the create_app is not implemented NotImplementedError will be raised
    def create_app(self):
        app = new_app()
        app.config["TESTING"] = True
        return app

    def test_flask_application_is_up_and_running(self):
        url = self.get_server_url()

        req = urllib.request.Request(url=url)
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
