import unittest
import pylos
from lib import game

class TestPylosState(unittest.TestCase):
    def test_board(self):
        state = pylos.PylosState()

        # Should raise because out of board
        for coord in [[0,-1,0], [0,0,-1], [4,0,0], [0,4,0], [0,0,4], [1,3,0], [1,0,3], [2,2,0], [2,0,2], [3,1,0], [3,0,1]]:
            with self.assertRaises(game.InvalidMoveException, msg="place to {}".format(coord)):
                state.update({
                    'move': 'place',
                    'to': coord
                }, 0)
        
        layer = 0
        for row in range(4-layer):
            for column in range(4-layer):
                if layer != 0 or row != 3 or column != 3:
                    state.update({
                        'move': 'place',
                        'to': [layer,row,column]
                    }, 0)
                    self.assertEqual(state.get(layer,row,column), 0)

        # Should raise because no more sphere
        with self.assertRaises(game.InvalidMoveException):
            state.update({
                'move': 'place',
                'to': [0, 3, 3]
            }, 0)

        # Fill the first layer
        state.update({
            'move': 'place',
            'to': [0, 3, 3]
        }, 1)
        self.assertEqual(state.get(0,3,3), 1)

        # Fill the board
        for layer in range(1, 4):
            for row in range(4-layer):
                for column in range(4-layer):
                    if layer != 3 or row != 0 or column != 0:
                        state.update({
                            'move': 'place',
                            'to': [layer,row,column]
                        }, 1)
                        self.assertEqual(state.get(layer,row,column), 1)

        # Should raise because sphere not free
        for layer in range(3):
            for row in range(4-layer):
                for column in range(4-layer):
                    with self.assertRaises(game.InvalidMoveException):
                        player = state.get(layer,row,column)
                        state.update({
                            'move': 'move',
                            'from': [layer,row,column],
                            'to': [3,0,0]
                        }, player)

    def test_promoteSphere(self):
        state = pylos.PylosState()

        state.update({
            'move': 'place',
            'to': [0, 0, 0]
        }, 0)
        state.update({
            'move': 'place',
            'to': [0, 0, 1]
        }, 1)
        state.update({
            'move': 'place',
            'to': [0, 1, 1]
        }, 0)
        state.update({
            'move': 'place',
            'to': [0, 1, 0]
        }, 1)
        state.update({
            'move': 'place',
            'to': [0, 0, 2]
        }, 0)
        state.update({
            'move': 'place',
            'to': [0, 2, 0]
        }, 1)

        # Should raise because not his sphere
        with self.assertRaises(game.InvalidMoveException):
            state.update({
                'move': 'move',
                'from': [0, 2, 0],
                'to': [1, 0, 0]
            }, 0)

        state.update({
            'move': 'move',
            'from': [0, 0, 2],
            'to': [1, 0, 0]
        }, 0)
    
    def test_square(self):
        state = pylos.PylosState()

        state.update({
            'move': 'place',
            'to': [0, 0, 0]
        }, 0)
        state.update({
            'move': 'place',
            'to': [0, 3, 3]
        }, 1)

        state.update({
            'move': 'place',
            'to': [0, 1, 0]
        }, 0)
        state.update({
            'move': 'place',
            'to': [0, 2, 3]
        }, 1)

        # Should raise because no square created
        with self.assertRaises(game.InvalidMoveException):
            state.update({
                'move': 'place',
                'to': [0, 0, 1],
                'remove': [
                    [0, 0, 0],
                    [0, 1, 0]
                ]
            }, 0)
        state.update({
            'move': 'place',
            'to': [0, 3, 2]
        }, 1)

        state.update({
            'move': 'place',
            'to': [0, 1, 1],
            'remove': [
                [0, 0, 0],
                [0, 1, 0]
            ]
        }, 0)

        # Should raise because trying to remove sphere from other player
        with self.assertRaises(game.InvalidMoveException):
            state.update({
                'move': 'place',
                'to': [0, 2, 2],
                'remove': [
                    [0, 3, 3],
                    [0, 1, 1]
                ]
            }, 1)

    def test_moveToSamePlace(self):
        state = pylos.PylosState()
        for layer in range(4):
            for row in range(4-layer):
                for column in range(4-layer):
                    state.set([layer, row, column], 0)
                    with self.assertRaises(game.InvalidMoveException):
                        state.update({
                            'move': 'move',
                            'from': [layer, row, column],
                            'to': [layer, row, column]
                        }, 0)



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPylosState)
    runner = unittest.TextTestRunner()
    exit(not runner.run(suite).wasSuccessful())