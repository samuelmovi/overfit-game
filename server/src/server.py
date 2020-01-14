import os
import json
from models import Player, Match


# Server message protocol:
#
# 1. Recipient: Player ID of recipient, used for filtering
# 2. ACTION: sender (SERVER or opponent player's ID), command (welcome, wait, ready, play)
# 3. Data: forwarded payload


class PullPubServer:
	
	online_players = []			# list of id values for all online players
	available_players = []		# list of id values for all online players waiting for a match
	matches = []
	# list of ongoing matches:
	# { 'player_1_id': 'status'},
	#   'player_2_id': 'status'},
	# }
	# values for status: playing, won, lost
	
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
				if sender not in self.online_players:
					# create new player
					new_player = Player(token=sender)
					self.db.save_player(new_player)
					# add player id to active_players
					self.online_players.append(new_player.token)
					
					# send response to new player
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
					elif info['status'] == 'WAITING':
						# ignore ???
						continue
					elif info['status'] == 'READY':
						# find corresponding match and set client as ready
						# TODO: this code doesn't look efficient, should be improved
						for match in self.matches:
							if sender in match.keys():
								match[sender] = 'READY'
								# check if both are ready
								c = 0
								for key in match.keys():
									if match[key] == 'READY':
										c += 1
								if c == 2:
									# both are ready, send command PLAY
									for player in match.keys():
										new_message = list()
										new_message.append(player)
										new_info = {'sender': 'SERVER', 'command': 'PLAY'}
										new_message.append(json.dumps(new_info))
										self.mq.pub_send_multi(new_message)
								else:
									continue
					elif info['status'] == 'OVER':		# someone lost
						# find match of sender
						loser = sender
						winner = None
						for match in self.matches:
							if loser in match.keys():
								# set loser
								match[loser] = 'LOSER'
								# inform other client
							for key in match.keys():
								if key != loser:
									winner = key
									match[winner] = 'WINNER'
						# capture match data and create new db entry
						self.db.save_match(winner, loser)
						# forward message to winner
						new_message = list()
						new_info = {'sender': 'SERVER', 'command': 'OVER'}		# OVER commands signals victory
						new_message.append(json.dumps(new_info))
						self.mq.pub_send_multi(new_message)
						continue
					elif info['status'] == 'QUIT':		# player disconnecting
						# remove player id from online_players
						self.online_players.pop(sender)
						continue
					else:
						pass
			except KeyboardInterrupt:
				stop_me = True
		os._exit(0)


if __name__ == '__main__':
	pass

