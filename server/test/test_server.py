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
        mock_mq = Mock()
        # execute method
        test_server = server.PullPubServer(mock_mq, mock_db)
        # assert expected outcome
        self.assertIsNotNone(test_server.mq)
        self.assertIsNotNone(test_server.db)
        self.assertEqual(mock_mq, test_server.mq)
        self.assertEqual(mock_db, test_server.db)
        self.assertEqual(len(test_server.online_players), 0)
        self.assertEqual(len(test_server.available_players), 0)
        # TODO: fix this failing when other test methods use matches -> self.assertEqual(len(test_server.matches), 0)
        self.assertTrue(mock_mq.setup.called)
    
    def test_onboard_client(self):
        # prepare state
        mock_db = Mock()
        mock_mq = Mock()
        test_server = server.PullPubServer(mock_mq, mock_db)
        sender = "sender_id1"
        # execute method
        test_server.onboard_client(sender)
        # assert expected results
        self.assertEqual(len(test_server.online_players), 1)
        # assert db.load_matches() called
        self.assertTrue(mock_db.load_matches.called)
        # assert mq.send() called
        self.assertTrue(mock_mq.send.called)
        # TODO: assert data passed to send()

    def test_handle_welcome(self):
        sender = "sender_id1"
        # TODO: assert data passed to mq.send()
        # SCENARIO 1: sender not in available players
        # prepare state
        mock_db = Mock()
        mock_mq = Mock()
        test_server = server.PullPubServer(mock_mq, mock_db)
        # execute method
        test_server.handle_welcome(sender)
        # assert expected results
        self.assertTrue(mock_db.load_matches.called)
        self.assertTrue(mock_mq.send.called)

        # SCENARIO 2: sender in available players
        # prepare state
        mock_db = Mock()
        mock_mq = Mock()
        test_server = server.PullPubServer(mock_mq, mock_db)
        test_server.available_players.append(sender)
        # execute method
        test_server.handle_welcome(sender)
        # assert expected results
        self.assertTrue(mock_db.load_matches.called)
        self.assertTrue(mock_mq.send.called)
        self.assertEqual(len(test_server.available_players), 0)

    def test_handle_available(self):
        sender = "sender_id1"
        # SCENARIO 1: no available players
        # prepare state
        mock_db = Mock()
        mock_mq = Mock()
        test_server = server.PullPubServer(mock_mq, mock_db)
        # execute method
        test_server.handle_available(sender)
        # assert expected results
        self.assertEqual(len(test_server.available_players), 1)
        self.assertEqual(test_server.available_players[0], sender)
        self.assertTrue(mock_mq.send.called)
        
        # SCENARIO 2: 1 available player
        opponent = "opponnent1"
        # prepare state
        mock_db2 = Mock()
        mock_mq2 = Mock()
        test_server2 = server.PullPubServer(mock_mq2, mock_db2)
        test_server2.available_players[0] = opponent
        # execute method
        test_server2.handle_available(sender)
        # assert expected results
        self.assertEqual(len(test_server2.available_players), 0)
        self.assertTrue(mock_mq2.send.called)
        # TODO: test number of send calls and data
        # TODO: assert ids in new match
        self.assertEqual(len(test_server2.matches), 1)

    def test_handle_ready(self):
        sender = "sender_id1"
        opponent = "opponnent1"
        # SCENARIO 1: match exists
        # prepare state
        mock_db = Mock()
        mock_mq = Mock()
        test_server = server.PullPubServer(mock_mq, mock_db)
        test_match = {sender: 'WAIT', opponent: 'READY'}
        test_server.matches[0] = test_match
        # execute method
        test_server.handle_ready(sender)
        # assert expected results
        # TODO: assert time called, and data
        self.assertTrue(mock_mq.send.called)

        # SCENARIO 2: no matching match
        # prepare state
        mock_db2 = Mock()
        mock_mq2 = Mock()
        test_server2 = server.PullPubServer(mock_mq2, mock_db2)
        test_server2.matches = []
        # execute method
        test_server2.handle_ready(sender)
        # assert expected results
        # TODO: assert times called, and data
        self.assertFalse(mock_mq2.send.called)

    def test_handle_playing(self):
        sender = "sender_id1"
        opponent = "opponnent1"
        # SCENARIO 1: match exists
        # prepare state
        mock_db = Mock()
        mock_mq = Mock()
        test_server = server.PullPubServer(mock_mq, mock_db)
        # execute method
        test_server.handle_playing(sender, opponent, {'sender': sender, 'status': 'PLAYING'})
        # assert expected results
        # TODO: assert data
        self.assertTrue(mock_mq.send.called)
    
    def test_handle_over(self):
        sender = "sender_id1"
        opponent = "opponnent1"
        # SCENARIO 1: match exists
        # prepare state
        mock_db = Mock()
        mock_mq = Mock()
        test_server = server.PullPubServer(mock_mq, mock_db)
        test_match = {sender: 'PLAY', opponent: 'PLAY'}
        test_server.matches[0] = test_match
        payload = {}
        # execute method
        test_server.handle_over(sender, payload)
        # assert expected results
        self.assertEqual(test_server.matches[0][sender], 'LOST')
        self.assertEqual(test_server.matches[0][opponent], 'WON')
        # TODO: assert data
        self.assertTrue(mock_db.save_match.called)
        self.assertTrue(mock_mq.send.called)

    def test_handle_quit(self):
        sender = "sender_id1"
        # SCENARIO 1: match exists
        # prepare state
        mock_db = Mock()
        mock_mq = Mock()
        test_server = server.PullPubServer(mock_mq, mock_db)
        test_server.online_players.append(sender)
        # execute method
        test_server.handle_quit(sender)
        # assert expected results
        self.assertEqual(len(test_server.online_players), 0)
        self.assertNotIn(sender, test_server.online_players)


if __name__ == '__main__':
    unittest.main()
