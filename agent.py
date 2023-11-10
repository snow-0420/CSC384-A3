"""
An AI player for Othello.
"""

import random
import sys
import time
import math

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

state_caching = {}

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)

# Method to compute utility value of terminal state
def compute_utility(board, color):
    p1_count, p2_count = get_score(board)
    if color == 1:
        return p1_count - p2_count
    else:
        return p2_count - p1_count

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    return 0 #change this!

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    if limit == 0:
        result = (None, compute_utility(board, color))
        return result
    if caching == 1:
        if board in state_caching:
            return state_caching[board]
    move_lst = get_possible_moves(board, 3-color)
    if not move_lst: # move_lst is empty (i.e. no possible move can be made)
        result = (None, compute_utility(board, color))
        return result
    min_value = math.inf
    min_move = None
    for move in move_lst:
        new_board = play_move(board, 3-color, move[0], move[1])
        result = minimax_max_node(new_board, color, limit-1, caching)
        if result[1] < min_value:
            min_value = result[1]
            min_move = move
        if caching == 1:
            state_caching[board] = result
    return (min_move, min_value)

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    if limit == 0:
        result = (None, compute_utility(board, color))
        return result
    if caching == 1:
        if board in state_caching:
            return state_caching[board]
    move_lst = get_possible_moves(board, color)
    if not move_lst: # move_lst is empty (i.e. no possible move can be made)
        result = (None, compute_utility(board, color))
        return result
    max_value = -math.inf
    max_move = None
    for move in move_lst:
        new_board = play_move(board, color, move[0], move[1])
        result = minimax_min_node(new_board, color, limit-1, caching)
        if result[1] > max_value:
            max_value = result[1]
            max_move = move
        if caching == 1:
            state_caching[board] = result
    return (max_move, max_value)

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    """
    return minimax_max_node(board, color, limit, caching)[0]


############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    if limit == 0:
        result = (None, compute_utility(board, color))
        return result
    if caching == 1:
        if board in state_caching:
            return state_caching[board]
    move_lst = get_possible_moves(board, 3-color)
    if not move_lst: # move_lst is empty (i.e. no possible move can be made)
        result = (None, compute_utility(board, color))
        return result
    min_value = math.inf
    min_move = None
    a = alpha
    b = beta
    if ordering == 1:
        util_lst = []
        util_dict = {}
        for move in move_lst:
            new_board = play_move(board, 3-color, move[0], move[1])
            util = compute_utility(new_board, color)
            if util not in util_lst:
                util_lst.append(util)
            if util not in util_dict:
                util_dict[util] = [move]
            else:
                util_dict[util].append(move)
        util_lst.sort(reverse=True)
        move_lst = []
        for utility in util_lst:
            move_lst.extend(util_dict[utility])
    for move in move_lst:
        new_board = play_move(board, 3-color, move[0], move[1])
        result = alphabeta_max_node(new_board, color, a, b, limit-1, caching, ordering)
        if result[1] < b:
            b = result[1]
        if b <= a:
            min_value = -math.inf
            break
        if result[1] < min_value:
            min_value = result[1]
            min_move = move
        if caching == 1:
            state_caching[board] = result
    return (min_move, min_value)

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    if limit == 0:
        result = (None, compute_utility(board, color))
        return result
    if caching == 1:
        if board in state_caching:
            return state_caching[board]
    move_lst = get_possible_moves(board, color)
    if not move_lst: # move_lst is empty (i.e. no possible move can be made)
        result = (None, compute_utility(board, color))
        return result
    max_value = -math.inf
    max_move = None
    a = alpha
    b = beta
    if ordering == 1:
        util_lst = []
        util_dict = {}
        for move in move_lst:
            new_board = play_move(board, color, move[0], move[1])
            util = compute_utility(new_board, color)
            if util not in util_lst:
                util_lst.append(util)
            if util not in util_dict:
                util_dict[util] = [move]
            else:
                util_dict[util].append(move)
        util_lst.sort(reverse=True)
        move_lst = []
        for utility in util_lst:
            move_lst.extend(util_dict[utility])
    for move in move_lst:
        new_board = play_move(board, color, move[0], move[1])
        result = alphabeta_min_node(new_board, color, a, b, limit-1, caching, ordering)
        if result[1] > a:
            a = result[1]
        if a >= b:
            max_value = math.inf
            break
        if result[1] > max_value:
            max_value = result[1]
            max_move = move
        if caching == 1:
            state_caching[board] = result
    return (max_move, max_value)

def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations.
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations.
    """
    return alphabeta_max_node(board, color, -math.inf, math.inf, limit, caching, ordering)[0]

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light.
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)

            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
