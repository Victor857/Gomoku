import random
from app.models import PlayerRecord, GameRecord
search_depths = [0, 1, 3, 5, 6]

class Game:
    # 0 represents white 2 represents black and 1 represents none
    def __init__(self, props):
        self.plays = []
        self.board = [1 for i in range(225)]
        self.next_player = 0
        self.play_importance = 0
        self.opponent = props['computer']
        self.difficulty = props['difficulty']
        self.search_depth = search_depths[self.difficulty]
        self.won = 1
        print(f'opponent is {self.opponent}')
        if self.opponent == 0:
            self.play_piece(112)
        self.playerID = props['playerID']

    def play_piece(self, i):
        print(f'play_piece({i})')
        if self.board[i] == 1 and self.won == 1:
            self.board[i] = self.next_player
            self.plays.append(i)
            if self.detect_win(self.next_player):
                self.won = self.next_player
                print(self.won)
            self.next_player = 2 - self.next_player
            return self.get_board()
        return {'updated': False}
            
    def unplay_piece(self):
        if self.plays:
            self.board[self.plays[-1]] = 1
            del self.plays[-1]
            self.next_player = 2 - self.next_player
            return self.get_board()
        return {'updated': False}

    def get_board(self):
        return {'updated': True,'pieces': self.board, 
                'player': self.next_player, 'won' : self.won}
    
    @staticmethod
    def past_games():
        return GameRecord.all_games()
    
    def detect_win(self,n):
        def find5(r):
            c = 0
            for j in r:
                if j == n:
                    c += 1
                    if c == 5:
                        return True
                else:
                    c = 0
            return False

        won = any([find5(self.board[i:i+15]) for i in range(0,225, 15)]) or \
                any([find5(self.board[i:225:15]) for i in range(15)]) or \
                any([find5(self.board[i:i*15+1:14]) 
                    or find5(self.board[210+i:210-i*15-1:-16]) 
                    for i in range(4,14)]) or \
                any([find5(self.board[i:15*(15-i):16]) 
                    or find5(self.board[210+i:15*i:-14]) 
                    for i in range(11)])
        if won:
            if self.playerID != 0:
                a = GameRecord(self.playerID, 2-self.opponent, 
                               self.difficulty, n, self.plays)
            return True
        return False

    
    def computer_play(self):
        return self.play_piece(self.best_move())

    # Produces a list of all moves and their importance based on a board and player
    @staticmethod
    def find_moves(player,board):
        moves = []

        def calc_line(line, indices):
            for i in range(len(line)-5):
                moves.extend(Game.eval5(line[i:i+5], player, indices[i:i+5]))
                moves.extend(Game.eval6(line[i:i+6], player, indices[i:i+6]))
            moves.extend(Game.eval5(line[-5:], player, indices[-5:]))
        
        for i in range(0,225, 15):
            calc_line(board[i:i+15], list(range(i,i+15)))
        for i in range(15):
            calc_line(board[i:225:15], list(range(i, 225, 15)))
        for i in range(4,14):
            calc_line(board[i:i*15+1:14], list(range(i, i*15+1, 14)))
            calc_line(board[210+i:210-i*15-1:-16], list(range(210+i, 210-i*15-1, -16)))
        for i in range(11):
            calc_line(board[i:15*(15-i):16], list(range(i,15*(15-i),16)))
            calc_line(board[210+i:15*i:-14], list(range(210+i,15*i,-14)))

        moves.sort(reverse = True)
        return moves
    

    # Takes list of all moves sorted by importance and produces a list with the
    # the list of viable moves
    @staticmethod
    def moveset(moves):
        importance = moves[0][0]
        res = []
        if importance >= 60:
            if importance == 60 or importance == 80:
                if importance == 60:
                    limit = 50
                else:
                    limit = 80
                for i, m in moves:
                    if i < limit:
                        break
                    if m not in res:
                        res.append(m)
                return res
            if importance == 90:
                return [moves[0][1]]
            return [moves[0][1]]

        for _, m in moves[:5]:
            if m not in res:
                res.append(m)
        return res

    # Takes sorted move list and produces how much the game is favour of 
    # the player
    @staticmethod
    def check_advantage(moves, maximizer):
        advantage = 0
        importance = moves[0][0]
        if importance == 70 or importance == 100:
            advantage = float('inf')
        elif  importance == 90:
            advantage = float('-inf')
        else:
            for importance, posn in moves:
                if importance <= 20:
                    if importance == 20:
                        advantage += 5
                    else:
                        advantage -= 5
                elif importance >=60: 
                    if importance == 60 or importance == 80:
                        advantage -= 250
                    else:
                        advantage += 1000
                elif importance == 30:
                    advantage -= 100
                elif importance == 50 or importance == 40:
                    advantage += 100
        if maximizer:
            return advantage
        return -advantage

    @staticmethod
    def eval5(pcs, p, indices):
        empties = pcs.count(1)
        if empties == 5:
            return []
        o = 2 - p
        p_count = pcs.count(p)
        o_count = 5 - empties - p_count
        if p_count == 4 and empties == 1:
            return [(100, indices[pcs.index(1)])]
        if o_count == 4 and empties == 1:
            return [(80, indices[pcs.index(1)])]
        if p_count == 3 and empties == 2:
            if pcs[0] == 1:
                return [(50, indices[0]), (50, indices[pcs.index(1,1)])]
            if pcs[4] == 1:
                return [(50, indices[pcs.index(1)]), (50, indices[4])]
        if o_count == 3 and empties == 2:
            i = pcs.index(1)
            return [(30, indices[i]), (29, indices[pcs.index(1, i+1)])]
        return []

    # x player, o opponent, _ empty
    # 100: xxxx_ win
    # 90: _xxxx_ lose
    # 80: oooo_  -250
    # 70: _x_xx_ +1000
    # 60: _o_oo_ -250
    # 50: x_x_x  +100
    # 40: __xx__ +100
    # 30: __oo__ or o_o_o -100
    # 20: __x___ +5 
    # 10: __o___ -5
    @staticmethod
    def eval6(pcs, p, indices):
        empties = pcs.count(1)
        if empties == 6:
            return []
        o = 2 - p
        p_count = pcs.count(p)
        o_count = 6 - empties - p_count
        if pcs[0] == 1 and pcs[5] == 1:
            if o_count == 4:
                return [(90, indices[0])]
            if p_count == 3 and empties == 3:
                return [(70, indices[pcs.index(1,1)])]
            if o_count == 3 and empties == 3:
                return [(60, indices[pcs.index(1,1)]), (59, indices[0]),(59, indices[5])]
            if p_count == 2 and empties == 4:
                i1 = pcs.index(1,1)
                return [(40, indices[i1]), (39, indices[pcs.index(1, i1+1)])]
            if o_count == 2 and empties == 4:
                i1 = pcs.index(1,1)
                return [(30, indices[i1]), (29, indices[pcs.index(1, i1+1)])]
        if empties == 5:
            if p_count == 1:
                i1 = pcs.index(p)
                if i1 == 2:
                    return [(20, indices[3])]
                if i1 == 3:
                    return [(20, indices[2])]
            if o_count == 1:
                i1 = pcs.index(o)
                if i1 == 2:
                    return [(10, indices[3])]
                if i1 == 3:
                    return [(10, indices[2])]
        return []
                 
    # consumes a board, remaining search depth, max score of maximizing player
    # max score of minimizing player, who is now playing and whether maximizing
    @staticmethod
    def alphabeta(board, depth, alpha, beta, player, maximizing):
        moves = Game.find_moves(player, board)
        if not moves:
            return 0
        if depth == 0:
            return Game.check_advantage(moves, maximizing)
        if moves[0][0] == 90:
            if maximizing:
                return float('-inf')
            return float('inf')
        if moves[0][0] == 100 or moves[0][0] == 70:
            if maximizing:
                return float('inf')
            return float('-inf')
        moveset = Game.moveset(moves)
        if maximizing:
            curr_advantage = float('-inf')
            for newmove in moveset:
                newboard = board[:]
                newboard[newmove] = player
                curr_advantage = max(curr_advantage, 
                        Game.alphabeta(newboard, depth - 1, alpha, beta, 2-player, False))
                #print(depth, newmove, curr_advantage)
                alpha = max(alpha, curr_advantage)
                if alpha >= beta:
                    break
        else:
            curr_advantage = float('inf')
            for newmove in moveset:
                newboard = board[:]
                newboard[newmove] = player
                curr_advantage = min(curr_advantage, 
                        Game.alphabeta(newboard, depth - 1, alpha, beta, 2-player, True))
                #print(depth, maximizing, newmove, curr_advantage)
                beta = min(beta, curr_advantage)
                if beta <= alpha:
                    break
        return curr_advantage
            
    def random_move(self):
        if self.board[112] == 1:
            return 112
        for i, p in enumerate(self.board):
            if p == 1:
                return p

    def best_move(self):
        print('!!!!!!best move!!!!!!!',self.next_player, self.opponent, self.won)
        if self.next_player != self.opponent:
            return {'updated': False}
        player = self.opponent
        moves = Game.find_moves(player, self.board)
        if not moves:
            return self.play_piece(self.random_move())
        print(moves)
        if self.search_depth == 0 or moves[0][0] in [70, 90, 100]:
            return self.play_piece(moves[0][1])
        bestmoves = []
        max_val = float('-inf')
        for move in Game.moveset(moves):
            #print(move)
            newboard = self.board[:]
            newboard[move] = player
            advantage = Game.alphabeta(newboard, self.search_depth-1, 
                    float('-inf'), float('inf'), 2-player, False)
            print(move, advantage)
            if advantage >= max_val:
                if advantage == max_val:
                    bestmoves.append(move)
                else:
                    max_val = advantage
                    bestmoves = [move]
        return self.play_piece(random.choice(bestmoves))


    def print_board(self):
        pieces = {1:'  ', 0:'▮ ', 2: '▯ '}
        for i in range(0, 225, 15):
            print(''.join((pieces[n] for n in self.board[i:i+15])))


def tst1():
    g = Game()
    g.play_piece(110)
    g.print_board()
    print(Game.find_moves(2, g.board))
    print(g.best_move(2))
    g.play_piece(95)
    g.play_piece(111) 
    g.print_board()
    print(Game.find_moves(2, g.board))
    print(g.best_move(2))
    g.play_piece(81)
    g.play_piece(112)
    g.print_board()
    print(Game.find_moves(2, g.board))
    print(g.best_move(2))

def test2(black, white):
    g = Game({'computer': 2, 'search_depth': 0, 'playerID': ''})
    for a, b in zip(black, white):
        g.play_piece(a)
        g.play_piece(b)
    if len(black) > len(white):
        g.play_piece(black[-1])
    g.print_board()
    g.computer_play()
    g.print_board()



if __name__ == '__main__':
    black = (112, 113, 98)
    white = (128, 114)
    test2(black, white)

