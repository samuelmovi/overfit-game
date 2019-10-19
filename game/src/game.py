from .controller import controller
from .model import player
from .view import view


def main():
	# start model
	my_player = player.Player()
	
	# start view
	my_view = view.View()
	
	# start controller
	ctrl = controller.Controller(my_view, my_player)
	ctrl.start_screen()
	

if __name__ == '__main__':
	main() 
