from controller import controller
from model import player, zmq_client, online_broker
from view import view
import os
import sys
import pygame


class Start:
	
	def __init__(self):
		self.player = None
		self.view = None
		self.ctrl = None
		self.mq = None
		self.broker = None
		
	def game(self):
		self.player = player.Player()
		
		# start view
		self.view = view.View()
		
		# online objects
		self.mq = zmq_client.ZmqConnector()
		self.broker = online_broker.OnlineBroker(self.player, self.mq)
		
		# start controller
		self.ctrl = controller.Controller(self.view, self.player, self.mq, self.broker)
		self.ctrl.load_external_resources(self.ctrl.view, os.path.join(os.getcwd(), '../resources'))
		self.ctrl.main_loop()
		pygame.quit()
		sys.exit()
	

if __name__ == '__main__':
	start = Start()
	start.game()
