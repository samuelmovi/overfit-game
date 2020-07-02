import pygame
import sys
import datetime
import time
import json
import os
from model import board, zmq_client, online_broker
from pygame.locals import *

    
class Controller:
    
    # constants
    RIGHT = 'right'
    LEFT = 'left'
    FPSCLOCK = None
    FPS = 30  # frames per second to update the screen, and execute code
    AP_Q = 'ap_q'
    
    # variables
    frame = 0  # to keep track of frames during explosion animations
    base_dir = os.path.join(os.getcwd(), '../')
    keyword = ""  # stores value used to control flow inside main_loop:
    draw_again = True
    loop_finished = False
    txt_msg = ""  # hold string to be displayed on waiting screens

    # model instances
    board = None
    broker = None
    mq = None
    view = None
    player = None
    
    # gameplay variables
    # explosion_counter = 1
    rows_received = 1
    ray_coords = {}
    targets = []        # list of figures to be destroyed during gameplay
    all_targets_acquired = False
    player_stats = {}  # dictionary for the players own stats
    
    # online variables
    HOST = '127.0.0.1'
    landing_data = None     # hold match data sent by server for display on landing page
    match_state = {'id': '', 'name': '', 'status': '', 'score': 0, 'total': 0, 'longest': 0}
    opponent_state = {'id': 'XXX', 'name': 'XXX', 'status': '', 'score': 0, 'total': 0, 'longest': 0}
    opponent = None      # id of opponent
    
    def __init__(self, view, player, mq, broker):
        print('[#] Initiating Controller...')
        self.mq = mq
        self.broker = broker
        
        pygame.init()
        pygame.mixer.quit()
        self.FPSCLOCK = pygame.time.Clock()
        pygame.display.set_caption('WeeriMeeris')
        
        self.player = player
        self.view = view
        self.view.set_up_fonts()
        
    def main_loop(self):
        inputs = None
        self.keyword = "start"

        while not self.loop_finished:
            # check if screen needs redrawing
            if self.draw_again:
                # draw screen based on keyword value, return input objects, if any
                inputs = self.draw(self.keyword)
                
            if self.keyword == "start":
                self.welcome_listener(inputs)
            elif self.keyword == "game":
                self.game_handler()
            elif self.keyword == "online_setup":
                self.online_setup_listener(inputs)
            elif self.keyword == "connect_online":
                # connect with server
                try:
                    self.mq.start(self.HOST, self.player.ID)
                    self.player.online = "connected"
                except Exception as e:
                    print(f"[main_loop] Error connect_online: {e}")
                    self.keyword = "online_setup"
                    self.draw_again = True
                time.sleep(0.1)
                # send welcome message
                info = {'status': 'WELCOME', 'recipient': 'SERVER'}
                self.mq.send(self.player.ID, info, {})
                for i in range(5):
                    response = self.mq.sub_receive_multi()
                    if response:
                        # display landing page
                        # print(f"[@] Got Response: {response}")
                        self.landing_data = response
                        self.keyword = "landing_page"
                        self.draw_again = True
                        self.player.online = "connected"
                        break
                    else:
                        time.sleep(0.01)
                        if i == 4:
                            print("[!!!] Response timeout")
                            self.keyword = "online_setup"
                            self.draw_again = True
            elif self.keyword == "landing_page":
                self.landing_listener(inputs)
            elif self.keyword == "find_online_match":
                self.find_match()
                self.find_match_listener()
            elif self.keyword == "settings":
                self.settings_listener(inputs)
            elif self.keyword == "confirm_exit":
                self.confirm_exit_listener(inputs)
            elif self.keyword == "confirm_leave":
                self.confirm_leave_listener(inputs)
            elif self.keyword == "game_over":
                self.game_over_listener()
            elif self.keyword == "victory":
                self.victory_listener()

            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)
            
    def draw(self, keyword):
        inputs = None
        if keyword == "start":
            inputs = self.view.draw_start_screen()
        elif keyword == "game":
            pass    # why??
        elif keyword == "online_setup":
            inputs = self.view.draw_online_options_screen(self.player.name, self.HOST)
        elif keyword == "landing_page":
            match_data = json.loads(self.landing_data[2])
            inputs = self.view.draw_landing_screen(self.HOST, self.player.name, match_data)
        elif keyword == "find_online_match":
            self.view.draw_wait_screen()
        elif keyword == "settings":
            inputs = self.view.draw_settings_screen(self.player.name, self.HOST)
        elif keyword == "confirm_exit":
            inputs = self.view.confirm_exit()
        elif keyword == "confirm_leave":
            inputs = self.view.confirm_leave_game()
        elif keyword == "game_over":
            self.view.draw_game_over()
        elif keyword == "victory":
            self.view.draw_victory()

        self.draw_again = False
        return inputs
       
    # EVENT LISTENERS
    def welcome_listener(self, inputs):
        # check for and handle events
        single_player_button, online_multi_button, settings_button = inputs

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop_finished = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.keyword = "confirm_exit"
                self.draw_again = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                if single_player_button.rect.collidepoint((mouse_x, mouse_y)):
                    self.keyword = 'game'
                    self.draw_again = True
                    print('[#] Game START!')
                    self.board = board.Board() 
                    self.board.setup()                
                elif online_multi_button.rect.collidepoint((mouse_x, mouse_y)):
                    self.keyword = 'online_setup'
                    self.draw_again = True
                    # print('[#] Opponent: {}'.format(self.opponent))
                elif settings_button.rect.collidepoint((mouse_x, mouse_y)):
                    self.keyword = 'settings'
                    self.draw_again = True
    
    def game_listener(self):
        # event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                self.loop_finished = True
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
                    self.keyword = "connect_online"
                    self.draw_again = True
        self.view.refresh_input(input_boxes)
    
    def landing_listener(self, inputs):
        find_match_button = inputs
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop_finished = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # should ask for confirmation to leave server
                self.keyword = "online_setup"
                self.draw_again = True
                # disconnect from server
                self.broker.quit()
                self.player.online = ''
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                if find_match_button.rect.collidepoint((mouse_x, mouse_y)):
                    self.keyword = 'find_online_match'
                    self.draw_again = True
    
    def find_match_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                self.loop_finished = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.clear()
                    # back to landing page
                    self.keyword = "landing_page"
                    self.draw_again = True
                    self.player.online = 'connected'
                    # send welcome message
                    info = {'status': 'WELCOME', 'recipient': 'SERVER'}
                    self.mq.send(self.player.ID, info, {})
                    print("[C] Retrieving landing page data...")
                    for i in range(5):
                        response = self.mq.sub_receive_multi()
                        if response:
                            self.landing_data = response
                            break
    
    def settings_listener(self, inputs):
        input_boxes, save_button = inputs

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop_finished = True
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
                    # go back to main window
                    pygame.event.clear()
                    self.keyword = "start"
                    self.draw_again = True
            for instance in input_boxes:
                instance.handle_event(event)
        self.view.refresh_input(input_boxes)
    
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
                    self.keyword = "game"       # redundant??
                    self.draw_again = True
    
    def game_over_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop_finished = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.event.clear()
                self.reset_state()
                self.keyword = "landing_page"
                self.draw_again = True
    
    def victory_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop_finished = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.event.clear()
                self.reset_state()
                self.keyword = "start"
                self.draw_again = True
    
    # GAMING FUNCTIONS
    
    def game_handler(self):
        # check for user input and execute commands
        self.game_listener()
        # update player stats to accommodate for changes due to executed commands
        self.update_match_state()
        # update board model top display changes
        self.board.update_counts()
        
        # check for online play
        if self.player.online == 'playing':
            self.check_on_opponent()
            self.update_player_stats()

        # paint changes to view
        self.view.update_game_screen(self.player, self.board, self.opponent_state)
        
        # check for capture
        if self.player.status == 'capturing':
            self.capture_animation()
        # check for return
        elif self.player.status == 'returning':
            self.return_animation()
        # check for explosion
        if self.all_targets_acquired is True:
            self.explode_all_targets()
    
    def capture_animation(self):
        if self.view.animate_return(self.ray_coords) is False:
            # remove bottom figure from column and capture it
            self.player.capture_figure(self.board.columns[self.ray_coords['position']].figures.pop(-1))
    
    def return_animation(self):
        # after the ray has finished being drawn
        if self.view.animate_return(self.ray_coords) is False:
            # if bottom figure in column fits returned figure
            if self.board.columns[self.ray_coords['position']].figures[-1].fits(self.player.captured_figure):
                # and  bottom figure is empty, fit them
                if self.board.columns[self.ray_coords['position']].figures[-1].empty is True:
                    self.board.columns[self.ray_coords['position']].figures[-1].value += self.player.captured_figure.value
                    self.board.columns[self.ray_coords['position']].figures[-1].empty = False
                else:
                    # if bottom figure is not empty it will explode
                    # list adjacent compatible figures
                    self.targets.clear()
                    self.targets = self.board.acquire_targets(
                        self.player.position,
                        self.board.columns[self.player.position].occupancy() - 1)
                    self.all_targets_acquired = True    # so game_handler knows to explode them
                    self.player.score += self.player.captured_figure.value
                    print('[#] All targets acquired: {} [{}]'.format(self.all_targets_acquired, len(self.targets)))
                    for target in self.targets:
                        print('\t> Position: {}\t> Height: {}'.format(target[0], target[1]))
                    self.frame = 0      # required for explosion handling
            else:
                # add figure to column
                self.board.columns[self.ray_coords['position']].figures.append(self.player.captured_figure)
            self.player.empty()
    
    def explode_all_targets(self):
        if self.frame < 16:
            # continue drawing the explosion
            self.view.draw_explosion(self.targets, self.frame)
            self.frame += 1
        else:
            # eliminate all exploded figures from board
            # sorting targets by height, to avoid IndexOutOfBoundsError
            self.targets.sort(key=lambda x: x[1], reverse=True)
            self.player.score += self.board.eliminate_targets(self.targets)
            self.frame = 0
            self.all_targets_acquired = False
    
    def update_match_state(self):
        # add new row to self for every 15 moves
        if self.player.steps > 15:
            self.board.add_row()
            self.player.steps = 0
        # recounting stuff on the board
        self.board.update_counts()
        if self.board.longest_column_count >= 10:
            self.keyword = "game_over"
            self.draw_again = True
    
    # ONLINE FUNCTIONS
    def find_match(self):
        # checks for opponent from broker and responds accordingly
        opponent = self.broker.negotiate_match()
        if opponent:
            self.player.online = 'playing'
            self.opponent = opponent
            self.keyword = "game"
            self.draw_again = True
            print('[#] Game START!')
            print(f'[#] Opponent: {self.opponent}')
            self.board = board.Board()
            self.board.setup()
        else:
            text = "waiting message goes here"
            # set text for wait-screen
            if self.player.online == 'available':
                text = 'Waiting for challengers'
                self.draw_again = True
            elif self.player.online == 'ready':
                text = 'Get ready to start'
                self.draw_again = True
            self.txt_msg = text
    
    def check_on_opponent(self):
        # check for messages from opponent and update info
        message = self.mq.sub_receive_multi()
        if message:
            info = json.loads(message[1])
            self.opponent_state = json.loads(message[2])
            if info['status'] == 'OVER':
                # i won!
                self.keyword = "victory"
                self.draw_again = True
            elif info['status'] == 'PLAYING':
                # self.view.draw_opponent(self.opponent_state)
                if self.rows_received * 20 < int(self.opponent_state['score']):
                    print('[#] Received row')
                    self.board.add_row()
                    self.rows_received += 1

    def update_player_stats(self):
        # check for changes in player stats, and inform server
        current_stats = self.player.get_stats()
        if current_stats != self.player_stats:
            print('[C] Updating opponent about player stats')
            self.player_stats = current_stats
            # send new stats to opponent
            sender = self.player.ID
            info = {'status': 'PLAYING', 'recipient': self.opponent}
            self.match_state = {'id': sender,
                                'name': self.player.name,
                                'status': self.player.status,
                                'score': self.player.score,
                                'total': self.board.figure_count,
                                'longest': self.board.longest_column_count,
                                }
            self.mq.send(sender, info, self.match_state)
    
    def reset_state(self):
        # disconnect zmq handler
        if self.mq.connected:
            # disconnect from server with QUIT message
            sender = self.player.ID
            info = {'status': 'QUIT', 'recipient': 'SERVER'}
            self.mq.send(sender, info, {})
            time.sleep(0.01)
            # close sockets
            self.mq.disconnect()
        
        # reset value of game variables
        self.opponent = None
        self.opponent_state = {'id': '', 'name': '', 'status': '', 'score': 0, 'total': 0, 'longest': 0}
        # self.explosion_counter = 1
        self.rows_received = 0
        self.player.reset()

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
    
    
# if __name__ == '__main__':
#     pass
