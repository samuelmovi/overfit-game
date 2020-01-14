import os
import json


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
		finished = False
		while not finished:
			try:
				message = self.mq.pull_receive_multi()
				if message:
					sender = message[0]
					info = message[1]
					payload = message[2]
					new_message = []
					# check player is active
					if sender not in self.online_players:
						# add player id to active_players
						self.online_players.append(sender)
					else:
						# check status
						if info['status'] == 'WELCOME':
							# send landing page info
							recipient = sender
							new_message.append(recipient)
							new_info = {'command': 'WELCOME', 'sender': 'SERVER'}
							new_message.append(json.dumps(new_info))
							# prepare landing page data
							payload = self.db.load_matches()
							new_message.append(json.dumps(payload))
							self.mq.pub_send_multi(message)
						elif info['status'] == 'AVAILABLE':
							# check for available players to match client with
							if len(self.available_players):
								# send ready signal to both players
								for id in (self.available_players.pop(), sender):
									new_message = list()
									new_message.append(id)
									new_info = {'sender': 'SERVER', 'command': 'READY'}
									new_message.append(json.dumps(new_info))
									new_message.append(json.dumps(dict()))
									self.mq.pub_send_multi(new_message)
							else:
								# add to available_players
								self.available_players.append(sender)
								# respond
								new_message = list()
								new_message.append(sender)
								new_info = {'sender': 'SERVER', 'command': 'WAIT'}
								new_message.append(json.dumps(new_info))
								new_message.append(json.dumps(dict()))
								self.mq.pub_send_multi(new_message)
						
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
										players = match.keys()
										# inform one player
										new_message = list()
										new_message.append(players[0])
										new_info = {'sender': players[1], 'command': 'PLAY'}
										new_message.append(json.dumps(new_info))
										self.mq.pub_send_multi(new_message)
										# inform the other
										new_message = list()
										new_message.append(players[1])
										new_info = {'sender': players[0], 'command': 'PLAY'}
										new_message.append(json.dumps(new_info))
										self.mq.pub_send_multi(new_message)
									else:
										continue
										
						elif info['status'] == 'PLAYING':
							# if playing, reformat and resend
							# add recipient to new message
							new_message = list()
							new_message.append(info['recipient'])
							# add action to new message
							new_action = {'sender': message[0], 'command': 'PLAY'}
							new_message.append(json.dumps(new_action))
							# add match data
							new_message.append(payload)
							self.mq.pub_send_multi(new_message)
						
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
				finished = True
		os._exit(0)


if __name__ == '__main__':
	pass

