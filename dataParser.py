from game import Game,GameState

f = open("./data/five.txt", "r")
levels = f.read().splitlines()

def init_game_from_level(level):
    problem,solution = level.split('=')
    problem_array = problem.split(';')
    
    board_size = problem_array.pop(0)
    board_size = [int(elem) for elem in board_size]
    x=board_size[0]
    y= board_size[1] if len(board_size)>1 else board_size[0]
    board_size = (x,y)
    
    num_valve_pairs = int(len(problem_array)/2)

    valve_index=0
    valves=[]
    for index,elem in enumerate(problem_array):
        pos_array = elem.split(':')
        pos = (int(pos_array[0])-1,int(pos_array[1])-1)
        valves.append([valve_index,pos])
        if index % 2 == 1: valve_index += 1
    
    return Game(board_size,num_valve_pairs,valves)

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