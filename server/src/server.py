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
					# print(f'[@] New message:\n\tFrom: {message}')
					sender = message[0].decode()
					info = json.loads(message[1])
					payload = json.loads(message[2])
					
					# check player is active
					if sender not in self.online_players:
						# add player id to active_players
						self.online_players.append(sender)
						print(f"[#] User '{sender}' added to online_players")
						# send directly to landing
						# send landing page info
						new_info = {'status': 'WELCOME', 'sender': 'SERVER'}
						match_data = self.db.load_matches()
						self.mq.send(sender, new_info, match_data)
					else:
						# check status
						if info['status'] == 'WELCOME':
							# if sender in available players, remove
							if sender in self.available_players:
								self.available_players.remove(sender)
								print(f"[#] User '{sender}' removed from available players")
							# send landing page info
							new_info = {'status': 'WELCOME', 'sender': 'SERVER'}
							match_data = self.db.load_matches()
							self.mq.send(sender, new_info, match_data)
						elif info['status'] == 'AVAILABLE':
							# check for available players to match client with
							if len(self.available_players) > 0:
								print("[#] Pairing up available players...")
								# send ready signal to both players
								for client in (self.available_players.pop(), sender):
									new_info = {'sender': 'SERVER', 'status': 'READY'}
									self.mq.send(client, new_info, {})
							else:
								print("[#] No other players available...")
								# add to available_players
								self.available_players.append(sender)
								print(f"[#] Adding '{sender}' to available players")
								# respond
								new_info = {'sender': 'SERVER', 'status': 'WAIT'}
								self.mq.send(sender, new_info, {})
						
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
										new_info = {'sender': players[1], 'status': 'PLAY'}
										self.mq.send(players[0], new_info, {})
										# inform the other
										new_info = {'sender': players[0], 'status': 'PLAY'}
										self.mq.send(players[1], new_info, {})
									else:
										continue
										
						elif info['status'] == 'PLAYING':
							# if playing, reformat and resend
							info = {'sender': message[0], 'status': 'PLAY'}
							self.mq.send(info['recipient'], info, {})
						
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
							new_info = {'sender': 'SERVER', 'status': 'OVER'}		# OVER commands signals victory
							self.mq.send(winner, new_info, payload)
							continue
						elif info['status'] == 'QUIT':		# player disconnecting
							# remove player id from online_players
							self.online_players.remove(sender)
							print(f"[#] User '{sender}' removed from online players")
							continue
						else:
							pass
						
			except KeyboardInterrupt:
				finished = True
			time.sleep(0.001)
		# os._exit(0)
		exit()
		

if __name__ == '__main__':
	pass

