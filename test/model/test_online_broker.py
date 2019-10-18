import unittest
from unittest.mock import Mock
import sys
import os
import json

sys.path.append(os.path.abspath('../../game/'))
from model import online_broker


class TestOnlineBroker(unittest.TestCase):
	
	mock_mq = None
	mock_player = None
	player_stats = {'sender': 'player inbox', 'name': 'Mr. Player', 'status': '', 'online': ''}
	mock_queue = 'player mock queue'
	test_broker = None
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
		print("[#] Testing method: OnlineBroker.__init__()")
		self.assertEqual(self.mock_player.connected, True)
		self.assertEqual(self.test_broker.player, self.mock_player)
	
	# def test_negotiate(self):
	# 	# possible online statuses: '' | available | challenger | accepted | itson | playing | over
	# 	# set object state
	# 	self.mock_player.online = 'qwerqeerq'
	# 	# execute method
	# 	outcome = self.test_broker.negotiate()
	# 	# assert expected outcome
	# 	self.assertEqual(None, outcome)
	#
	# 	# set object state
	# 	self.mock_player.online = ''
	# 	spy = Mock(spec=online_broker.OnlineBroker)
	# 	online_broker.OnlineBroker.check_for_available_player(spy)
	# 	# execute method
	# 	self.test_broker.negotiate()
	# 	# assert expected outcome
	# 	self.mock_mq.filter_sub_socket.assert_called_with('XXX')
	# 	self.assertEqual(0, self.test_broker.timer)
	# 	assert spy.mock_calls == [spy.call.check_for_available_player()]

	def test_check_for_available_player(self):
		# set object state
		self.mock_mq.sub_receive_multi.return_value = [
			'{"sender": "opponent inbox", "status": "XXX", "online": "available"}',
			'{"sender": "opponent inbox", "status": "XXX",  "online": "available"}'.encode()
		]
		# execute method
		outcome = self.test_broker.check_for_available_player()
		
		# assert expected outcome
		self.assertTrue(outcome)
		
		# BAD DATA
		self.mock_mq.sub_receive_multi.return_value = [
			'{"sender": "opponent inbox", "status": "XXX", "online": "qcwrqw"}',
			'{"sender": "opponent inbox", "status": "XXX",  "online": "rcqweqwe"}'.encode()
		]
		# execute method
		outcome = self.test_broker.check_for_available_player()
		
		# assert expected outcome
		self.assertFalse(outcome)
		
	def test_set_player_available(self):
		# check pre-state
		self.assertNotEqual(self.mock_player.online, 'available')
		# set object state
		self.mock_mq.push_send_multi.return_value = True
		# execute method
		outcome = self.test_broker.set_player_available()
		# assert expected outcome
		self.assertTrue(outcome)
		self.assertEqual(self.mock_player.online, "available")
		# assert if: self.mq.filter_sub_socket(self.player.ID)
	
		# BAD DATA
		self.mock_mq.push_send_multi.return_value = False
		# execute method
		outcome = self.test_broker.set_player_available()
		# assert expected outcome
		self.assertFalse(outcome)
		self.assertNotEqual(self.mock_player.online, "available")
	
	def test_check_for_challenger(self):
		# set object data
		self.mock_mq.sub_receive_multi.return_value = [
			'',
			'{"sender": "opponent inbox", "status": "XXX",  "online": "challenger"}'.encode()
		]
		message = ['XXX', json.dumps(self.player_stats)]
		for i in range(len(message)):
			message[i] = message[i].encode()
			
		# execute method
		outcome = self.test_broker.check_for_challenger()
		
		# assert expected outcome
		self.assertEqual(type(outcome), type({}))
		self.mock_mq.push_send_multi.assert_called_with(message)

		# BAD DATA
		self.mock_mq.sub_receive_multi.return_value = [
			'',
			'{"sender": "opponent inbox", "status": "XXX",  "online": "qwerqwe"}'.encode()
		]
		# execute method
		outcome = self.test_broker.check_for_challenger()
		
		# assert expected outcome
		self.assertEqual(type(outcome), type(None))
	
	def test_handle_challenger(self):
		pass

	def test_accept_challenge(self):
		# player online variable must be accepted
		# set object state
		self.mock_mq.push_send_multi.return_value = True

		# execute method
		outcome = self.test_broker.accept_challenge()
		
		# assert expected outcome
		self.assertTrue(outcome)
		self.assertEqual(self.mock_player.online, 'accepted')
		
		# BAD DATA
		self.mock_mq.push_send_multi.return_value = False
		
		# execute method
		outcome = self.test_broker.accept_challenge()
		
		# assert expected outcome
		self.assertFalse(outcome)
		self.assertNotEqual(self.mock_player.online, 'accepted')

	def test_is_it_on(self):
		# if message from inbox has status itson returns true
		# set object state
		self.mock_mq.sub_receive_multi.return_value = [
			'',
			'{"sender": "opponent inbox", "status": "XXX",  "online": "itson"}'.encode()
		]
		# execute method
		outcome = self.test_broker.is_it_on()
		
		# assert expected outcome
		self.assertEqual(outcome, True)
		
		# BAD DATA
		self.mock_mq.sub_receive_multi.return_value = [
			'{"sender": "test sender", "status": "XXX", "online": "qwerqwe"}',
			'{"sender": "opponent inbox", "status": "XXX",  "online": "qwerqwe"}'.encode()
		]
		self.assertEqual(self.test_broker.is_it_on(), False)

	def test_challenge_ap(self):
		# test that player status changes to challenger
		# set object state
		self.mock_mq.push_send_multi.return_value = True

		# execute method
		outcome = self.test_broker.challenge_ap()
		
		# assert expected outcome
		self.assertEqual(outcome, True)
		self.assertEqual(self.mock_player.online, "challenger")

	def test_check_challenge_response(self):
		# GOOD test
		# set object state
		self.mock_mq.sub_receive_multi.return_value = [
			'{"sender": "test sender", "status": "XXX", "online": "accepted"}',
			'{"sender": "opponent inbox", "status": "XXX",  "online": "accepted"}'.encode()
		]
		# execute method
		outcome = self.test_broker.check_challenge_response()
		
		# assert expected outcome
		self.assertEqual(outcome, True)
		
		# BAD test
		# set object state
		self.mock_mq.sub_receive_multi.return_value = [
			'{"sender": "test sender", "status": "XXX", "online": "refwegfcrew"}',
			'{"sender": "opponent inbox", "status": "XXX",  "online": "wercewrcwrc"}'.encode()
		]
		
		# execute method
		outcome = self.test_broker.check_challenge_response()
		
		# assert expected outcome
		self.assertEqual(outcome, False)

	def test_itson(self):
		# set object state
		
		# execute method
		self.test_broker.itson()
		
		# assert expected outcome
		self.assertEqual(self.test_broker.player.online, 'itson')

	def test_update_player_stats(self):
		# change player stats, call broker's recorded stats, update stats, and check they have been update
		# set object state
		old_stats = self.test_broker.player_stats
		# change player stats
		self.mock_player.get_stats.return_value = {'sender': 'test sender', 'status': 'online status', 'score': 123, 'total': 231, 'longest': 312}
		
		# execute method
		self.test_broker.update_player_stats()
		
		# assert expected outcome
		self.assertNotEqual(self.test_broker.player_stats, old_stats)


if __name__ == '__main__':
	unittest.main()
