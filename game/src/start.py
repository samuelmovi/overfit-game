from controller import controller
from model import player
from view import view
import os


class Start:
	
	def __init__(self):
		self.my_player = None
		self.my_view = None
		self.ctrl = None
		
	def game(self):
		self.my_player = player.Player()
		
		# start view
		self.my_view = view.View()
		
		# start controller
		self.ctrl = controller.Controller(self.my_view, self.my_player)
		self.ctrl.load_external_resources(self.ctrl.my_view, os.path.join(os.getcwd(), '../resources'))
		self.ctrl.main_loop()
	

if __name__ == '__main__':
	start = Start()
	start.game()
