import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src/'))
from model import zmq_client
from unittest.mock import Mock


class TestMQ(unittest.TestCase):

	test_mq = None

	def __init__(self, *args, **kwargs):
		super(TestMQ, self).__init__(*args, **kwargs)
		pass
	
	def test_start(self):
		# set state
		host = 'qwerqew'
		topic = 'asfdadsf'
		
		test_mq = zmq_client.ZmqConnector()
		
		test_mq.client_auth = Mock()
		test_mq.connect_push = Mock()
		test_mq.connect_sub = Mock()
		test_mq.filter_sub_socket = Mock()
		test_mq.check_folder_structure = Mock()
		test_mq.check_folder_structure.return_value = True
		
		# execute method
		test_mq.start(host, topic)
		
		# assert expected results
		self.assertTrue(test_mq.client_auth.called)
		self.assertTrue(test_mq.connect_push.called)
		self.assertTrue(test_mq.connect_sub.called)
		self.assertTrue(test_mq.filter_sub_socket.called)
		self.assertEqual(test_mq.host, host)
		self.assertIsNotNone(test_mq.context)
	
	def test_send(self):
		# set state
		test_mq = zmq_client.ZmqConnector()
		test_mq.push_send_multi = Mock()
		
		# execute method
		test_mq.send('sender', {"info": "nada"}, {})
		
		# assert expected outcome
		self.assertTrue(test_mq.push_send_multi.called)
	
	# def test_check_folder_structure(self):
	# 	# TODO: find workaround issue with disparate cwd's affecting file and folder read
	# 	# set object state
	# 	test_mq = zmq_client.ZmqConnector()
	# 	test_mq.base_dir = ''
	# 	# execute method
	# 	result = test_mq.check_folder_structure()
	# 	# assert expected outcome
	# 	self.assertIsNotNone(result)
	# 	self.assertTrue(result)

	def test_disconnect(self):
		# set state
		test_mq = zmq_client.ZmqConnector()
		test_mq.context = Mock()
		test_mq.pusher = Mock()
		test_mq.subscriber = Mock()
		
		# execute method
		test_mq.disconnect()
		
		# assert expected results
		self.assertTrue(test_mq.context.term.called)
		self.assertTrue(test_mq.pusher.close.called)
		self.assertTrue(test_mq.subscriber.close.called)
		

if __name__ == '__main__':
	unittest.main()
