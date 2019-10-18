import unittest
from unittest.mock import Mock
import sys
import os
# sys.path.append(os.path.abspath(sys.path[0]) + '/../../')
sys.path.append(os.path.abspath('../../game/'))
from model import zmq_connector


class TestMQ(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestMQ, self).__init__(*args, **kwargs)
		pass

	def test_connect(self):
		pass

	def test_declare_queue(self):
		pass

	def test_send_message(self):
		pass

	def test_get_messages(selfs):
		pass

	def test_get_last_message(self):
		pass

	def test_disconnect(self):
		pass


if __name__ == '__main__':
	unittest.main()
