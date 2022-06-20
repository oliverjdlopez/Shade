import chess
import heuristic
import time

def generate_nodes(board, depth): 
  move_list=board.legal_moves
  nodes=0
  for move in move_list:
    if depth==0:
      board.push(move)
      board.pop()
      nodes+=1
    else: 
      board.push(move)
      nodes+=generate_nodes(board, depth-1)
      board.pop()
  return nodes

def generate_nodes_with_heur(board,depth): 
  move_list=board.legal_moves
  nodes=0
  for move in move_list:
    if depth==0:
      board.push(move)
      heuristic.shallow_eval(board)
      board.pop(move)
      nodes+=1
    else: 
      board.push(move)
      nodes+=generate_nodes(board, depth-1)
      board.pop()
  return nodes
    




def speed_test(): 
  user_input=input("With or without heuristic?")
  if user_input == "without":
    test_board= chess.Board()
    start=time.time()
    total_nodes=generate_nodes(test_board, 4)
    end=time.time()
    total_time=end-start
    print("NPS w/o heuristic: " + str(total_nodes/total_time))
    print("Nodes analyzed: " + str(total_nodes))
    print("Total time spent: " + str(total_time))
  if user_input == "with":
    test_board= chess.Board()
    start=time.time()
    total_nodes=generate_nodes_with_heur(test_board, 4)
    end=time.time()
    total_time=end-start
    print("NPS w/ heuristic: " + str(total_nodes/total_time))
    print("Nodes analyzed: " + str(total_nodes))
    print("Total time spent: " + str(total_time))
  else: print("That's not a valid input. run the program again and respond with either with or without ")



from io import StringIO
import csv
import chess.pgn

def position_test(): 
  pgn=open('data/test_position')
  game=chess.pgn.read_game(pgn)
  board=game.board()
  #put moves from pgn on board
  for move in game.mainline_moves(): 
    board.push(move)
  line=input("Separated my commas, enter the moves that you want to add to the test_position")
  line=line.replace(" ", "")
  file=StringIO(line)
  reader=csv.reader(file, delimiter=',')
  for row in reader: 
    for move in row: 
      board.push(chess.Move.from_uci(move))
  print(board)
  heuristic.test_eval(board)




user_input=input("Do you want to test speed or a position?")
if user_input== "speed":
  speed_test()
elif user_input=="position":
  position_test()
else: print("That's not a valid input. run the program again and respond with either speed or position")
