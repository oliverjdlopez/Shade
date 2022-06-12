import chess
import eval

def negamax(board,depth,alpha, beta):
    if board.is_game_over() or board.can_claim_draw():
        if board.outcome()==None:
            return 0,None
        if board.outcome()==board.turn:
            return -1000,None
        else:
            return 1000,None
    if depth==0:
        return shallow_eval(board)
    move_list=prioritize(board)
    tuple=(-10000000000000,None)
    for move in move_list:
        board.push(move)
        eval=-negamax(board, depth-1, -beta, -alpha)[0]
        alpha=max(eval, alpha)
        if (eval>tuple[0]):
            tuple=(eval,move)
        if alpha>=beta:
            board.pop()
            break
        board.pop()
    return tuple