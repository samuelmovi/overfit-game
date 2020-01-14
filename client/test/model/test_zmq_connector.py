import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src/'))
from model import zmq_client


class TestMQ(unittest.TestCase):

	test_mq = None

	def __init__(self, *args, **kwargs):
		super(TestMQ, self).__init__(*args, **kwargs)
		pass
	
	def test_init(self):
		# set object state
		# execute method
		self.test_mq = zmq_client.ZmqConnector()
		# assert expected result
		self.assertEqual('127.0.0.1', self.test_mq.HOST)
		self.assertIsNotNone(self.test_mq.context)
		
		# execute method
		self.test_mq = zmq_client.ZmqConnector('172.17.0.2')
		# assert expected result
		self.assertEqual('172.17.0.2', self.test_mq.HOST)
		self.assertIsNotNone(self.test_mq.context)
	
	def test_check_folder_structure(self):
		# set object state
		self.test_mq = zmq_client.ZmqConnector()
		# execute method
		outcome = self.test_mq.check_folder_structure()
		# assert expected outcome
		self.assertTrue(outcome)
	
	# TODO: figure out how to mock ThreadAuthenticator
	# def test_server_auth(self):
	# 	# set object state
	#
	# 	# execute method
	#
	# 	# assert expected outcome
	#

	# TODO: test execution without errors
	# def test_client_auth(self):
	# 	# set object state
	#
	# 	# execute method
	#
	# 	# assert expected outcome


if __name__ == '__main__':
	unittest.main()
