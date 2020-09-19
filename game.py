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
        self.graphics.draw_game()

    def draw_from_2d_array(self,start_index,problem_array,solution_array):
        self.graphics.draw_game_from_2d_array(start_index,problem_array,solution_array)

class Cell:
    def __init__(self, value = -1, isValve = False, isStartValve=False):
        self.value = value
        self.isValve = isValve
        self.isStartValve = isStartValve
    
    def __repr__(self):
        if self.isValve: return 'V'+str(self.value)
        else: return str(self.value)
    
    def __eq__(self,other):
        return self.value == other.value and self.isValve == other.isValve
    
class GameState:

    def __init__(self, game, board_occupancy=None, paths=None, active_path = 0):
        self.game = game
        
        if board_occupancy is None:
            self.board_occupancy = np.empty(shape=[game.size[0],game.size[1]], dtype = Cell)
            for position in self.list_positions():
                self.board_occupancy[position[0]][position[1]] = Cell()
            # set up valves:
            for valve in game.valves:
                self.board_occupancy[valve[1][0]][valve[1][1]].isValve = True
                self.board_occupancy[valve[1][0]][valve[1][1]].value = valve[0]
            for i in range(game.num_pairs):
                valve = game.valves[i*2]
                self.board_occupancy[valve[1][0]][valve[1][1]].isStartValve = True
        else:
            self.board_occupancy = board_occupancy
        
        if paths is None:
            self.paths = []
            for i in range(game.num_pairs):
                valve = game.valves[i*2]
                self.paths.append([valve[1]])
        else: self.paths = paths
        
        self.active_path = active_path

    def list_positions(self):
        states = []
        for x in range(self.game.size[0]):
            for y in range(self.game.size[1]):
                states.append((x,y))
        return states

    def get_position_value(self,pos):
        if pos[0] >= 0 and pos[0] < self.game.size[0] and pos[1] >= 0 and pos[1] < self.game.size[1]:
            return self.board_occupancy[pos[0]][pos[1]].value
        else: return None

    def update(self,position_tuple,value):
        pos_value = self.board_occupancy[position_tuple[0]][position_tuple[1]].value
        if not self.board_occupancy[position_tuple[0]][position_tuple[1]].isValve:
            self.board_occupancy[position_tuple[0]][position_tuple[1]].value = value
        if not self.board_occupancy[position_tuple[0]][position_tuple[1]].isStartValve:
            if value==-1 and position_tuple in self.paths[pos_value]:
                self.paths[pos_value].remove(position_tuple)
            elif value >= 0 and position_tuple != self.paths[value][-1] and util.checkAdjacency(position_tuple,self.paths[value][-1]): 
                self.paths[value].append(position_tuple)

    def update_and_copy(self, position_tuple=None,value=None, active_path = 0):
        board_occupancy = np.empty(shape=[self.game.size[0],self.game.size[1]], dtype = Cell)
        for x in range(self.game.size[0]):
            for y in range(self.game.size[1]):
                board_occupancy[x][y] = Cell(value=self.board_occupancy[x][y].value, isValve=self.board_occupancy[x][y].isValve, isStartValve=self.board_occupancy[x][y].isStartValve)

        paths = []
        for path in self.paths:
            new_path = path.copy()
            paths.append(new_path)

        new_active_path = active_path if active_path else self.active_path 
        
        # update
        if position_tuple is not None and value is not None:
            pos_value = self.board_occupancy[position_tuple[0]][position_tuple[1]].value
            if not self.board_occupancy[position_tuple[0]][position_tuple[1]].isValve:
                board_occupancy[position_tuple[0]][position_tuple[1]].value = value
            if not self.board_occupancy[position_tuple[0]][position_tuple[1]].isStartValve:
                if value==-1 and position_tuple in self.paths[pos_value]:
                    paths[pos_value].remove(position_tuple)
                elif value >= 0 and position_tuple != self.paths[value][-1] and util.checkAdjacency(position_tuple,self.paths[value][-1]):
                    paths[value].append(position_tuple)
        # copy
        new_game_state = GameState(game=self.game,board_occupancy=board_occupancy,paths=paths,active_path=new_active_path)
        return new_game_state
    
    def check_value_complete(self, value):
        return self.paths[value][-1] == self.game.valves[value*2+1][1]
    
    def check_complete(self):
        complete = True
        for i in range(self.game.num_pairs):
            if not self.check_value_complete(i):
                complete = False
                break
        return complete

    def get_numeric_array(self,max_size=15):
        state_array = [-1]*max_size*max_size
        for i in range(max_size*max_size):
            y,x = divmod(i,max_size)
            if x<self.game.size[0] and y<self.game.size[1]: state_array[i] = self.board_occupancy[x][y].value
        return state_array

    def draw(self):
        self.game.graphics.draw_game_state(game_state=self)

    ### Class attributes:    
    def copy(self):
        new_game_state = GameState(self.game)
        for x in range(self.game.size[0]):
            for y in range(self.game.size[1]):
                new_game_state.board_occupancy[x][y] = Cell(value=self.board_occupancy[x][y].value, isValve=self.board_occupancy[x][y].isValve, isStartValve=self.board_occupancy[x][y].isStartValve)
        new_game_state.active_path = self.active_path
        new_game_state.paths = []
        for path in self.paths:
            new_path = path.copy()
            new_game_state.paths.append(new_path)
        return new_game_state
    
    def reset(self):
        self.__init__(self.game)
    
    def __eq__(self,other):
        comparison = self.board_occupancy == other.board_occupancy
        return comparison.all() and self.paths == other.paths

    def __hash__(self):
        return hash(hash(str(self.board_occupancy)) + 42*hash(str(self.paths))) + 37*hash(str(self.active_path))

    def __repr__(self):
        return self.board_occupancy.__repr__()

def generate_game(game_name):
    if game_name == 'tiny': return Game((2,4),2,[[0,(1,0)],[0,(0,3)],[1,(1,1)],[1,(1,3)]])
    if game_name == 'small': return Game((5,5),4,[[0,(3,0)],[0,(0,2)],[1,(4,0)],[1,(3,1)],[2,(2,1)],[2,(1,3)],[3,(0,3)],[3,(4,3)],[4,(3,3)],[4,(4,4)]])
    if game_name == 'medium': return Game((8,8),4,[[0,(2,0)],[0,(3,4)],[1,(3,0)],[1,(1,1)],[2,(2,1)],[2,(1,6)],[3,(2,2)],[3,(5,5)]])
    if game_name == 'large': return Game((14,14),12,[[0,(5,1)],[0,(10,3)],[1,(3,3)],[1,(9,7)],[2,(3,5)],[2,(2,11)],[3,(5,5)],[3,(8,6)],[4,(10,5)],[4,(8,7)],[5,(1,6)],[5,(6,7)],[6,(5,6)],[6,(3,11)],[7,(6,8)],[7,(11,13)],[8,(9,9)],[8,(5,11)],[9,(1,10)],[9,(7,10)],[10,(12,13)],[10,(13,12)],[11,(12,6)],[11,(6,13)]])