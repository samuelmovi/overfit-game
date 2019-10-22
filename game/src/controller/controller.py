import pygame
import sys
import time
import json
import os
from model import board, zmq_connector, online_broker
from pygame.locals import *

    
class Controller:
    RIGHT = 'right'
    LEFT = 'left'
    FPS = 30  # frames per second to update the screen
    AP_Q = 'ap_q'
    opponent = None  # used to store the opponents dictionaries
    send_counter = 0  # used to delay checking queues
    explosion_counter = 1
    rows_received = 1
    ray_coords = {}
    frame = 0  # to keep track of frames during explosion animations
    all_targets_acquired = False
    player_stats = {}  # dictionary for the players own stats
    board = None
    broker = None
    mq = None
    HOST = '127.0.0.1'
    
    my_view = None
    player = None
    targets = []
    FPSCLOCK = None
    base_dir = os.path.join(os.getcwd(), '../')
    
    keyword = ""
    draw_again = True
    loop_finished = False

    def __init__(self, view, player):
        print('[#] Initiating Controller...')
        pygame.init()
        pygame.mixer.quit()
        
        self.my_view = view
        self.my_view.set_up_fonts()
        # self.load_external_resources(self.my_view, self.base_dir)
    
        self.player = player
    
        self.FPSCLOCK = pygame.time.Clock()
        pygame.display.set_caption('WeeriMeeris')
        
    @staticmethod
    def load_external_resources(my_view, resource_dir):
        my_view.ball = pygame.image.load(os.path.join(resource_dir, 'ball.png'))
        my_view.triangle_full = pygame.image.load(os.path.join(resource_dir, 'triangle-pink-full.png'))
        my_view.triangle_empty = pygame.image.load(
            os.path.join(resource_dir, 'triangle-pink-empty.png'))
        my_view.square_full = pygame.image.load(os.path.join(resource_dir, 'square-yellow-full.png'))
        my_view.square_empty = pygame.image.load(os.path.join(resource_dir, 'square-yellow-empty.png'))
        my_view.triangle_hole_complete = pygame.image.load(
            os.path.join(resource_dir, 'triangle-hole-green-complete.png'))
        my_view.triangle_hole_full = pygame.image.load(
            os.path.join(resource_dir, 'triangle-hole-green-full.png'))
        my_view.triangle_hole_empty = pygame.image.load(
            os.path.join(resource_dir, 'triangle-hole-green-empty.png'))
        my_view.square_hole_complete = pygame.image.load(
            os.path.join(resource_dir, 'square-hole-red-complete.png'))
        my_view.square_hole_full = pygame.image.load(
            os.path.join(resource_dir, 'square-hole-red-full.png'))
        my_view.square_hole_empty = pygame.image.load(
            os.path.join(resource_dir, 'square-hole-red-empty.png'))
        my_view.player_full = pygame.image.load(os.path.join(resource_dir, 'player-full.png'))
        my_view.player_empty = pygame.image.load(os.path.join(resource_dir, 'player-empty.png'))
        my_view.fire1 = pygame.image.load(os.path.join(resource_dir, 'fire1.png'))
        my_view.fire2 = pygame.image.load(os.path.join(resource_dir, 'fire2.png'))
        my_view.fire3 = pygame.image.load(os.path.join(resource_dir, 'fire3.png'))
        my_view.ray = pygame.image.load(os.path.join(resource_dir, 'ray-short.png'))
    
    def main_loop(self):
        inputs = None
        self.keyword = 'start'
        # TODO: figure put how to use methods as dictionary values
        event_listeners = {
            'start': self.welcome_listener,
            'game': self.game_listener,
            'online_setup': self.online_setup_listener,
            'settings': self.settings_listener,
            "confirm_exit": self.confirm_exit_listener,
            "confirm_leave": self.confirm_leave_listener
        }

        while not self.loop_finished:
            if self.draw_again:
                inputs = self.draw(self.keyword)
            # event_listeners[self.keyword](inputs)
            if self.keyword == "start":
                self.welcome_listener(inputs)
            elif self.keyword == "game":
                self.play()
            elif self.keyword == "online_setup":
                self.online_setup_listener(inputs)
            elif self.keyword == "settings":
                self.settings_listener(inputs)
            elif self.keyword == "confirm_exit":
                self.confirm_exit_listener(inputs)
            elif self.keyword == "confirm_leave":
                self.confirm_leave_listener(inputs)
        self.shutdown()
    
    def draw(self, keyword):
        inputs = None
        if keyword == "start":
            inputs = self.my_view.draw_start_screen()
        elif keyword == "game":
            self.game_handler()
        elif keyword == "online_setup":
            inputs = self.my_view.draw_online_options_screen(self.player.name, self.HOST)
        elif keyword == "settings":
            inputs = self.my_view.draw_settings_screen(self.player.name, self.HOST)
        elif keyword == "confirm_exit":
            inputs = self.my_view.confirm_exit()
        elif keyword == "confirm_leave":
            inputs = self.my_view.confirm_leave_game()
        self.draw_again = False
        return inputs
       
    # EVENT LISTENERS
    def welcome_listener(self, inputs):
        # check for and handle events
        single_player_button, online_multi_button, settings_button = inputs

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.shutdown()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.confirm_exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                if single_player_button.rect.collidepoint((mouse_x, mouse_y)):
                    self.keyword = 'game'
                    self.draw_again = True
                    print('[#] Game START!')
                    self.board = board.Board()
                    print('[#] Opponent: {}'.format(self.opponent))
                    
                elif online_multi_button.rect.collidepoint((mouse_x, mouse_y)):
                    self.keyword = 'online_setup'
                    self.draw_again = True
                elif settings_button.rect.collidepoint((mouse_x, mouse_y)):
                    self.keyword = 'settings'
                    self.draw_again = True
    
    def game_listener(self):
        # event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                self.shutdown()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move_player(self.LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.player.move_player(self.RIGHT)
                elif event.key == pygame.K_SPACE:
                    self.ray_coords = self.player.action(self.board.columns)
                elif event.key == pygame.K_ESCAPE:
                    pygame.event.clear()
                    self.keyword = "confirm_leave"
                    self.draw_again = True
    
    def online_setup_listener(self, inputs):
        input_boxes, start_button = inputs

        for event in pygame.event.get():
            # handle events in inputs first
            for input_box in input_boxes:
                input_box.handle_event(event)
        
            if event.type == pygame.QUIT:
                self.loop_finished = True
                self.shutdown()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.clear()
                    self.keyword = "start"
                    self.draw_again = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                if start_button.rect.collidepoint((mouse_x, mouse_y)):
                    if len(input_boxes[0].get_text()) > 0:
                        self.HOST = input_boxes[0].get_text()
                    if len(input_boxes[1].get_text()) > 0:
                        self.player.name = input_boxes[1].get_text()
                    self.find_online_match()
    
    def settings_listener(self, inputs):
        input_boxes, save_button = inputs

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.shutdown()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.clear()
                    self.keyword = "start"
                    self.draw_again = True
                elif event.key == pygame.K_RETURN:
                    if len(input_boxes[0].get_text()) > 0:
                        self.mq.HOST = input_boxes[0].get_text()
                    if len(input_boxes[1].get_text()) > 0:
                        self.player.name = input_boxes[1].get_text()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                if save_button.rect.collidepoint((mouse_x, mouse_y)):
                    self.HOST = input_boxes[0].text
                    self.player.name = input_boxes[1].text
                    print("[#] Data updated\n\t> Host: {}\n\t> Player Name: {}"
                          .format(input_boxes[0].text, input_boxes[1].text))
            for instance in input_boxes:
                instance.handle_event(event)
    
    def confirm_exit_listener(self, inputs):
        yes_button, no_button = inputs
        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.QUIT:
                self.loop_finished = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.keyword = "start"
                self.draw_again = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                if yes_button.rect.collidepoint((mouse_x, mouse_y)):
                    self.loop_finished = True
                elif no_button.rect.collidepoint((mouse_x, mouse_y)):
                    self.keyword = "start"
                    self.draw_again = True
    
    def confirm_leave_listener(self, inputs):
        yes_button, no_button = inputs

        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.QUIT:
                self.loop_finished = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                if yes_button.rect.collidepoint((mouse_x, mouse_y)):
                    self.reset_state()
                    self.keyword = "start"
                    self.draw_again = True
                elif no_button.rect.collidepoint((mouse_x, mouse_y)):
                    return
    
    # SCREENS
    def welcome_screen(self):
        # draw the start screen and get the buttons
        single_player_button, online_multi_button, settings_button = self.my_view.draw_start_screen()
    
        while True:
            # check for and handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.shutdown()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.confirm_exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = event.pos
                    if single_player_button.rect.collidepoint((mouse_x, mouse_y)):
                        self.play()
                    elif online_multi_button.rect.collidepoint((mouse_x, mouse_y)):
                        self.online_setup_screen()
                    elif settings_button.rect.collidepoint((mouse_x, mouse_y)):
                        self.settings_screen()
            # update display with all changes drawn
            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)
    
    def online_setup_screen(self):
        print('[#] Online Setup screen')
        input_boxes, start_button = self.my_view.draw_online_options_screen(self.player.name, self.HOST)
        while True:
            # event handling loop
            for event in pygame.event.get():
                # handle events in inputs first
                for input_box in input_boxes:
                    input_box.handle_event(event)
    
                if event.type == pygame.QUIT:
                    self.shutdown()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.clear()
                        self.welcome_screen()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = event.pos
                    if start_button.rect.collidepoint((mouse_x, mouse_y)):
                        if len(input_boxes[0].get_text()) > 0:
                            self.HOST = input_boxes[0].get_text()
                        if len(input_boxes[1].get_text()) > 0:
                            self.player.name = input_boxes[1].get_text()
                        self.find_online_match()
            self.my_view.refresh_input(input_boxes)
            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)
    
    def settings_screen(self):
        print('[#] Settings screen')
        inputs, save_button = self.my_view.draw_settings_screen(self.player.name, self.HOST)
        while True:
            # event handling loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.shutdown()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.clear()
                        self.welcome_screen()
                    elif event.key == pygame.K_RETURN:
                        if len(inputs[0].get_text()) > 0:
                            self.mq.HOST = inputs[0].get_text()
                        if len(inputs[1].get_text()) > 0:
                            self.player.name = inputs[1].get_text()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = event.pos
                    if save_button.rect.collidepoint((mouse_x, mouse_y)):
                        self.HOST = inputs[0].text
                        self.player.name = inputs[1].text
                        print("[#] Data updated\n\t> Host: {}\n\t> Player Name: {}".format(inputs[0].text, inputs[1].text))
                for instance in inputs:
                    instance.handle_event(event)
            self.my_view.refresh_input(inputs)
            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)
    
    def confirm_exit(self):
        print('[#] Confirm exit')
        yes_button, no_button = self.my_view.confirm_exit()
        while True:
            for event in pygame.event.get():  # event handling loop
                if event.type == pygame.QUIT:
                    self.shutdown()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.welcome_screen()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = event.pos
                    if yes_button.rect.collidepoint((mouse_x, mouse_y)):
                        self.shutdown()
                    elif no_button.rect.collidepoint((mouse_x, mouse_y)):
                        self.welcome_screen()
            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)
    
    def confirm_leave_game(self):
        print('[#] Confirm leave game')
        yes_button, no_button = self.my_view.confirm_leave_game()
        while True:
            for event in pygame.event.get():  # event handling loop
                if event.type == pygame.QUIT:
                    self.shutdown()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = event.pos
                    if yes_button.rect.collidepoint((mouse_x, mouse_y)):
                        self.reset_state()
                        self.welcome_screen()
                    elif no_button.rect.collidepoint((mouse_x, mouse_y)):
                        return
                """
                # THIS CODE CRASHES GAME FOR UNKNOWN REASON
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.event.clear()
                    return
                """
            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)
    
    # GAMING FUNCTIONS
    def game_handler(self):
        self.game_listener()
        self.update_player_stats()
        self.board.update_counts()
        self.my_view.update_game_screen(self.player, self.board)
        self.check_online_play()
    
        # check for capture
        if self.player.status == 'capturing':
            self.capture_animation()
        # check for return
        elif self.player.status == 'returning':
            self.return_animation()
        # check for explosion
        if self.all_targets_acquired is True:
            self.explode_all_targets()
        
    def play(self):
        print('[#] Game START!')
        self.board = board.Board()
        print('[#] Opponent: {}'.format(self.opponent))
    
        while True:
            self.game_listener()
            self.update_player_stats()
            self.board.update_counts()
            self.my_view.update_game_screen(self.player, self.board)
            self.check_online_play()
    
            # check for capture
            if self.player.status == 'capturing':
                self.capture_animation()
            # check for return
            elif self.player.status == 'returning':
                self.return_animation()
            # check for explosion
            if self.all_targets_acquired is True:
                self.explode_all_targets()
    
            # Refresh screen and wait a clock tick.
            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)
    
    def capture_animation(self):
        if self.my_view.animate_return(self.ray_coords) is False:		# else ???
            # remove bottom figure from column and capture it
            self.player.capture_figure(self.board.columns[self.ray_coords['position']].figures.pop(-1))
    
    def return_animation(self):
        if self.my_view.animate_return(self.ray_coords) is False:		# else ???
            # after the ray has finished being drawn
            # if column is empty add captured figure to column
            if len(self.board.columns[self.ray_coords['position']].figures) == 0:
                self.board.columns[self.ray_coords['position']].figures.append(self.player.captured_figure)
            # if bottom figure in column fits captured figure
            elif self.board.columns[self.ray_coords['position']].figures[-1].fits(self.player.captured_figure):
                # and  bottom figure is empty, fit them
                if self.board.columns[self.ray_coords['position']].figures[-1].empty is True:
                    self.board.columns[self.ray_coords['position']].figures[-1].value += self.player.captured_figure.value
                    self.board.columns[self.ray_coords['position']].figures[-1].empty = False
                else:
                    # if bottom figure is not empty
                    # list adjacent compatible figures
                    self.targets = self.board.acquire_targets(
                        self.player.position,
                        self.board.columns[self.player.position].occupancy() - 1)
                    self.all_targets_acquired = True
                    self.player.score += self.player.captured_figure.value
                    print('[#] All targets acquired: {} [{}]'.format(self.all_targets_acquired, len(self.targets)))
                    for target in self.targets:
                        print('\t> Position: {}\t> Height: {}'.format(target[0], target[1]))
                    self.frame = 0
            else:
                # if figures don't fit add to column
                self.board.columns[self.ray_coords['position']].figures.append(self.player.captured_figure)
            self.player.empty()
    
    def explode_all_targets(self):
        if self.frame < 16:
            self.my_view.draw_explosion(self.targets, self.frame)
            self.frame += 1
        else:
            # sorting targets by height, to avoid IndexOutOfBoundsError
            self.targets.sort(key=lambda x: x[1], reverse=True)
            self.player.score += self.board.eliminate_targets(self.targets)
            self.frame = 0
    
    def update_player_stats(self):
        # add new row to self for every 15 moves
        if self.player.steps > 15:
            self.board.add_row()
            self.player.steps = 0
        # recounting stuff on the board
        self.board.update_counts()
        if self.board.longest_column_count >= 10:
            self.game_over()
    
    # ONLINE FUNCTIONS
    def find_online_match(self):
        print('[#] Finding online match...')
        self.mq = zmq_connector.ZmqConnector(self.HOST)
        self.broker = online_broker.OnlineBroker(self.player, self.mq)
    
        text = ''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    self.shutdown()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.clear()
                        self.broker = None
                        self.reset_state()
                        self.welcome_screen()
    
            opponent = self.broker.negotiate()
            if opponent is not None:
                self.player.online = 'playing'
                self.opponent = opponent
                self.play()
    
            # set text for wait-screen
            if self.player.online == 'available':
                text = 'Waiting for challengers'
                # timer = time.process_time()
            elif self.player.online == 'accepted':
                text = 'Challenge has been accepted'
            elif self.player.online == 'challenger':
                text = 'Challenging available opponent'
            elif self.player.online == 'itson':
                text = 'It\'s F**king ON!!!'
                # self.player.online = 'playing'
    
            if self.broker.timeout() is True:
                break
    
            self.my_view.draw_wait_screen(text)
            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)
    
    def check_online_play(self):
        if self.player.connected is True:
            # send  message every 10 frames, read every 20
            if self.send_counter > 10:
                self.send_counter = 0
                self.check_on_opponent()
                self.broker.update_player_stats()
            self.send_counter += 1
            # draw opponents score board
            self.my_view.draw_opponent(self.opponent)
    
    def check_on_opponent(self):
        message = self.mq.sub_receive_multi()
        if message is not None:
            print("[#] Opponent update: {}".format(message))
            self.opponent = json.loads(message[1].decode())
        if self.opponent['online'] == 'over':
            self.victory()
        elif self.opponent['online'] == 'playing':
            if self.rows_received * 20 < int(self.opponent['score']):
                print('[#] Received row')
                self.board.add_row()
                self.rows_received += 1
    
    # END GAME
    def game_over(self):
        self.my_view.draw_game_over()
    
        while True:
            # event handling loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.shutdown()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.event.clear()
                    self.reset_state()
                    self.welcome_screen()
            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)
    
    def victory(self):
        self.my_view.draw_victory()
    
        while True:
            # event handling loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.shutdown()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.event.clear()
                    self.reset_state()
                    self.welcome_screen()
            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)
    
    def reset_state(self):
        if self.mq is not None:
            self.player.online = 'over'
            print('[player] {}'.format(self.player.online))
            if self.opponent is not None:
                message = [self.opponent['sender'], json.dumps(self.player.get_stats())]
                for i in range(len(message)):
                    message[i] = message[i].encode()
                self.mq.push_send_multi(message)
            time.sleep(1)
            self.mq.disconnect()
    
        self.opponent = None
        self.send_counter = 0
        self.explosion_counter = 1
        self.rows_received = 0
        self.player.reset()
    
    @staticmethod
    def shutdown():
        pygame.quit()
        sys.exit()
    
    
if __name__ == '__main__':
    pass
