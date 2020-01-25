import unittest
import sys
import os
sys.path.append(os.path.abspath('../src/'))
import zmq_server


class TestMQ(unittest.TestCase):

	test_mq = None

	def __init__(self, *args, **kwargs):
		super(TestMQ, self).__init__(*args, **kwargs)
		pass
	
	def test_init(self):
		# set object state
		# execute method
		self.test_mq = zmq_server.ZmqConnector()
		# assert expected result
		self.assertEqual('127.0.0.1', self.test_mq.HOST)
		self.assertIsNotNone(self.test_mq.context)
		
		# execute method
		self.test_mq = zmq_server.ZmqConnector('172.17.0.2')
		# assert expected result
		self.assertEqual('172.17.0.2', self.test_mq.HOST)
		self.assertIsNotNone(self.test_mq.context)
	
	def test_check_folder_structure(self):
		# set object state
		self.test_mq = zmq_server.ZmqConnector()
		# execute method
		outcome = self.test_mq.check_folder_structure()
		# assert expected outcome
		self.assertTrue(outcome)
	
	# def server_auth(self):
	# 	# Start an authenticator for this context
	# 	print("[#] Starting authenticator...")
	# 	self.auth = ThreadAuthenticator(self.context)
	# 	self.auth.start()
	# 	self.auth.allow(self.HOST)
	# 	# give authenticator access to approved clients' certificate directory
	# 	self.auth.configure_curve(domain='*', location=self.public_keys_dir)
	#
	# def bind_pull(self, port=5555):
	# 	print("[zmq] Binding PULL socket : {}".format(port))
	# 	self.puller = self.context.socket(zmq.PULL)
	# 	# feed certificates to socket
	# 	server_secret_file = os.path.join(self.secret_keys_dir, "server.key_secret")
	# 	self.puller.curve_publickey, self.puller.curve_secretkey = zmq.auth.load_certificate(server_secret_file)
	# 	self.puller.curve_server = True  # must come before bind
	# 	self.puller.bind("tcp://*:{}".format(port))
	#
	# def pull_receive_multi(self):
	# 	try:
	# 		message = self.puller.recv_multipart(flags=zmq.DONTWAIT)
	# 		print(f"[zmq] Received :\n\t{datetime.datetime.now()}- {message}")
	# 		return message
	# 	except zmq.Again as a:
	# 		# print("[!zmq!] Error while getting messages: {}".format(a))
	# 		# print(traceback.format_exc())
	# 		return None
	# 	except zmq.ZMQError as e:
	# 		print("[!zmq!] Error while getting messages: {}".format(e))
	# 		print(traceback.format_exc())
	# 		return None
	#
	# def bind_pub(self, port=5556):
	# 	print("[zmq] Binding PUB socket: {}".format(port))
	# 	self.publisher = self.context.socket(zmq.PUB)
	# 	# feed own and approved certificates to socket
	# 	server_secret_file = os.path.join(self.secret_keys_dir, "server.key_secret")
	# 	self.publisher.curve_publickey, self.publisher.curve_secretkey = zmq.auth.load_certificate(server_secret_file)
	# 	self.publisher.curve_server = True  # must come before bind
	# 	self.publisher.bind("tcp://*:{}".format(port))
	#
	# def send(self, recipient, info, payload):
	# 	message = list()
	# 	message.append(recipient.encode())
	# 	message.append(json.dumps(info).encode())
	# 	message.append(json.dumps(payload).encode())
	# 	self.pub_send_multi(message)
	#
	# def pub_send_multi(self, message):
	# 	try:
	# 		self.publisher.send_multipart(message)
	# 		print(f"[zmq] Sent :\n\t{datetime.datetime.now()}- {message}")
	# 	except TypeError as e:
	# 		print("[!zmq!] TypeError while sending message: {}".format(e))
	# 		print(traceback.format_exc())
	# 	except ValueError as e:
	# 		print("[!zmq!] ValueError while sending message: {}".format(e))
	# 		print(traceback.format_exc())
	# 	except zmq.ZMQError as e:
	# 		print("[!zmq!] ZMQError while sending message: {}".format(e))
	# 		print(traceback.format_exc())
	#
	# # GENERIC FUNCTIONS
	# def disconnect(self):
	# 	print("[zmq] Disconnecting client...")
	# 	for socket in (self.publisher, self.puller):
	# 		if socket is not None:
	# 			socket.close()
	# 	self.context.term()


if __name__ == '__main__':
	unittest.main()
