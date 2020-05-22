from graphics import Graphics
from datetime import datetime
import math, random
import util
import numpy

class Game:

    def __init__( self, size, num_pairs, valves=[]):
        self.start_time = datetime.now()
        self.size = size
        self.num_pairs = len(valves) if valves else num_pairs
        self.valves = valves or self.randomise_valves()
        self.game_state = GameState(self)
        self.graphics = Graphics(self)
        print(util.get_duration(self.start_time,'game initiated'))

    def randomise_valves(self):
        valves = []
        for i in range(self.num_pairs):
            for j in range(2):
                x = math.floor(random.uniform(0,self.size[0]))
                y = math.floor(random.uniform(0,self.size[1]))
                # prevent duplication or adjacency to similar color:
                while (x,y) in [valve[1] for valve in valves] or (j==1 and util.checkAdjacency((x,y),(valves[-1][1][0],valves[-1][1][1]))):
                    x = math.floor(random.uniform(0,self.size[0]))
                    y = math.floor(random.uniform(0,self.size[1]))
                valves.append([i,(x,y)])
        return valves

    def draw(self):
        self.graphics.init_frame()

class Cell:
    def __init__( self):
        self.isValve = False
        self.value = -1
    
    def __repr__(self):
        if self.isValve: return 'V'+str(self.value)
        else: return str(self.value)
    
class GameState:

    def __init__( self, game):
        self.game = game
        self.board_occupancy = numpy.empty(shape=[game.size[0],game.size[1]], dtype = Cell)
        # have to do this loop to ensure each instance is separate cell
        for x in range(len(self.board_occupancy)):
            for y in range(len(self.board_occupancy[x])):
                self.board_occupancy[x][y] = Cell()
        for valve in game.valves:
            self.board_occupancy[valve[1][0]][valve[1][1]].isValve = True
            self.board_occupancy[valve[1][0]][valve[1][1]].value = valve[0]

    def print(self):
        print(self.board_occupancy)

    def update(self,position_tuple,value):
        self.board_occupancy[position_tuple[0]][position_tuple[1]] = value
        # self.game.graphics.create_circle_in_grid_pos(x=position_tuple[0], y=position_tuple[1], color=self.game.graphics.colors[value], diameter_percent = 0.3)



class Agent:

    def __init__( self, game):
        self.game = game
        self.start_state = game.valves[0][1] if game.valves else None

    def update_state(self):
        self.game.game_state.update((1,1),0)

        
    # def graphSearch(problem,function,**kwargs):
    #     priority_queue = PriorityQueue()
    #     start_state = problem.getStartState()
    #     priority_queue.push((start_state,[],0),0)
    #     visited = [start_state]   # need to use list for Python as can't have nested sets. Ok as anyway checking if exists before inserting
    #     heuristic = kwargs.get('heuristic', None)

    #     while not priority_queue.isEmpty():
    #         state, path, total_cost = priority_queue.pop()
    #         if problem.isGoalState(state):
    #             return path
    #         for successor in problem.getSuccessors(state):
    #             new_state, direction, cost = successor
    #             if new_state not in visited:
    #                 cost = function(total_cost,cost)
    #                 heuristic_value = heuristic(new_state,problem=problem) if heuristic else 0
    #                 priority_queue.push((new_state,path+[direction],cost),cost + heuristic_value)
    #                 visited.append(new_state)

game = Game((5,5),4, util.sample_valves())
game.game_state.print()
game.draw()
# agent = Agent(game)
# agent.update_state()