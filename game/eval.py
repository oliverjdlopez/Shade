import chess


def negamax(board,depth,alpha, beta):
    if board.is_game_over() or board.can_claim_draw():
        if board.outcome()==None:
            return 0,None
        if board.outcome()==board.turn:
            return -1000,None
        else:
            return 1000,None
    if depth==0:
        tuple=shallow_eval(board)
        return tuple[0],tuple[1]
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



"""Evaluation function for a given position based purely off computer's 'intuition'.
Evaluation is from the perspective of the player with the turn.
 Returns a tuple of (evaluation, None)."""
def shallow_eval(board):
    has_move=board.turn
    next_move= not has_move
    tuple=materialAndStage(board,has_move,next_move)
    material=tuple[0]-hanging_material(board,has_move,next_move)
    stage=1-tuple[1]
    mobility=mobility_eval(board, has_move, next_move)
    territory=territory_eval(board, has_move, next_move)
    structure=structure_eval(board,has_move, next_move)
    move_advantage=.2 #maybe this can become a function
    #hanging=hanging_material(board, has_move, next_move)
    return (material+(0.1*mobility)+(0.2*territory)+move_advantage+stage*structure, None)

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

"""returns the material difference between the player with the move and the player without the move.
In order to properly optimize, also returns the game stage based on the amount of
material on the board. A stage value of 1 means that all material is on the Board,
0 means all is off (roughly). returns a tuple of (material_diff, game_stage)"""
def materialAndStage(board,has_move, next_move):
    mover_material=0
    other_material=0
    total_material=0
    for rook in board.pieces(chess.ROOK,has_move):
        mover_material+=5
    for pawn in board.pieces(chess.PAWN, has_move):
        mover_material+=1
    for bishop in board.pieces(chess.BISHOP,has_move):
        mover_material+=3
    for knight in board.pieces(chess.KNIGHT,has_move):
        mover_material+=3
    for queen in board.pieces(chess.QUEEN, has_move):
        mover_material+=9
    for rook in board.pieces(chess.ROOK,next_move):
        other_material+=5
    for pawn in board.pieces(chess.PAWN, next_move):
        other_material+=1
    for bishop in board.pieces(chess.BISHOP,next_move):
        other_material+=3
    for knight in board.pieces(chess.KNIGHT,next_move):
        other_material+=3
    for queen in board.pieces(chess.QUEEN, next_move):
        other_material+=9
    total_material=mover_material+other_material

    return mover_material-other_material, adjusted_sigmoid(total_material)


"""returns the difference in legal moves."""
def mobility_eval(board, has_move, next_move):
    has_moves=board.legal_moves.count()
    board.push(chess.Move.from_uci("0000"))
    next_moves=board.legal_moves.count()
    board.pop()
    return has_moves-next_moves

def territory_eval(board, has_move, next_move):
    mover_territory=0
    next_territory=0
    white_territory=0
    black_territory=0
    if board.turn:
        for move in board.legal_moves:
            if move.to_square > 31:
                white_territory+=1
        board.push(chess.Move.from_uci("0000"))
        for move in board.legal_moves:
            if move.to_square < 32:
                black_territory+=1
    else:
        for move in board.legal_moves:
            if move.to_square < 32:
                black_territory+=1
        board.push(chess.Move.from_uci("0000"))
        for move in board.legal_moves:
            if move.to_square > 31:
                white_territory+=1
    board.pop()
    if has_move:
        mover_territory=white_territory
        next_territory=black_territory
    else:
        mover_territory=black_territory
        next_territory=white_territory
    return mover_territory-next_territory

def hanging_material(board, has_move, next_move):
    hanging=0
    return hanging

"""takes in real number, returns a modified sigmoid function to work on the range of
0 to 78"""
def adjusted_sigmoid(num):
    return 1/(1+2.71828182845**(-(num-20)/10))

def structure_eval(board,has_move, next_move):
    mover_structure=0
    next_structure=0
    files=[]
    squares=board.pieces(chess.PAWN, has_move)
    doubled=0
    for s in squares:
        mover_structure+=1
        if s in files:
            doubled +=1
        else:
            files.append(chess.square_file(s))
    mover_structure=mover_structure-(0.5)*doubled
    doubled=0
    squares=board.pieces(chess.PAWN, has_move)
    for s in squares:
        next_structure+=1
        if s in files:
            doubled +=1
        else:
            files.append(chess.square_file(s))
    next_structure=next_structure-(0.5)*doubled
    return mover_structure-next_structure

def king_safety(board, has_move, next_move):
    return 0


"""Recursive evaluation function for a given position, recursed depth number of times.
Returns tuple of evaluation with best play and best move. HAS BEEN REPLACED BY NEGAMAX """
def rec_eval(board, depth):
    """First evaluate if game is drawn, or if one color has won"""
    if board.is_game_over() or board.can_claim_draw():
        if board.outcome()==None:
            return 0,None
        if board.outcome():
            return 1000,None
        if not board.outcome():
            return -1000,None
    if depth==0:
        return shallow_eval(board)
    move_list=prune(board)
    tuple=(None,None)
    if board.turn:
        for move in move_list:
            if tuple==(None,None):
                board.push(move)
                tuple=(rec_eval(board,depth-1)[0],move)
                board.pop()
            else:
                """if white to move, returns best play for white"""
                """print("baord.turn accessed")"""
                board.push(move)
                eval=rec_eval(board, depth-1)[0]
                board.pop()
                if eval > tuple[0]:
                    tuple=(eval,move)

            """if black to move, return best play for black"""
    if not board.turn:
        for move in move_list:
            if tuple==(None,None):
                board.push(move)
                tuple=(rec_eval(board,depth-1)[0],move)
                board.pop()
            else:
                """if white to move, returns best play for white"""
                """print("baord.turn accessed")"""
                board.push(move)
                eval=rec_eval(board, depth-1)[0]
                board.pop()
                if eval<tuple[0]:
                    tuple=(eval,move)
    return tuple