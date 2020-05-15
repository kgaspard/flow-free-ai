from graphics import Graphics
import math, random
import numpy

class Game:

    def __init__( self, size, num_pairs):
        self.size = size
        self.num_pairs = num_pairs
        self.valves = self.randomise_valves()
        self.game_state = GameState(self)

    def randomise_valves(self):
        valves = []
        for i in range(self.num_pairs):
            for j in range(2):
                x = math.floor(random.uniform(0,self.size[0]))
                y = math.floor(random.uniform(0,self.size[1]))
                while (x,y) in [valve[1] for valve in valves]:
                    x = math.floor(random.uniform(0,self.size[0]))
                    y = math.floor(random.uniform(0,self.size[1]))
                valves.append([i,(x,y)])
        return valves

    def draw(self):
        graphics = Graphics(self)
        graphics.init_frame()

class GameState:

    def __init__( self, game):
        self.game = game
        self.board_occupancy = numpy.full((game.size[0],game.size[1]),-1)
        self.valve_map = numpy.full((game.size[0],game.size[1]),-1)
        for valve in game.valves:
            self.board_occupancy[valve[1][0]][valve[1][1]] = valve[0]
            self.valve_map[valve[1][0]][valve[1][1]] = valve[0]

    def print(self):
        print(self.valve_map)

    def update(self,x,y,value):
        self.board_occupancy[x][y] = value

game = Game((10,5),6)
game.draw()