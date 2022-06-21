import chess
import heuristic

"""takes a board, and returns a prioritized list of promising legal moves.TODO: CAN BE OPTIMIZED
WITH NEGAMAX TO AVOID UNNCESSARY REALLOCATIONS FOR LISTS"""
def prioritize(board):
    checks=[]
    captures=[]
    other=[]
    for move in board.legal_moves:
        if board.gives_check(move):
            checks.append(move)
        elif board.is_capture(move):
            captures.append(move)
        else:
            other.append(move)
    return checks+captures+other

def trim(board): 
    return False



""" A class to represent a line 

class Line: 
    def __init__(self): 
        self.moves=[]

    def __str__(self):
        print(self.moves)

    def add (self, move): 
        self.append(move)

    def remove(self):
        self.pop
"""



"""Search function with alpha-beta pruning. Currently not handling three-fold repetition
or fifty-move rule draws because checking is slow"""
def negamax(board,depth,alpha, beta, line):
    if board.is_game_over(): 
        return (heuristic.shallow_eval(board), None, line)
    #if recursion depth reached
    if depth==0:
            return (heuristic.shallow_eval(board), None, line)
    #otherwise, recurse.
    move_list=prioritize(board)
    #the initialized out value must be greater then the initialized alpha value or it can return as None
    out=(-10000,None, line)
    for move in move_list:
        board.push(move)
        line.append(move)
        child=negamax(board, depth-1, -beta, -alpha, line)
        new_evaluation=-(child[0])
        new_line=child[2]
        old_evaluation=out[0]
        if (new_evaluation>old_evaluation):
            out=(new_evaluation, move, new_line.copy())
        alpha=max(new_evaluation, alpha)
        if alpha>=beta:
            board.pop()
            line.pop()
            break
        board.pop()
        line.pop()
    return out
