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


def negamax(board,depth,alpha, beta, current_line: list):
    if board.is_game_over() or board.can_claim_draw():
        if board.outcome()==None:
            return 0,None
        if board.outcome()==board.turn:
            return -1000,None
        else:
            return 1000,None
    if depth==0:
        return heuristic.shallow_eval(board)
    #move_list=prioritize(board)
    move_list=board.legal_moves
    new_line=current_line
    out=(-10000000000000,"None",new_line)
    for move in move_list:
        board.push(move)
        new_line.append(move)
        evaluation=-negamax(board, depth-1, -beta, -alpha, new_line)[0]
        alpha=max(evaluation, alpha)
        if (evaluation>out[0]):
            out=(evaluation,move,new_line)
        if alpha>=beta:
            board.pop()
            new_line.pop()
            break
        board.pop()
        new_line.pop()
    out=(out[0], out[1], out[2].append(out[1]))
    return out