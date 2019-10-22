import zmq
import zmq.auth
from zmq.auth.thread import ThreadAuthenticator
import os
import traceback


class ZmqConnector:
	context = None
	auth = None
	public_keys_dir = None
	secret_keys_dir = None
	pusher = None
	puller = None
	publisher = None
	subscriber = None
	requester = None
	replier = None
	base_dir = None

	HOST = ''

	opponent_id = None
	available_player = 'XXX'

	# all messages are multipart:
	#   > first part is the recipient (or XXX for broadcast of available player)
	#   > second part holds player json data

	def __init__(self, host='127.0.0.1'):
		print("[zmq] Initializing ZMQ client object...")
		self.HOST = host
		self.context = zmq.Context()
		self.base_dir = os.getcwd()
	
	def check_folder_structure(self):
		print("[#] checking folder structure...")
		keys_dir = os.path.join(self.base_dir, '../certs')
		self.public_keys_dir = os.path.join(keys_dir, 'public')    # has the public keys of allowed clients
		self.secret_keys_dir = os.path.join(keys_dir, 'private')   # has the server's private cert

		if not os.path.exists(keys_dir) and not os.path.exists(self.public_keys_dir) and not os.path.exists(self.secret_keys_dir):
			print("[!!] Certificates folders are missing: {}".format(keys_dir))
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
	
	def client_auth(self):
		print("[#] Managing certificates...")
		# Load client's certificate into client socket
		client_secret_file = os.path.join(self.secret_keys_dir, "client.key_secret")
		self.context.curve_publickey, self.context.curve_secretkey = zmq.auth.load_certificate(client_secret_file)
		# Load server's public key into socket
		server_public_file = os.path.join(self.public_keys_dir, "server.key")
		self.context.curve_serverkey, _ = zmq.auth.load_certificate(server_public_file)

	# PULL - PUSH
	def connect_pull(self, port):
		print("[zmq] Connecting PULL socket : {}/{}".format(self.HOST, port))
		self.puller = self.context.socket(zmq.PULL)
		self.puller.connect("tcp://{}:{}".format(self.HOST, port))

	def bind_pull(self, port):
		print("[zmq] Binding PULL socket : {}".format(port))
		self.puller = self.context.socket(zmq.PULL)
		# feed certificates to socket
		server_secret_file = os.path.join(self.secret_keys_dir, "server.key_secret")
		self.puller.curve_publickey, self.puller.curve_secretkey = zmq.auth.load_certificate(server_secret_file)
		self.puller.curve_server = True  # must come before bind
		self.puller.bind("tcp://*:{}".format(port))

	def pull_send(self, message):
		self.send(self.puller, message)

	def pull_send_multi(self, message):
		self.send_multi(self.puller, message)

	def pull_receive(self):
		message = self.receive(self.puller)
		return message

	def pull_receive_multi(self):
		message = self.receive_multi(self.puller)
		return message

	def connect_push(self, port):
		print("[zmq] Connecting PUSH socket: {}/{}".format(self.HOST, port))
		self.pusher = self.context.socket(zmq.PUSH)
		self.pusher.connect("tcp://{}:{}".format(self.HOST, port))

	def bind_push(self, port):
		print("[zmq] Binding PUSH socket : {}".format(port))
		self.pusher = self.context.socket(zmq.PUSH)
		self.pusher.bind("tcp://*:{}".format(port))

	def push_send(self, message):
		self.send(self.pusher, message)

	def push_send_multi(self, message):
		self.send_multi(self.pusher, message)

	# REQUEST - REPLY
	def connect_req(self, port):
		print("[zmq] Connecting REQ socket: {}/{}".format(self.HOST, port))
		self.requester = self.context.socket(zmq.REQ)
		self.requester.connect("tcp://{}:{}".format(self.HOST, port))

	def req_send(self, message):
		self.send(self.requester, message)

	def req_send_multi(self, message):
		self.send_multi(self.requester, message)

	def req_receive(self):
		message = self.receive(self.requester)
		return message

	def req_receive_multi(self):
		message = self.receive_multi(self.requester)
		return message

	def bind_reply(self, port):
		print("[zmq] Binding REP socket : {}".format(port))
		self.replier = self.context.socket(zmq.REP)
		self.replier.bind("tcp://*:{}".format(port))

	def reply_receive(self):
		message = self.receive(self.replier)
		return message

	def reply_receive_multi(self):
		message = self.receive_multi(self.replier)
		return message

	def reply_send(self, message):
		self.send(self.replier, message)

	def reply_send_multi(self, message):
		self.send_multi(self.replier, message)

	# PUBLISH - SUBSCRIBE
	def connect_pub(self, port):
		print("[zmq] Connecting PUB socket: {}/{}".format(self.HOST, port))
		self.publisher = self.context.socket(zmq.PUB)
		self.publisher.connect("tcp://{}:{}".format(self.HOST, port))

	def bind_pub(self, port):
		print("[zmq] Binding PUB socket: {}".format(port))
		self.publisher = self.context.socket(zmq.PUB)
		# feed own and approved certificates to socket
		server_secret_file = os.path.join(self.secret_keys_dir, "server.key_secret")
		self.publisher.curve_publickey, self.publisher.curve_secretkey = zmq.auth.load_certificate(server_secret_file)
		self.publisher.curve_server = True  # must come before bind
		self.publisher.bind("tcp://*:{}".format(port))

	def pub_send(self, message):
		self.send(self.publisher, message)

	def pub_send_multi(self, message):
		self.send_multi(self.publisher, message)

	def connect_sub(self, port):
		print("[zmq] Connecting SUB socket: {}/{}".format(self.HOST, port))
		self.subscriber = self.context.socket(zmq.SUB)
		self.subscriber.connect("tcp://{}:{}".format(self.HOST, port))

	def bind_sub(self, port):
		print("[zmq] Binding SUB socket : {}".format(port))
		self.subscriber = self.context.socket(zmq.PUSH)
		self.subscriber.bind("tcp://*:{}".format(port))

	def sub_receive(self):
		message = self.receive(self.subscriber)
		return message

	def sub_receive_multi(self):
		message = self.receive_multi(self.subscriber)
		return message

	# SUBSCRIPTION FILTERS
	def filter_sub_socket(self, filter_string):
		print("[zmq] Filtering SUBscription: {}".format(filter_string))
		self.subscriber.setsockopt_string(zmq.SUBSCRIBE, filter_string)

	def unfilter_sub_socket(self, filter_string):
		print("[zmq] Unfiltering SUBscription: {}".format(filter_string))
		self.subscriber.setsockopt_string(zmq.UNSUBSCRIBE, filter_string)

	# GENERIC FUNCTIONS
	def send_multi(self, socket, message):
		try:
			socket.send_multipart(message)
			print("[zmq] Multi-Message sent :{}".format(message))
		except TypeError as e:
			print("[!zmq!] TypeError while sending message: {}".format(e))
			print(traceback.format_exc())
		except ValueError as e:
			print("[!zmq!] ValueError while sending message: {}".format(e))
			print(traceback.format_exc())
		except zmq.ZMQError as e:
			print("[!zmq!] ZMQError while sending message: {}".format(e))
			print(traceback.format_exc())

	def send(self, socket, message):
		try:
			# print("[zmq] Sending message:\n\t> Message: {}".format(message))
			socket.send(message)
			print("[zmq] Message sent")
		except TypeError as e:
			print("[!zmq!] TypeError while sending message: {}".format(e))
			print(traceback.format_exc())
		except ValueError as e:
			print("[!zmq!] ValueError while sending message: {}".format(e))
			print(traceback.format_exc())
		except zmq.ZMQError as e:
			print("[!zmq!] ZMQError while sending message: {}".format(e))
			print(traceback.format_exc())

	def receive_multi(self, socket):
		try:
			# print("[zmq] Reading multipart messages from socket...")
			# message = socket.recv_multipart(flags=zmq.DONTWAIT)
			message = socket.recv_multipart(flags=zmq.NOBLOCK)
			# print("[zmq] Multi-Part Message received: ")
			# for part in message:
			#     print("\t> {} /{}".format(part, type(part)))
			return message
		except zmq.Again as a:
			print("[!zmq!] Error while getting messages: {}".format(a))
			print(traceback.format_exc())
			return None
		except zmq.ZMQError as e:
			print("[!zmq!] Error while getting messages: {}".format(e))
			print(traceback.format_exc())
			return None

	def receive(self, socket):
		try:
			# print("[zmq] Reading messages from socket...")
			message = socket.recv(flags=zmq.DONTWAIT)
			# print("[zmq] Message received: \n\tMessage: {}".format(message))
			return message
		except zmq.Again as a:
			print("[!zmq!] Error while getting messages: {}".format(a))
			print(traceback.format_exc())
			return None
		except zmq.ZMQError as e:
			print("[!zmq!] Error while getting messages: {}".format(e))
			print(traceback.format_exc())
			return None

	def disconnect(self):
		print("[zmq] Disconnecting client...")
		for socket in (self.pusher, self.publisher, self.puller, self.subscriber, self.replier, self.requester):
			if socket is not None:
				socket.close()
		self.context.term()


if __name__ == '__main__':
	pass
