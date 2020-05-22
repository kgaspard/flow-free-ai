from graphics import Graphics
from datetime import datetime
import math, random
import util
import numpy as np

class Game:

    def __init__( self, size, num_pairs, valves=[]):
        self.start_time = datetime.now()
        self.size = size
        self.num_pairs = int(len(valves)/2) if valves else num_pairs
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
    def __init__(self, value = -1, isValve = False):
        self.value = value
        self.isValve = isValve
    
    def __repr__(self):
        if self.isValve: return 'V'+str(self.value)
        else: return str(self.value)
    
class GameState:

    def __init__( self, game):
        self.game = game
        self.board_occupancy = np.empty(shape=[game.size[0],game.size[1]], dtype = Cell)
        # have to do this loop to ensure each instance is separate cell
        for position in self.list_positions():
            self.board_occupancy[position[0]][position[1]] = Cell()
        for valve in game.valves:
            self.board_occupancy[valve[1][0]][valve[1][1]].isValve = True
            self.board_occupancy[valve[1][0]][valve[1][1]].value = valve[0]

    def print(self):
        print(self.board_occupancy)

    def list_positions(self):
        states = []
        for x in range(self.game.size[0]):
            for y in range(self.game.size[1]):
                states.append((x,y))
        return states

    def update(self,position_tuple,value):
        if not self.board_occupancy[position_tuple[0]][position_tuple[1]].isValve: self.board_occupancy[position_tuple[0]][position_tuple[1]].value = value