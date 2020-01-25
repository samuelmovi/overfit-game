import os
import json
import time

# Server message protocol:
#
# 1. Recipient: Player ID of recipient, used for filtering
# 2. ACTION: sender (SERVER or opponent player's ID), command (welcome, wait, ready, play)
# 3. Data: forwarded payload


class PullPubServer:
	
	online_players = []			# list of id values for all online players
	available_players = []		# list of id values for all online players waiting for a match
	matches = []			# ongoing matches: [ {'id_1': 'WAIT/READY/PLAY/won/lost', 'id_2': 'WAIT/READY/PLAY/won/lost'} ]
	
	def __init__(self, connector=None, db=None):
		if connector and db:
			self.mq = connector
			self.mq.setup()
			self.db = db
		else:
			print("[!!] No connector or db??\n")
			exit()
		
	def loop(self):
		print("[#] starting loop...")
		finished = False
		while not finished:
			try:
				message = self.mq.pull_receive_multi()
				if message:
					# print(f'[@] New message:\n\tFrom: {message}')
					sender = message[0].decode()
					info = json.loads(message[1])
					payload = json.loads(message[2])
					
					# check player is active
					if sender not in self.online_players:
						self.onboard_client(sender)
					else:
						# check status
						if info['status'] == 'WELCOME':
							self.handle_welcome(sender)
						elif info['status'] == 'AVAILABLE':
							self.handle_available(sender)
						elif info['status'] == 'READY':
							self.handle_ready(sender)
						elif info['status'] == 'PLAYING':
							self.handle_playing(info['recipient'], sender, payload)
						elif info['status'] == 'OVER':
							# someone lost
							self.handle_over(sender, payload)
						elif info['status'] == 'QUIT':
							# player disconnecting
							self.handle_quit(sender)
						else:
							print(f"[!!] unknown player status: {info['status']}")
			except KeyboardInterrupt:
				finished = True
			time.sleep(0.001)
		# os._exit(0)
		exit()
	
	def onboard_client(self, sender):
		# add player id to active_players
		self.online_players.append(sender)
		print(f"[#] User '{sender}' added to online_players")
		# send directly to landing
		# send landing page info
		new_info = {'status': 'WELCOME', 'sender': 'SERVER'}
		match_data = self.db.load_matches()
		self.mq.send(sender, new_info, match_data)
	
	def handle_welcome(self, sender):
		# if sender in available players, remove
		if sender in self.available_players:
			self.available_players.remove(sender)
			print(f"[#] User '{sender}' removed from available players")
		# send landing page info
		new_info = {'status': 'WELCOME', 'sender': 'SERVER'}
		match_data = self.db.load_matches()
		self.mq.send(sender, new_info, match_data)
	
	def handle_available(self, sender):
		# check for available players to match client with
		if len(self.available_players) > 0:
			print("[#] Pairing up available players...")
			player_1 = self.available_players.pop()
			player_2 = sender
			# send ready signal to both players
			for client in (player_1, player_2):
				new_info = {'sender': 'SERVER', 'status': 'READY'}
				self.mq.send(client, new_info, {})
			# add match to matches
			match = dict()
			match[player_1] = 'WAIT'
			match[player_2] = 'WAIT'
			self.matches.append(match)
		else:
			print("[#] No other players available...")
			# add to available_players
			self.available_players.append(sender)
			print(f"[#] Adding '{sender}' to available players")
			# respond
			new_info = {'sender': 'SERVER', 'status': 'WAIT'}
			self.mq.send(sender, new_info, {})
	
	def handle_ready(self, sender):
		# find corresponding match and set client as ready
		# send PLAY messages, with each other as sender
		for match in self.matches:
			if sender in match.keys():
				match[sender] = 'READY'
				# check if other player ready too
				c = 0
				for key in match.keys():
					if match[key] == 'READY':
						c += 1
				if c == 2:
					# both are ready, send status START
					players = list(match.keys())
					# inform one player
					new_info = {'sender': players[1], 'status': 'START'}
					self.mq.send(players[0], new_info, {})
					# inform the other
					new_info = {'sender': players[0], 'status': 'START'}
					self.mq.send(players[1], new_info, {})
				else:
					# not both players are ready
					break
	
	def handle_playing(self, recipient, sender, payload):
		# if playing, reformat and resend
		new_info = {'sender': sender, 'status': 'PLAYING'}
		self.mq.send(recipient, new_info, payload)
	
	def handle_over(self, sender, payload):
		# find match of sender
		loser = sender
		winner = None
		for match in self.matches:
			if loser in match.keys():
				# set loser
				match[loser] = 'LOST'
			# inform other client
			for key in match.keys():
				if key != loser:
					winner = key
					match[winner] = 'WON'
		# capture match data and create new db entry
		self.db.save_match(winner, loser)
		# forward message to winner
		new_info = {'sender': 'SERVER', 'status': 'OVER'}  # OVER commands signals victory
		self.mq.send(winner, new_info, payload)
	
	def handle_quit(self, sender):
		# remove player id from online_players
		self.online_players.remove(sender)
		print(f"[#] User '{sender}' removed from online players")
	

if __name__ == '__main__':
	pass

