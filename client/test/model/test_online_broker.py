import unittest
from unittest.mock import Mock
import sys
import os
import json

sys.path.append(os.path.abspath('../../src/'))
from model import online_broker


class TestOnlineBroker(unittest.TestCase):
	
	test_broker = None
	mock_mq = None
	mock_player = None
	player_stats = {'id': 'player.ID', 'name': 'Mr. Player', 'status': '', 'score': 0 }
	mock_opponent = {'sender': 'opponent inbox', 'name': 'Mr. Opponent',  'status': '', 'online': '', 'score': 123, 'total': 231, 'longest': 312}

	def __init__(self, *args, **kwargs):
		super(TestOnlineBroker, self).__init__(*args, **kwargs)
		self.mock_mq = Mock()
		self.mock_mq.connect.return_value = None
		self.mock_mq.send_message.return_value = True

		self.mock_player = Mock()
		self.mock_player.online.value = 'XXX'
		self.mock_player.inbox.value = ''
		self.mock_player.get_stats.return_value = self.player_stats

		self.test_broker = online_broker.OnlineBroker(self.mock_player, self.mock_mq)
		self.test_broker.opponent = self.mock_opponent
	
	def test_init(self):
		# check initial state
		self.assertIsNotNone(self.test_broker.player)
		self.assertIsNotNone(self.test_broker.mq)
		self.assertEqual(self.mock_player, self.test_broker.player)
		self.assertEqual(self.mock_mq, self.test_broker.mq)

	def test_set_player_available(self):
		
		# execute method
		self.test_broker.set_player_available()
		# assert expected changes
		self.assertEqual(self.mock_player.online, 'available')
		# mock and assert execution of landing_page()
		# assert execution of mq.send with info = {'status': 'AVAILABLE', 'recipient': 'SERVER'}
	
	def test_check_for_ready(self):
		# TODO: create fake messages for mock_mq.receive
		# null message, execute method
		# self.test_broker.check_for_ready()
		# assert player status didn't change and mq.send wasn't triggered
		# self.assertNotEqual(self.mock_player.online, 'ready')
		# good message, execute method
		# self.test_broker.check_for_ready()
		# assert player status changed to ready and mq.send triggered with correct package
		# self.assertEqual(self.mock_player.online, 'ready')
		pass
	
	def test_check_for_start(self):
		
		# TODO: plant null message, execute method, test response
		response = self.test_broker.check_for_start()
		self.assertIsNone(response)
		# TODO: plant good message with status START, execute method, test response
		# response = self.test_broker.check_for_ready()
		# self.assertNotNone(response)
		# self.assertTrue(type(response) == str())
	
	def test_negotiate_match(self):
		# manipulate value of player.online: connected, available, ready
		# connected
		self.mock_player.online = 'connected'
		# execute method and test
		response = self.test_broker.negotiate_match()
		self.assertIsNone(response)
		# TODO: assert execution of set_player_available
		# available
		self.mock_player.online = 'available'
		# execute method and test
		response = self.test_broker.negotiate_match()
		self.assertIsNone(response)
		# TODO: assert execution of check_for_ready
		# ready, no opponent
		self.mock_player.online = 'ready'
		# execute method and test
		response = self.test_broker.negotiate_match()
		self.assertIsNone(response)
		# TODO: assert execution of check_for_start, with null and good results
	
	def test_quit(self):
		# execute and test
		self.test_broker.quit()
		# TODO: assert message sent
		# TODO: assert mq.disconnect executed
		# mq is none
		self.test_broker.mq = None
		self.test_broker.quit()
		# TODO: assert nothing happened


if __name__ == '__main__':
	unittest.main()
