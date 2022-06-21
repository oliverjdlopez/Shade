import chess
import math


"""Evaluation function for a given position based purely off computer's 'intuition'.
Evaluation is from the perspective of the player with the turn.
It is the same type as the search function, but because it is a shallow eval, does not know what the best move is. Therefore,
returns a tuple of (evaluation, None)."""
def shallow_eval(board):
    has_move=board.turn
    next_move= not has_move
    #if terminal node
    if board.is_game_over() or board.can_claim_draw():
        if board.outcome()==None:
            return 0
        if board.outcome()==has_move:
            return 1000
        else:
            return -1000
    tuple=materialAndStage(board,has_move,next_move)
    material=tuple[0]
    stage=1-tuple[1] #heuristic for what stage the game is. Higher values of stage represent a later game point
    mobility=mobility_eval(board, has_move, next_move)
    territory=territory_eval(board, has_move, next_move)
    structure=structure_eval(board,has_move, next_move)
    move_advantage=.2 #maybe this can become a function
    #hanging=hanging_material(board, has_move, next_move)
    return material+(0.01*mobility)+(0.05*territory)+move_advantage+(stage*structure)



"""takes in real number, returns a modified sigmoid function to work on the range of
0 to 78"""
def adjusted_sigmoid(num):
    return 1/(1+math.e**(-(num-20)/10))


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
    """This function is not implemented fully. It does not account for trade-order
    or anything that's forcing yet. Further, doesn't count a queen as hanging if, for example,
    it is defended by a pawn but can be taken by a bishop. Also it's really slow but not sure if there is a better way to go about that"""
    material= 0
    is_hanging=0
    for rook in board.pieces(chess.ROOK,has_move):
        is_hanging = 1 if len(board.attackers(has_move, rook))<len(board.attackers(next_move,rook)) else 0
        material+=5*is_hanging
    for pawn in board.pieces(chess.PAWN, has_move):
        is_hanging = 1 if len(board.attackers(has_move, pawn))<len(board.attackers(next_move,pawn)) else 0
        material+=1*is_hanging
    for bishop in board.pieces(chess.BISHOP,has_move):
        is_hanging = 1 if len(board.attackers(has_move, bishop))<len(board.attackers(next_move,bishop)) else 0
        material+=3*is_hanging
    for knight in board.pieces(chess.KNIGHT,has_move):
        is_hanging = 1 if len(board.attackers(has_move, knight))<len(board.attackers(next_move,knight)) else 0
        material+=3*is_hanging
    for queen in board.pieces(chess.QUEEN, has_move):
        is_hanging = 1 if len(board.attackers(has_move, queen))<len(board.attackers(next_move,queen)) else 0
        material+=9*is_hanging
    return material




"""returns the difference between how many doubled pawns the mover has vs the oppponent"""
def structure_eval(board,has_move, next_move):
    mover_structure=0
    next_structure=0
    files=[]
    pawns=board.pieces(chess.PAWN, has_move)
    doubled=0
    for p in pawns:
        mover_structure+=1
        if p in files:
            doubled +=1
        else:
            files.append(chess.square_file(p))
    mover_structure=mover_structure-(0.5)*doubled
    doubled=0
    pawns=board.pieces(chess.PAWN, has_move)
    for p in pawns:
        next_structure+=1
        if p in files:
            doubled +=1
        else:
            files.append(chess.square_file(p))
    next_structure=next_structure-(0.5)*doubled
    return mover_structure-next_structure

def king_safety(board, has_move, next_move):
    return 0


def test_eval(board):
    has_move=board.turn
    next_move= not has_move
    tuple=materialAndStage(board,has_move,next_move)
    material=tuple[0]
    stage=1-tuple[1]
    mobility=mobility_eval(board, has_move, next_move)
    territory=territory_eval(board, has_move, next_move)
    structure=structure_eval(board,has_move, next_move)
    move_advantage=.2 #maybe this can become a function
    if board.turn:
        print("It is white to move")
    else:
        print("It is black to move")
    print("The material advantage is " + str(material))
    print("The mobility advantage is " + str(mobility))
    print("The territory advnatge is " + str(territory))
    print("The structure advantage is " + str(structure))
    print("The stage of the game is " + str(stage))
    print("The total evaluation of the position is " + str((material+(0.01*mobility)+(0.05*territory)+move_advantage+(stage*structure))))
    return (material+(0.01*mobility)+(0.05*territory)+move_advantage+(stage*structure), None)
