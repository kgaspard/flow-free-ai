from game import Game,GameState
import numpy as np
import os

def parse_board_size(board_size_string):
    board_size = board_size_string
    board_size = [int(elem) for elem in board_size]
    x=board_size[0]
    y= board_size[1] if len(board_size)>1 else board_size[0]
    board_size = (x,y)
    return board_size

#### Parse level:

def init_game_from_level(level):
    problem,solution = level.split('=')
    problem_array = problem.split(';')
    
    board_size_string = problem_array.pop(0)
    board_size = parse_board_size(board_size_string)
    
    num_valve_pairs = int(len(problem_array)/2)

    valve_index=0
    valves=[]
    for index,elem in enumerate(problem_array):
        pos_array = elem.split(':')
        pos = (int(pos_array[0])-1,int(pos_array[1])-1)
        valves.append([valve_index,pos])
        if index % 2 == 1: valve_index += 1
    
    return Game(board_size,num_valve_pairs,valves)

def problem_to_array(problem, max_board_size=25):
    problem_array = problem.split(';')
    board_size_string = problem_array.pop(0)
    board = np.full((max_board_size, max_board_size), -1)

    valve_index=0
    for index,elem in enumerate(problem_array):
        pos_array = elem.split(':')
        x,y = (int(pos_array[0])-1,int(pos_array[1])-1)
        board[x][y] = valve_index
        if index % 2 == 1: valve_index += 1
    return board.flatten()

def level_array_to_game(array):
    max_board_size = int(np.sqrt(len(array)))
    valves=[]
    board_size = [0,0]
    num_valve_pairs = 0
    for index,elem in enumerate(array):
        if elem <= -1: continue
        pos = np.divmod(index,max_board_size)
        if pos[0] > board_size[0]: board_size[0] = pos[0]
        if pos[1] > board_size[1]: board_size[1] = pos[1]
        valves.append([elem,pos])
    (board_size_x,board_size_y) = (board_size[0]+1,board_size[1]+1)
    valves.sort(key=lambda x: int(x[0]))
    num_valve_pairs = int(len(valves)/2)
    return Game((board_size_x,board_size_y), num_valve_pairs, valves)

#### Parse solution:

def game_solution_from_level(level):
    game = init_game_from_level(level)
    state = GameState(game=game)
    problem,solution = level.split('=')
    solution_array = [elem.split(';') for elem in solution.split('|')]
    
    for path_index,path in enumerate(solution_array):
        for elem in path:
            pos_array = elem.split(':')
            pos = (int(pos_array[0])-1,int(pos_array[1])-1)
            state.update(pos,path_index)

    return state.update_and_copy()

def solution_to_array(solution, max_board_size=25):
    solution_array = [elem.split(';') for elem in solution.split('|')]
    board = np.full((max_board_size, max_board_size), -1)
    
    for path_index,path in enumerate(solution_array):
        for elem in path:
            pos_array = elem.split(':')
            x,y = (int(pos_array[0])-1,int(pos_array[1])-1)
            board[x][y] = path_index

    return board.flatten()

##### Parse files

def parse_files(max_board_size=15):
    files = os.listdir('./data')
    problems = []
    solutions = []
    for f in files:
        levels = open("./data/"+f, "r").read().splitlines()
        for level in levels:
            problem,solution = level.split('=')
            problems.append(problem_to_array(problem, max_board_size=max_board_size))
            solutions.append(solution_to_array(solution, max_board_size=max_board_size))
    return problems,solutions