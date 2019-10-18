import unittest
from unittest.mock import Mock
import sys
import os
sys.path.append(os.path.abspath('../..'))
from model import online_broker


class TestOnlineBroker(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestOnlineBroker, self).__init__(*args, **kwargs)
		self.mock_mq = Mock()
		self.mock_mq.connect.return_value = None
		self.mock_mq.send_message.return_value = True

		self.mock_player = Mock()
		self.mock_player.online.value = 'XXX'
		self.mock_player.inbox.value = ''
		self.mock_player.get_stats.return_value = {'sender': 'player inbox', 'name': 'Mr. Player', 'status': 'online status', 'score': 123, 'total': 231, 'longest': 312}

		self.opponent = {'sender': 'opponent inbox', 'name': 'Mr. Opponent', 'status': 'online status', 'score': 123, 'total': 231, 'longest': 312}
		self.mock_queue = 'player mock queue'
		self.my_broker = online_broker.OnlineBroker(self.mock_player, self.mock_mq, self.mock_queue)

	def test_init(self):
		print("[#] Testing method: OnlineBroker.__init__()")
		self.assertEqual(self.mock_player.connected, True)
		self.assertEqual(self.my_broker.player, self.mock_player)
	'''
	def test_negotiate(self):
		pass

	def test_check_for_available_player(self):
		pass

	def test_set_player_available(self):
		pass

	def test_check_for_challenger(self):
		pass
	'''
	def test_handle_challenger(self):
		pass

	def mock_send_message(self, queue, message):
		if queue == self.opponent['sender'] and self.opponent.keys() == message.keys():
			return True
		else:
			return False

	def test_accept_challenge(self):
		# player online variable must be accepted
		# message with correct queue string and message with all required fields
		print("[#] Testing method: OnlineBroker.accept_challenge()")
		self.mock_mq.send_message = self.mock_send_message
		self.my_broker.accept_challenge()
		self.assertEqual(self.mock_player.online, 'accepted')

	def mock_get_messages(self, queue):
		if queue == self.mock_queue:
			return self.fake_message_list
		else:
			return False

	def test_is_it_on(self):
		# if message from inbox has status itson returns true
		print("[#] Testing method: OnlineBroker.is_it_on()")
		self.mock_mq.get_messages = self.mock_get_messages
		self.fake_message_list = [
			'{"sender": "test sender", "status": "itson", "score": 123, "total": 231, "longest": 312}']
		self.assertEqual(self.my_broker.is_it_on(), True)
		self.fake_message_list = [
			'{"sender": "test sender", "status": "XXX", "score": 123, "total": 231, "longest": 312}']
		self.assertEqual(self.my_broker.is_it_on(), False)

	def test_challenge_ap(self):
		# test that player status changes to challenger
		print("[#] Testing method: OnlineBroker.challenge_ap()")
		self.mock_player.name = 'TEST NAME'
		self.assertEqual(self.my_broker.challenge_ap(), True)
		self.assertEqual(self.mock_player.online, 'challenger')

	def test_check_challenge_response(self):
		print("[#] Testing method: OnlineBroker.check_challenge_response()")
		self.my_broker.opponent = {"sender": "test sender", "status": "empty", "score": 123, "total": 231, "longest": 312}
		# create no good messages and assert False
		fake_message_list = ['{"sender": "test sender", "status": "not accepted", "score": 123, "total": 231, "longest": 312}']
		self.mock_mq.get_messages.return_value = fake_message_list
		self.assertEqual(self.my_broker.check_challenge_response(), False)
		# create good message and assert True
		fake_message_list = ['{"sender": "test sender", "status": "accepted", "score": 123, "total": 231, "longest": 312}']
		self.mock_mq.get_messages.return_value = fake_message_list
		self.assertEqual(self.my_broker.check_challenge_response(), True)

	def test_itson(self):
		print("[#] Testing method: OnlineBroker.itson()")
		self.my_broker.itson()
		self.assertEqual(self.my_broker.player.online, 'itson')

	def test_update_player_stats(self):
		# change player stats, call broker's recorded stats, update stats, and check they have been update
		print("[#] Testing method: OnlineBroker.update_player_stats()")
		# change player stats
		mock_stats = {'sender': 'test sender', 'status': 'online status', 'score': 123, 'total': 231, 'longest': 312}
		self.mock_player.get_stats.return_value = mock_stats
		#  call broker's recorded stats
		old_stats = self.my_broker.player_stats
		# update stats
		self.my_broker.update_player_stats()
		# check they have been updated
		self.assertNotEqual(self.my_broker.player_stats, old_stats)


if __name__ == '__main__':
	unittest.main()
