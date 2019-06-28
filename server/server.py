import zmq_connector
# import time
import os


HOST = '127.0.0.1'


class PullPubServer:

	mq = None

	def __init__(self):
		print("[#] Initiating PULlPubServer object...")
		self.mq = zmq_connector.ZmqConnector()
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


def main():
	server = PullPubServer()
	print("[#] server object initiated")

	print("[#] starting work...")
	while True:
		try:
			message = server.pull()
			if message is not None:
				print("[#] Message pulled:".format(message))
				for part in message:
					print("\t> {} /{}".format(part, type(part)))
				print("\n[#] rePUBlishing Message...")
				server.pub(message)
			# time.sleep(0.1)
		except KeyboardInterrupt:
			os._exit(0)


if __name__ == '__main__':
	main()

