import os
import unittest
import tempfile
from reconcile import app


class FlaskrTestCase(unittest.TestCase):

  def setUp(self):
    self.app = app.test_client()

  def test_root(self):
    rv = self.app.get('/')
    assert b'Reconcile' in rv.data


if __name__ == '__main__':
  unittest.main()
