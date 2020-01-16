import zmq
import zmq.auth
from zmq.auth.thread import ThreadAuthenticator
import os
import traceback
import json
import datetime


class ZmqConnector:
	context = None
	auth = None
	public_keys_dir = None
	secret_keys_dir = None
	puller = None
	publisher = None

	HOST = ''

	opponent_id = None
	available_player = 'XXX'
	
	# Client message protocol:
	#
	# 1. ID: Player ID (random string created by online broker)
	# 2. ACTION: status, command, recipient.
	# 3. MATCH: relevant player match data
	
	# Server message protocol:
	#
	# 1. Recipient: Player ID of recipient, used for filtering
	# 2. ACTION: sender (SERVER or opponent player's ID), command (welcome, wait, ready, play)
	# 3. Data: forwarded payload
	
	def __init__(self, host='127.0.0.1'):
		print("[zmq] Initializing ZMQ client object...")
		self.HOST = host
		self.context = zmq.Context()
		
	def setup(self):
		if not self.check_folder_structure():
			return None
		else:
			self.server_auth()
			self.bind_pull()
			self.bind_pub()
	
	def check_folder_structure(self):
		keys_dir = os.path.join(os.getcwd(), '../certs')
		print(f"[#] checking folder structure: {keys_dir}")
		self.public_keys_dir = os.path.join(keys_dir, 'public')  # has the public keys of registered clients
		self.secret_keys_dir = os.path.join(keys_dir, 'private') 	# has the server's private cert

		if not os.path.exists(keys_dir) \
			and not os.path.exists(self.public_keys_dir) \
			and not os.path.exists(self.secret_keys_dir):
			print("[!!] Certificates folders are missing")
			return False
		else:
			return True
	
	def server_auth(self):
		# Start an authenticator for this context
		print("[#] Starting authenticator...")
		self.auth = ThreadAuthenticator(self.context)
		self.auth.start()
		self.auth.allow(self.HOST)
		# give authenticator access to approved clients' certificate directory
		self.auth.configure_curve(domain='*', location=self.public_keys_dir)
	
	def bind_pull(self, port=5555):
		print("[zmq] Binding PULL socket : {}".format(port))
		self.puller = self.context.socket(zmq.PULL)
		# feed certificates to socket
		server_secret_file = os.path.join(self.secret_keys_dir, "server.key_secret")
		self.puller.curve_publickey, self.puller.curve_secretkey = zmq.auth.load_certificate(server_secret_file)
		self.puller.curve_server = True  # must come before bind
		self.puller.bind("tcp://*:{}".format(port))

	def pull_receive_multi(self):
		try:
			message = self.puller.recv_multipart(flags=zmq.DONTWAIT)
			print(f"[zmq] Received :\n\t{datetime.datetime.now()}- {message}")
			return message
		except zmq.Again as a:
			# print("[!zmq!] Error while getting messages: {}".format(a))
			# print(traceback.format_exc())
			return None
		except zmq.ZMQError as e:
			print("[!zmq!] Error while getting messages: {}".format(e))
			print(traceback.format_exc())
			return None
	
	def bind_pub(self, port=5556):
		print("[zmq] Binding PUB socket: {}".format(port))
		self.publisher = self.context.socket(zmq.PUB)
		# feed own and approved certificates to socket
		server_secret_file = os.path.join(self.secret_keys_dir, "server.key_secret")
		self.publisher.curve_publickey, self.publisher.curve_secretkey = zmq.auth.load_certificate(server_secret_file)
		self.publisher.curve_server = True  # must come before bind
		self.publisher.bind("tcp://*:{}".format(port))

	def send(self, recipient, info, payload):
		message = list()
		message.append(recipient.encode())
		message.append(json.dumps(info).encode())
		message.append(json.dumps(payload).encode())
		# print(f'[zmq] sending message: {message}')
		self.pub_send_multi(message)
		
	def pub_send_multi(self, message):
		try:
			self.publisher.send_multipart(message)
			print(f"[zmq] Sent :\n\t{datetime.datetime.now()}- {message}")
		except TypeError as e:
			print("[!zmq!] TypeError while sending message: {}".format(e))
			print(traceback.format_exc())
		except ValueError as e:
			print("[!zmq!] ValueError while sending message: {}".format(e))
			print(traceback.format_exc())
		except zmq.ZMQError as e:
			print("[!zmq!] ZMQError while sending message: {}".format(e))
			print(traceback.format_exc())

	# GENERIC FUNCTIONS
	def disconnect(self):
		print("[zmq] Disconnecting client...")
		for socket in (self.publisher, self.puller):
			if socket is not None:
				socket.close()
		self.context.term()


if __name__ == '__main__':
	pass
