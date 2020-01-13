import os
import json
from models import Player, Match


# Server message protocol:
#
# 1. Recipient: Player ID of recipient, used for filtering
# 2. ACTION: sender (SERVER or opponent player's ID), command (welcome, wait, ready, play)
# 3. Data: forwarded payload


class PullPubServer:
	
	active_players = []		# id values for all active players
	available_players = []

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
		stop_me = False
		while not stop_me:
			try:
				message = self.mq.pull_receive_multi()
				sender = message[0]
				info = message[1]
				payload = message[2]
				new_message = []
				# check player is active
				if sender not in self.active_players:
					# create new player
					new_player = Player(token=sender)
					self.db.save_player(new_player)
					# add player id to active_players
					self.active_players.append(new_player.token)
					
					# send data to new player
					recipient = new_player.token
					new_message.append(recipient)
					info = {'command': 'WELCOME', 'sender': 'SERVER'}
					new_message.append(json.dumps(info))
					# prepare landing page data
					payload = self.db.load_matches()
					new_message.append(json.dumps(payload))
					
					self.mq.pub_send_multi(message)
				else:
					# check status
					if info['status'] == 'PLAYING':
						# if playing, reformat and resend
						# add recipient to new message
						new_message.append(info['recipient'])
						# add action to new message
						new_action = {'sender': message[0], 'command': 'PLAY'}
						new_message.append(json.dumps(new_action))
						# add match data
						new_message.append(payload)
						self.mq.pub_send_multi(new_message)
					elif info['status'] == 'OVER':
						# capture match data and create new db entry
						pass
					elif info['status'] == 'QUIT':
						# remove player id from active_players
						pass
					else:
						pass
			except KeyboardInterrupt:
				stop_me = True
		os._exit(0)


if __name__ == '__main__':
	pass

