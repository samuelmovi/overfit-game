import unittest
import sys
import os
from unittest import mock

sys.path.append(os.path.abspath('../../src/'))
from controller import controller


# TODO: find way to patch-in a mock pygame.event
class TestController(unittest.TestCase):
    
    test_ctrl = None
    
    def __init__(self, *args, **kwargs):
        super(TestController, self).__init__(*args, **kwargs)
        pass
    
    def test_init(self):
        # check nulls
        self.assertIsNone(controller.Controller.my_view)
        self.assertIsNone(controller.Controller.player)
        self.assertIsNone(controller.Controller.FPSCLOCK)

        # set object state
        mock_view = mock.Mock()
        mock_player = mock.Mock()
        # execute method
        self.test_ctrl = controller.Controller(mock_view, mock_player)

        # assert expected outcome
        self.assertIsNotNone(self.test_ctrl.targets)
        self.assertIsNotNone(self.test_ctrl.FPSCLOCK)
        self.assertEqual(mock_view, self.test_ctrl.my_view)
        self.assertEqual(mock_player, self.test_ctrl.player)
    
    # def test_main_loop(self):
    #     # set object state
    #     # mock inner method calls
    #     # set all keywords: start, game, online_setup, find_online_match, settings, confirm_exit, confirm_leave,
    #     #     game_over, victory
    #     # set loop_finished boolean side effects to limit looping
    #     # set draw_again boolean
    #     # execute method
    #     test_controller.main_loop()
    #     # assert expected outcome
    #     # each keyword calls expected function
    #     pass
    #
    # def test_draw(self):
    #     # set object state
    #     # inject mock view
    #     # set all keywords: start, game, online_setup, find_online_match, settings, confirm_exit, confirm_leave,
    #     game_over, victory
    #     # execute method
    #     inputs = test_controller.draw()
    #     # assert expected outcome
    #     # calls to mock view methods
    #     # returned object
    #     pass
    #
    # def test_welcome_listener(self):
    #     # set object state
    #     # inject mock inputs
    #     # mock pygame.event.get
    #     # execute method
    #     test_controller.welcome_listener(mock_inputs)
    #     # assert expected outcome
    #     # value of keyword, draw again
    #     # value of draw loop finished, board
    #     pass
    #
    # def test_game_listener(self):
    #     # set object state
    #     # inject mock player
    #     # mock pygame.event.get
    #     # execute method
    #     test_controller.game_listener()
    #     # assert expected outcome
    #     # value of keyword, draw again
    #     # value of draw loop finished, board
    #     pass
    #
    # def test_online_setup_listener(self):
    #     # set object state
    #     # inject mock inputs
    #     # mock pygame.event.get
    #     # execute method
    #     test_controller.online_setup_listener(mock_inputs)
    #     # assert expected outcome
    #     # value of keyword, draw again
    #     # value of draw loop finished, broker, mq
    #     # calls to mock view
    #     pass
    #
    # def test_find_match_listener(self):
    #     # set object state
    #     # mock pygame.event.get
    #     # execute method
    #     test_controller.find_match_listener()
    #     # assert expected outcome
    #     # value of keyword, draw again
    #     # value of draw loop finished, broker, mq
    #     # calls to mock view
    #     pass
    #
    # def test_settings_listener(self):
    #     # set object state
    #     # inject mock inputs
    #     # mock pygame.event.get
    #     # execute method
    #     test_controller.settings_listener(mock_inputs)
    #     # assert expected outcome
    #     # value of keyword, draw again
    #     # value of draw loop finished, broker, mq
    #     # calls to mock view
    #     pass
    #
    # def test_confirm_exit_listener(self):
    #     # set object state
    #     # inject mock inputs
    #     # mock pygame.event.get
    #     # execute method
    #     test_controller.confirm_exit_listener(mock_inputs)
    #     # assert expected outcome
    #     # value of keyword, draw again
    #     # value of draw loop finished
    #     pass
    #
    # def test_confirm_leave_listener(self):
    #     # set object state
    #     # inject mock inputs
    #     # mock pygame.event.get
    #     # execute method
    #     test_controller.confirm_leave_listener(mock_inputs)
    #     # assert expected outcome
    #     # value of keyword, draw again
    #     # value of draw loop finished
    #     pass
    #
    # def test_game_over_listener(self):
    #     # set object state
    #     # mock pygame.event.get
    #     # execute method
    #     test_controller.game_over_listener()
    #     # assert expected outcome
    #     # value of keyword, draw again
    #     # value of draw loop finished
    #     pass
    #
    # def test_victory_listener(self):
    #     # set object state
    #     # mock inner method calls
    #     # execute method
    #     test_controller.game_handler()
    #     # assert expected outcome
    #     # value of keyword, draw again
    #     # value of draw loop finished
    #     pass
    #
    # def test_game_handler(self):
    #     # set object state
    #     # mock pygame.event.get
    #     # inject mock view
    #     # set player status: capturing, returning
    #     # set all_targets_acquired boolean
    #     # execute method
    #     test_controller.victory_listener()
    #     # assert expected outcome
    #     # calls to inner methods
    #     # calls to mock view
    #     pass
    #
    # def test_capture_animation(self):
    #     # set object state
    #     # inject mock player
    #     # inject mock view, board
    #     # set value for ray_coords
    #     # execute method
    #     test_controller.capture_animation()
    #     # assert expected outcome
    #     # calls to inner methods
    #     # call to mock objects methods
    #     # changes to mock values
    #     pass
    #
    # def test_return_animation(self):
    #     # set object state
    #     # set boolean return for self.my_view.animate_return(self.ray_coords)
    #     # set size for self.board.columns[self.ray_coords['position']].figures
    #     # set boolean return for self.board.columns[self.ray_coords['position']].figures[-1].fits(*)
    #     # set boolean return for self.board.columns[self.ray_coords['position']].figures[-1].empty
    #
    #     # execute method
    #     test_controller.return_animation()
    #     # assert expected outcome
    #     # confirm calls to mock player, view and board
    #     pass
    #
    # def test_explode_all_targets(self):
    #     # set object state
    #     # set controller.frame
    #     # execute method
    #     test_controller.explode_all_targets()
    #     # assert expected outcome
    #     # call to controller.my_view.draw_explosion()
    #     # call controller.board.eliminate_targets(self.targets)
    #     # call to controller.targets.sort(lambda)
    #     # value of controller.player.score
    #     # value of controller.frame
    #     pass
    #
    #
    # def test_update_player_stats(self):
    #     # set object state
    #     # set player state,
    #     # set board total, longest
    #     # mock controller.board.columns
    #     # execute method
    #     test_controller.update_player_stats()
    #     # assert expected outcome
    #     # calls to board.add_row()
    #     # values of player state
    #     # values for board total, longest
    #     #
    #     pass
    #
    # def test_find_match(self):
    #     # beware of while true
    #     # mock zmq connector, online broker, pygame.event.get()
    #     # mock online broker negotiate, timeout
    #     # set player state,
    #     # set board total, longest
    #     # mock controller.board.columns
    #     # execute method
    #     test_controller.find_match()
    #     # assert expected outcome
    #     # calls to board.add_row()
    #     # values of player online
    #     # values received for self.my_view.draw_wait_screen(text)
    #     #
    #     pass    #
    # def test_check_online_play(self):
    #     # set object state
    #     # set value for self.player.connected
    #     # set value for controller.send_counter
    #     # mock view
    #     # execute method
    #     test_controller.check_online_play()
    #     # assert expected outcome
    #     # call to mock view draw_opponent
    #     pass
    #
    # def test_check_on_opponent(self):
    #     # set object state
    #     # mock mq sub_receive_multi()
    #     # mock board add_row
    #     # mock inner class method victory()
    #     # value for opponent online, score
    #     # set rows_received
    #     # execute method
    #     test_controller.check_on_opponent()
    #     # assert expected outcome
    #     pass
    #
    # def test_reset_state(self):
    #     # set object state
    #     # inject mock mq, player
    #     # set opponent
    #     # execute method
    #     test_controller.load_external_resources
    #     # assert expected outcome
    #     # values of opponent, send counter, explosion_counter, rows received,
    #     # calls to mock object methods
    #     pass
    #
    # def test_load_external_resources(self):
    #     # set object state
    #     # inject mock view
    #     # maybe, mock pygame itself ???
    #     # execute method
    #     test_controller.load_external_resources(mock_view, path)
    #     # assert expected outcome
    #     # calls to mock object methods
    #     pass
    #
    
        
if __name__ == '__main__':
    unittest.main()
