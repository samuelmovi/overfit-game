import json
import traceback
import time


class OnlineBroker:

	mq = None
	opponent = {}
	player = {}
	counter = 0
	no_challenger = True
	challenging = False
	player_stats = {}

	PUSH_PORT = '5555'
	SUB_PORT = '5556'

	timer = None

	def __init__(self, player, zmq):
		print("[broker] Initializing online game broker...")
		self.mq = zmq
		self.mq.check_folder_structure()
		self.mq.client_auth()
		self.mq.connect_push(self.PUSH_PORT)
		self.mq.connect_sub(self.SUB_PORT)
		try:
			self.player = player
			self.player.connected = True
		except Exception as e:
			print("[broker!] Error starting online game: {}".format(e))
			traceback.print_exc()

	def timeout(self):
		if self.timer > 60:
			return True
		else:
			return False

	def negotiate(self):
		if self.player.online == '':
			# filter the subscription to get APs
			self.mq.filter_sub_socket('XXX')

			if self.check_for_available_player() is True:
				self.mq.filter_sub_socket(self.player.ID)
				self.player.online = 'challenger'
				self.challenge_ap()
			else:
				self.set_player_available()
			self.timer = 0
		elif self.player.online == 'available':
			self.timer += 1
			self.handle_challenger()
		elif self.player.online == 'challenger':
			self.timer += 1
			if self.check_challenge_response() is True:
				self.itson()
		elif self.player.online == 'accepted':
			self.timer += 1
			if self.is_it_on() is True:
				return self.opponent
		elif self.player.online == 'itson':
			self.timer += 1
			return self.opponent
		return None

	def check_for_available_player(self):
		time.sleep(0.2)
		print("[broker] Looking for available players...")
		response = self.mq.sub_receive_multi()
		self.mq.unfilter_sub_socket('XXX')
		if response is not None:
			print("[#] Available player: {}".format(response))
			self.opponent = json.loads(response[1].decode())
			if self.opponent['online'] == 'available':
				print('[broker] Got 1 available player: {}'.format(self.opponent))
				return True
		else:
			print('[broker] No available players: {}'.format(type(response)))
			return False

	def set_player_available(self):
		print('[broker] Setting player available...')
		self.mq.filter_sub_socket(self.player.ID)
		message = ['XXX', json.dumps(self.player.get_stats())]
		for i in range(len(message)):
			message[i] = message[i].encode()
		if self.mq.push_send_multi(message) is True:
			self.player.online = 'available'
			return True
		else:
			self.player.online = ''
			return False
			
	def check_for_challenger(self):
		print("[broker] Resending message as available...")
		message = ['XXX', json.dumps(self.player.get_stats())]
		for i in range(len(message)):
			message[i] = message[i].encode()
		self.mq.push_send_multi(message)
		time.sleep(0.5)
		print('[broker] Checking for challengers...')
		# check for responses
		message = self.mq.sub_receive_multi()
		if message is not None:
			print("[broker] Got 1 message: {}".format(message))
			opponent = json.loads(message[1].decode())
			if opponent['online'] == 'challenger':
				print("[broker] Got 1 challenger!")
				return opponent
		else:
			# print("[broker] problem checking for challenger")
			return None

	def handle_challenger(self,):
		opponent = self.check_for_challenger()
		if opponent is not None:
			self.opponent = opponent
			self.no_challenger = False
			self.accept_challenge()

	def accept_challenge(self):
		message = [self.opponent['sender'], json.dumps(self.player.get_stats())]
		for i in range(len(message)):
			message[i] = message[i].encode()
		if self.mq.push_send_multi(message):
			print('[broker] Challenged received and accepted!')
			self.player.online = 'accepted'
			return True
		else:
			self.player.online = 'available'
			return False

	def is_it_on(self):
		print('[broker] Is it ON??')
		# check for responses
		response = self.mq.sub_receive_multi()
		if response is not None:
			response = json.loads(response[1].decode())
			if response['online'] == 'itson':
				return True
		return False

	# if there is an available player in queue
	def challenge_ap(self):
		print('[broker] Challenging available player...')
		message = [self.opponent['sender'], json.dumps(self.player.get_stats())]
		for i in range(len(message)):
			message[i] = message[i].encode()
		if self.mq.push_send_multi(message) is True:
			self.player.online = 'challenger'
			return True
		else:
			return False

	def check_challenge_response(self):
		self.challenge_ap()
		time.sleep(0.5)
		print('[broker] Waiting for challenge accepted...')
		response = self.mq.sub_receive_multi()
		if response is not None:
			message = json.loads(response[1].decode())
			if message['sender'] == self.opponent['sender'] and message['online'] == 'accepted':
				self.opponent = message
				return True
			else:
				return False
		else:
			return False

	def itson(self):
		self.player.online = 'itson'
		message = [self.opponent['sender'], json.dumps(self.player.get_stats())]
		for i in range(len(message)):
			message[i] = message[i].encode()

		self.mq.push_send_multi(message)

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
