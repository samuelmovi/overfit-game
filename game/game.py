from controller import controller
from model import player
from view import view


def main():
	# start model
	my_player = player.Player()
	
	# start view
	my_view = view.View()
	
	# start controller
	controller.Controller(my_view, my_player)
	

if __name__ == '__main__':
	main() 
