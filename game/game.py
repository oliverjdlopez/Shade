import chess
import chess.pgn
import heuristic
import search
import math



"""TODO:
1)implement other functions in evaluation module. See how well that improves the accuracy.
2)sac bug
2) Do performance tests using perft. See where I can clean up efficiency
3)impleemnt better pruning so engine can go deeper. Good things to explore on chess wiki and similar sites
4) Implement tablebase consulting?
5) neural_nets for better linear comb of evaluation function
"""

def play_human(board):
    while not board.is_game_over() and not board.can_claim_draw():
        string_input=input("what is your move?")
        player_move=chess.Move.from_uci(string_input)
        while not board.is_legal(player_move):
            string_input=input("That is not a legal move. What is your move?")
            player_move=chess.Move.from_uci(string_input)
        board.push(player_move)
        computer_move=search.negamax(board,  3, board.turn,-10000, 10000, [])[1]
        board.push(computer_move)
        print("The engine plays" +computer_move.uci())
    print("the game is over")


"""searches to higher nad higher depths depending on how much material is on the board,
and therefore how complex the search tree would roughly be"""
def added_depth(board):
    return math.floor(2/(heuristic.materialAndStage(board,board.turn, not board.turn)[1]))

def play_self(board):
    base_depth=4
    node=set_up(board,base_depth)
    while not board.is_game_over() and not board.can_claim_draw():
        depth=base_depth +added_depth(board)
        depth=base_depth
        tuple=search.negamax(board, depth, -1000, 1000, [])
        computer_move=tuple[1] 
        node=node.add_variation(computer_move)
        print("The engine plays" +computer_move.uci())
        if board.turn:
            print("it evaluates the position as " + str(tuple[0]))
        else:
            print("it evaluates the position as " + str(-tuple[0]))
        print("It thinks that the best line is :" + str(tuple[2]))
        board.push(computer_move)
        print("Here is the pgn so far:")
        print(file)
    print("the game is over")
    print("Here is the pgn:")
    #print(file)

def set_up(board,depth):
    first_move=search.negamax(board, depth, -10000,10000, [])[1]
    board.push(first_move)
    print("The engine plays" + first_move.uci())
    node=file.add_variation(first_move)
    return node



board=chess.Board()
file=chess.pgn.Game()
play_self(board)
