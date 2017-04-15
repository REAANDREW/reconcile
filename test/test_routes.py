import os
import unittest
import tempfile
from skeleton_python_system import app


class FlaskrTestCase(unittest.TestCase):

  def setUp(self):
    self.app = app.test_client()

  def test_root(self):
    rv = self.app.get('/')
    assert b'Skeleton' in rv.data


if __name__ == '__main__':
  unittest.main()
