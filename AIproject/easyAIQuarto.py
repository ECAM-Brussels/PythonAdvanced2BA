from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax
from quarto import QuartoState
import copy

class Quarto(TwoPlayersGame):
    def __init__(self, players):
        self.players = players
        self.nplayer = 1 # player 1 starts
        self.state = QuartoState()

    def possible_moves(self):
        state = self.state._state['visible']
        moves = []

        if state['pieceToPlay'] is None:
            for i in range(len(state['remainingPieces'])):
                moves.append({'nextPiece': i})
            return moves

        for p in range(16):
            if state['board'][p] is None:
                for n in range(len(state['remainingPieces'])-1):
                    move = {
                        'pos': p,
                        'nextPiece': n,
                        'quarto': True
                    }

                    try:
                        stateCopy = copy.deepcopy(self.state)
                        stateCopy.applymove(move)
                    except:
                        del(move['quarto'])
                    
                    moves.append(move)
        return moves

    def make_move(self,move):
        self.state.applymove(move)

    def is_over(self):
        return self.state.winner() != -1

    def show(self):
        self.state.prettyprint()

    def scoring(self):
        if self.state.winner() is None:
            return 0
        
        if self.state.winner() != -1:
            return 100
        
        return -100

game = Quarto( [ AI_Player(Negamax(2)), AI_Player(Negamax(2)) ] )
history = game.play()

print(history)