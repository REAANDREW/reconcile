import urllib2
from flask import Flask
from flask_testing import LiveServerTestCase
from skeleton_pyton_system import app

# Testing with LiveServer


class MyTest(LiveServerTestCase):
  # if the create_app is not implemented NotImplementedError will be raised
  def create_app(self):
    app.config['TESTING'] = True
    return app

  def test_flask_application_is_up_and_running(self):
    url = self.get_server_url()
    response = urllib2.urlopen(url)
    self.assertEqual(response.code, 200)
