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

	timer = None

	def __init__(self, player, zmq):
		print("[broker] Initializing online game broker...")
		self.mq = zmq
		self.mq.setup()
		try:
			self.player = player
			self.player.online = 'connected'
			self.mq.filter_sub_socket(self.player.ID)		# filter sub responses to player ID
		except Exception as e:
			print("[broker!] Error starting online game: {}".format(e))
			traceback.print_exc()
	
	def landing_page(self):
		# send WELCOME command and get back the data to display in landing page
		message = []
		sender = self.player.ID
		message.append(sender)
		info = {'status': 'WELCOME', 'recipient': 'SERVER'}
		message.append(json.dumps(info))
		message.append(json.dumps(dict()))
		self.mq.push_send_multi(message)
		# maybe a little wait
		response = self.mq.sub_receive_multi()
		return response
	
	def set_player_available(self):
		self.player.online = 'available'
		new_message = []
		sender = self.player.ID
		new_message.append(sender)
		info = {'status': 'AVAILABLE', 'command': 'FIND', 'sender': 'SERVER'}
		new_message.append(json.dumps(info))
		payload = dict() 	# empty payload, for compliance
		new_message.append(json.dumps(payload))
		self.mq.push_send_multi(new_message)
		# go to landing page
		self.landing_page()

	def check_for_ready(self):
		# read from subscription and check
		response = self.mq.sub_receive_multi()
		if response:
			# check for READY status
			info = response[1]
			if info['sender'] == 'SERVER' and info['status'] == 'READY':
				self.player.online = 'ready'
				# respond ready
			pass
	
	def check_for_play(self):
		# read from subscription and check
		response = self.mq.sub_receive_multi()
		if response:
			# check for PLAY status
			info = response[1]
			if info['status'] == 'PLAY':
				# return opponent's id
				return info['sender']
			else:
				return None

	# def timeout(self):
	# 		if (timeit.default_timer() - self.timer) > 5:
	# 			return True
	# 		else:
	# 			return False

	def negotiate_match(self):
		if self.player.online == 'connected':
			self.set_player_available()
			self.timer = timeit.default_timer()
		elif self.player.online == 'available':
			self.timer += 1
			self.check_for_ready()
		elif self.player.online == 'ready':
			self.timer = timeit.default_timer()
			opponent = self.check_for_play()
			if opponent:
				return opponent
		return None
	
	# during game
	def update_player_stats(self):
		current_stats = self.player.get_stats()
		if current_stats != self.player_stats:
			print('[broker] Updating opponent about player stats')
			self.player_stats = current_stats
			message = [self.opponent['sender'], json.dumps(self.player_stats)]
			for i in range(len(message)):
				message[i] = message[i].encode()
			self.mq.push_send_multi(message)


if __name__ == '__main__':
	pass
