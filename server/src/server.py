import os


class Server:

	def __init__(self, connector=None, db=None):
		if connector and db:
			self.mq = connector
			self.db = db
		else:
			print("[!!] No connector or db??\n")
			exit()
	
	def loop(self):
		print("[#] starting loop...")
		stop_me = False
		while not stop_me:
			try:
				message = self.pull()
				if message is not None:
					print("[#] Message pulled:".format(message))
					for part in message:
						print("\t> {} /{}".format(part, type(part)))
					print("\n[#] rePUBlishing Message...")
					self.pub(message)
			except KeyboardInterrupt:
				stop_me = True
	

class PullPubServer:
	
	mq = None

	def __init__(self, connector=None):
		if connector:
			self.mq = connector
	
	def set_up(self):
		self.mq.check_folder_structure()
		self.mq.server_auth()
		self.connect_pull()
		self.connect_pub()

	def connect_pull(self):
		print("[#] Creating PULLER...")
		self.mq.bind_pull(5555)

	def connect_pub(self):
		print("[#] Creating PUBLISHER...")
		self.mq.bind_pub(5556)

	def pull(self):
		# print("[#] Reading multipart messages from PULL socket...")
		message = self.mq.pull_receive_multi()
		return message

	def pub(self, message):
		print("[#] Sending multi-message PUB:")
		self.mq.pub_send_multi(message)

	def loop(self):
		print("[#] starting loop...")
		stop_me = False
		while not stop_me:
			try:
				message = self.pull()
				if message is not None:
					print("[#] Message pulled:".format(message))
					for part in message:
						print("\t> {} /{}".format(part, type(part)))
					print("\n[#] rePUBlishing Message...")
					self.pub(message)
			except KeyboardInterrupt:
				stop_me = True
		os._exit(0)


if __name__ == '__main__':
	pass

