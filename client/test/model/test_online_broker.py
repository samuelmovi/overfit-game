import unittest
from unittest.mock import Mock
import sys
import os

sys.path.append(os.path.abspath('../../src/'))
from model import online_broker


class TestOnlineBroker(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestOnlineBroker, self).__init__(*args, **kwargs)
		pass
	
	def test_init(self):
		# set state
		mock_mq = Mock()
		mock_player = Mock()
		# execute method
		test_broker = online_broker.OnlineBroker(mock_player, mock_mq)
		# check initial state
		self.assertIsNotNone(test_broker.player)
		self.assertIsNotNone(test_broker.mq)
		self.assertEqual(mock_player, test_broker.player)
		self.assertEqual(mock_mq, test_broker.mq)

	def test_set_player_available(self):
		# set state
		mock_mq = Mock()
		mock_player = Mock()
		test_broker = online_broker.OnlineBroker(mock_player, mock_mq)
		# execute method
		test_broker.set_player_available()
		# assert expected changes
		self.assertEqual(mock_player.online, 'available')
		self.assertTrue(mock_mq.send.called)

	def test_check_for_ready(self):
		# set state
		mock_mq = Mock()
		mock_player = Mock()
		test_broker = online_broker.OnlineBroker(mock_player, mock_mq)
		
		mock_mq.sub_receive_multi.return_value = [0, b'{"sender": "SERVER", "status": "READY"}', 1]
		# execute method
		test_broker.check_for_ready()
		# assert expected results
		self.assertEqual(mock_player.online, 'ready')
		self.assertTrue(mock_mq.send.called)
	
	def test_check_for_start(self):
		# set state
		mock_mq = Mock()
		mock_player = Mock()
		test_broker = online_broker.OnlineBroker(mock_player, mock_mq)
		
		# SCENARIO 1: no start
		mock_mq.sub_receive_multi.return_value = [0, b'{"sender": "SERVER", "status": "qwerwqe"}', 1]
		# execute method
		result = test_broker.check_for_start()
		# assert expected results
		self.assertIsNone(result)
		
		# SCENARIO 2: start
		mock_mq.sub_receive_multi.return_value = [0, b'{"sender": "OPPONENT_ID", "status": "START"}', 1]
		# execute method
		result = test_broker.check_for_start()
		# assert expected results
		self.assertIsNotNone(result)
		self.assertEqual(result, "OPPONENT_ID")
	
	def test_negotiate_match(self):
		# set state
		mock_mq = Mock()
		mock_player = Mock()
		test_broker = online_broker.OnlineBroker(mock_player, mock_mq)
		
		# SCENARIOS for player.online: connected, available, ready
		# connected
		test_broker.set_player_available = Mock()
		mock_player.online = 'connected'
		# execute method
		response = test_broker.negotiate_match()
		# assert expected outcome
		self.assertIsNone(response)
		self.assertTrue(test_broker.set_player_available.called)
		
		# available
		test_broker.check_for_ready = Mock()
		mock_player.online = 'available'
		# execute method
		response = test_broker.negotiate_match()
		# assert expected outcome
		self.assertIsNone(response)
		self.assertTrue(test_broker.check_for_ready.called)
		
		# ready
		test_broker.check_for_start = Mock()
		test_broker.check_for_start.return_value = 1
		mock_player.online = 'ready'
		# execute method
		response = test_broker.negotiate_match()
		# assert expected outcome
		self.assertIsNotNone(response)
		self.assertTrue(test_broker.check_for_start.called)

	def test_quit(self):
		# set state
		mock_mq = Mock()
		mock_player = Mock()
		test_broker = online_broker.OnlineBroker(mock_player, mock_mq)
		
		# execute method
		test_broker.quit()
		
		# assert expected outcome
		self.assertTrue(mock_mq.send.called)
		self.assertTrue(mock_mq.disconnect.called)


if __name__ == '__main__':
	unittest.main()
