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
	
	def test_start(self):
		# set state
		host = 'qwerqew'
		topic = 'asfdadsf'
		
		# create object and test
		test_mq = zmq_client.ZmqConnector()
		self.assertEquals(test_mq.host, '')
		self.assertIsNone(test_mq.context)
		self.assertIsNone(test_mq.pusher)
		self.assertIsNone(test_mq.subscriber)
		
		# execute method and test
		test_mq.start(host, topic)
		self.assertIsNotNone(test_mq.context)
		self.assertEquals(test_mq.host, host)
		self.assertIsNotNone(test_mq.base_dir)
		# should mock check_folder_structure
		# check execution of methods: client_auth, connect_push, connect_sub, filter_sub_socket [with topic]

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
