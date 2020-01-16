import zmq
import zmq.auth
from zmq.auth.thread import ThreadAuthenticator
import os
import traceback
import json


class ZmqConnector:
	context = None
	auth = None
	secret_keys_dir = None
	public_keys_dir = None
	pusher = None
	subscriber = None
	base_dir = None

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
	# 3. Data:
	
	def start(self, host, topic):
		print("[zmq] Initializing ZMQ client object...")
		self.HOST = host
		self.context = zmq.Context()
		
		self.base_dir = os.getcwd()
		if not self.check_folder_structure():
			print("[!!] Problem with cert folder structure\n")
			return None
		else:
			self.client_auth()
			self.connect_push()  	# where we send our packets
			self.connect_sub()  	# where we get our packets
			self.filter_sub_socket(topic)
	
	def send(self, sender, info, payload):
		message = list()
		message.append(sender.encode())
		message.append(json.dumps(info).encode())
		message.append(json.dumps(payload).encode())
		self.push_send_multi(message)

	def check_folder_structure(self):
		keys_dir = os.path.join(self.base_dir, '../certs')
		print(f"[#] checking folder structure: {keys_dir}")
		self.secret_keys_dir = os.path.join(keys_dir, 'private')   # has the client's private key
		self.public_keys_dir = os.path.join(keys_dir, 'public')   # has the server's public key

		if not os.path.exists(keys_dir) and not os.path.exists(self.secret_keys_dir) and not os.path.exists(
				self.public_keys_dir):
			print(f"[!!] Certificates folders are missing: {keys_dir}")
			return False
		else:
			return True
	
	def client_auth(self):
		# TODO: what if this fails??
		print("[#] Managing certificates...")
		# Load client's certificate into client socket
		client_secret_file = os.path.join(self.secret_keys_dir, "client.key_secret")
		self.context.curve_publickey, self.context.curve_secretkey = zmq.auth.load_certificate(client_secret_file)
		# Load server's public key into socket
		server_public_file = os.path.join(self.public_keys_dir, "server.key")
		self.context.curve_serverkey, _ = zmq.auth.load_certificate(server_public_file)

	def connect_push(self, port=5555):
		print("[zmq] Connecting PUSH socket: {}/{}".format(self.HOST, port))
		self.pusher = self.context.socket(zmq.PUSH)
		self.pusher.connect("tcp://{}:{}".format(self.HOST, port))

	def push_send_multi(self, message):
		try:
			self.pusher.send_multipart(message)
			print("[zmq] Multi-Message sent :{}".format(message))
		except TypeError as e:
			print("[!zmq!] TypeError push_send_multi: {}".format(e))
			# print(traceback.format_exc())
		except ValueError as e:
			print("[!zmq!] ValueError push_send_multi: {}".format(e))
			# print(traceback.format_exc())
		except zmq.ZMQError as e:
			print("[!zmq!] ZMQError push_send_multi: {}".format(e))
			# print(traceback.format_exc())
			
	def connect_sub(self, port=5556):
		print("[zmq] Connecting SUB socket: {}/{}".format(self.HOST, port))
		self.subscriber = self.context.socket(zmq.SUB)
		self.subscriber.connect("tcp://{}:{}".format(self.HOST, port))

	def sub_receive_multi(self):
		try:
			message = self.subscriber.recv_multipart(flags=zmq.DONTWAIT)
			return message
		except zmq.Again as a:
			# print("[!zmq!] sub_receive_multi zmq.Again: {}".format(a))
			# print(traceback.format_exc())
			print("[@] No messages received")
			return None
		except zmq.ZMQError as e:
			print("[!zmq!] sub_receive_multi ZMQError: {}".format(e))
			# print(traceback.format_exc())
			return None

	# SUBSCRIPTION FILTERS
	def filter_sub_socket(self, filter_string):
		print(f"[zmq] Filtering SUBscription: {filter_string}")
		self.subscriber.setsockopt(zmq.SUBSCRIBE, filter_string.encode())

	def unfilter_sub_socket(self, filter_string):
		print("[zmq] Unfiltering SUBscription: {}".format(filter_string))
		self.subscriber.setsockopt(zmq.UNSUBSCRIBE, filter_string)

	# GENERIC FUNCTIONS
	def disconnect(self):
		print("[zmq] Disconnecting client...")
		for socket in (self.pusher, self.subscriber):
			if socket is not None:
				socket.close()
		self.context.term()


if __name__ == '__main__':
	pass
