import chess
import chess.pgn
import heuristic
import search
import math
board=chess.Board()
file=chess.pgn.Game()


"""TODO:
1)implement other functions in evaluation module. See how well that improves the accuracy.
2) Implement tablebase consulting?
3) neural_nets for better linear comb of evaluation function
"""

def play_human(board):
    while not board.is_game_over() and not board.can_claim_draw():
        string_input=input("what is your move?")
        player_move=chess.Move.from_uci(string_input)
        while not board.is_legal(player_move):
            string_input=input("That is not a legal move. What is your move?")
            player_move=chess.Move.from_uci(string_input)
        board.push(player_move)
        computer_move=search.negamax(board,3,-10000, 10000)[1]
        board.push(computer_move)
        print("The engine plays" +computer_move.uci())
    print("the game is over")

def play_self(board):
    base_depth=3
    node=set_up(board,base_depth)
    while not board.is_game_over() and not board.can_claim_draw():
        depth=base_depth+added_depth(board)
        tuple=search.negamax(board,depth, -10000, 10000)
        computer_move=tuple[1]
        board.push(computer_move)
        node=node.add_variation(computer_move)
        print("The engine plays" +computer_move.uci())
        if board.turn:
            print("it evaluates the position as " + str(tuple[0]))
        else:
            print("it evaluates the position as " + str(-tuple[0]))
        print("Here is the pgn so far:")
        print(file)
    print("the game is over")
    print("Here is the pgn:")
    #print(file)

def set_up(board,depth):
    first_move=search.negamax(board,depth,-10000,10000)[1]
    board.push(first_move)
    print("The engine plays" +first_move.uci())
    node=file.add_variation(first_move)
    return node


"""searches to higher nad higher depths depending on how much material is on the board,
and therefore how complex the search tree would roughly be"""
def added_depth(board):
    return math.floor(1/(heuristic.materialAndStage(board,board.turn, not board.turn)[1]))

play_self(board)
