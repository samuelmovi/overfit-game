import unittest
import sys
import os
from unittest.mock import Mock

sys.path.append(os.path.abspath('../src/'))
import server


class TestServer(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(TestServer, self).__init__(*args, **kwargs)
        pass
    
    def test_init(self):
        # set object state
        mock_db = Mock()
        mock_connector = Mock()
        # execute method
        test_server = server.PullPubServer(mock_connector, mock_db)
        # assert expected outcome
        self.assertIsNotNone(test_server.mq)
        self.assertIsNotNone(test_server.db)
        self.assertEqual(mock_connector, test_server.mq)
        self.assertEqual(mock_db, test_server.db)

    def test_onboard_client(self, sender):
        # # add player id to active_players
        # self.online_players.append(sender)
        # print(f"[#] User '{sender}' added to online_players")
        # # send directly to landing
        # # send landing page info
        # new_info = {'status': 'WELCOME', 'sender': 'SERVER'}
        # match_data = self.db.load_matches()
        # self.mq.send(sender, new_info, match_data)
        pass

    def test_handle_welcome(self, sender):
        # # if sender in available players, remove
        # if sender in self.available_players:
        #     self.available_players.remove(sender)
        #     print(f"[#] User '{sender}' removed from available players")
        # # send landing page info
        # new_info = {'status': 'WELCOME', 'sender': 'SERVER'}
        # match_data = self.db.load_matches()
        # self.mq.send(sender, new_info, match_data)
        pass

    def handle_available(self, sender):
        # # check for available players to match client with
        # if len(self.available_players) > 0:
        #     print("[#] Pairing up available players...")
        #     player_1 = self.available_players.pop()
        #     player_2 = sender
        #     # send ready signal to both players
        #     for client in (player_1, player_2):
        #         new_info = {'sender': 'SERVER', 'status': 'READY'}
        #         self.mq.send(client, new_info, {})
        #     # add match to matches
        #     match = dict()
        #     match[player_1] = 'playing'
        #     match[player_2] = 'playing'
        #     self.matches.append(match)
        # else:
        #     print("[#] No other players available...")
        #     # add to available_players
        #     self.available_players.append(sender)
        #     print(f"[#] Adding '{sender}' to available players")
        #     # respond
        #     new_info = {'sender': 'SERVER', 'status': 'WAIT'}
        #     self.mq.send(sender, new_info, {})
        pass

    def handle_ready(self, sender):
        # # find corresponding match and set client as ready
        # # TODO: this code doesn't look efficient, should be improved
        # # send PLAY messages, with each other as sender
        # for match in self.matches:
        #     if sender in match.keys():
        #         match[sender] = 'READY'
        #         # check if both are ready
        #         c = 0
        #         for key in match.keys():
        #             if match[key] == 'READY':
        #                 c += 1
        #         if c == 2:
        #             # both are ready, send command START
        #             players = list(match.keys())
        #             # inform one player
        #             new_info = {'sender': players[1], 'status': 'START'}
        #             self.mq.send(players[0], new_info, {})
        #             # inform the other
        #             new_info = {'sender': players[0], 'status': 'START'}
        #             self.mq.send(players[1], new_info, {})
        #         else:
        #             # continue
        #             break
        pass

    def handle_playing(self, recipient, sender, payload):
        # # if playing, reformat and resend
        # new_info = {'sender': sender, 'status': 'PLAYING'}
        # self.mq.send(recipient, new_info, payload)
        pass

    def handle_over(self, sender, payload):
        # # find match of sender
        # loser = sender
        # winner = None
        # for match in self.matches:
        #     if loser in match.keys():
        #         # set loser
        #         match[loser] = 'LOSER'
        #     # inform other client
        #     for key in match.keys():
        #         if key != loser:
        #             winner = key
        #             match[winner] = 'WINNER'
        # # capture match data and create new db entry
        # self.db.save_match(winner, loser)
        # # forward message to winner
        # new_info = {'sender': 'SERVER', 'status': 'OVER'}  # OVER commands signals victory
        # self.mq.send(winner, new_info, payload)
        pass

    def handle_quit(self, sender):
        # # remove player id from online_players
        # self.online_players.remove(sender)
        # print(f"[#] User '{sender}' removed from online players")
        pass


if __name__ == '__main__':
    unittest.main()
