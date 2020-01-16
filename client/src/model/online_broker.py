import json
import traceback
import time
import timeit


# Client message protocol:
#
# 1. ID: Player ID (random string created by online broker)
# 2. ACTION: status, recipient.
# 3. MATCH: relevant player match data


# Server message protocol:
#
# 1. Recipient: Player ID of recipient, used for filtering
# 2. ACTION: sender (SERVER or opponent player's ID), command (welcome, wait, ready, play, winner)
# 3. Data: forwarded payload, or empty dictionary

class OnlineBroker:

	mq = None
	opponent = {}
	player = {}
	counter = 0
	no_challenger = True
	challenging = False
	player_stats = {}

	# timer = None

	def __init__(self, player, zmq):
		print("[broker] Initializing online game broker...")
		self.mq = zmq
		self.player = player
	
	def landing_page(self):
		# print("[#] Retrieving landing page data...")
		try:
			response = self.mq.sub_receive_multi()
			return response
		except Exception as e:
			print(f"[broker!] Error landing_page: {e}")
		return None
	
	def set_player_available(self):
		self.player.online = 'available'
		info = {'status': 'AVAILABLE', 'recipient': 'SERVER'}
		self.mq.send(self.player.ID, info, {})
		# go to landing page
		self.landing_page()

	def check_for_ready(self):
		# read from subscription and check
		response = self.mq.sub_receive_multi()
		if response:
			# check for READY status
			info = json.loads(response[1])
			if info['sender'] == 'SERVER' and info['status'] == 'READY':
				self.player.online = 'ready'
				my_info = {'status': 'READY', 'recipient': 'SERVER'}
				self.mq.send(self.player.ID, my_info, {})
	
	def check_for_start(self):
		# read from subscription and check
		response = self.mq.sub_receive_multi()
		if response:
			# check for START status
			info = json.loads(response[1])
			if info['status'] == 'START':
				# return opponent's id
				return info['sender']
			else:
				return None

	def negotiate_match(self):
		if self.player.online == 'connected':
			self.set_player_available()
		elif self.player.online == 'available':
			self.check_for_ready()
		elif self.player.online == 'ready':
			opponent = self.check_for_start()
			if opponent:
				return opponent
		else:
			print(f"[!!!] Player online status: {self.player.online}")
		return None
	
	def quit(self):
		if self.mq is not None:
			# disconnect from server with QUIT message
			sender = self.player.ID
			info = {'status': 'QUIT', 'recipient': 'SERVER'}
			self.mq.send(sender, info, {})
			time.sleep(0.1)
			# close sockets
			self.mq.disconnect()


if __name__ == '__main__':
	pass
