from game import Game
import time
import util
from util import Search

class AgentState:
    def __init__(self,pos = (0,0), value = -1):
        self.pos = pos
        self.value = value
    
    def __repr__(self):
        return str(self.pos)
        # return '['+str(self.pos)+','+str(self.value)+']'

    def __eq__(self,other):
        return self.pos == other.pos and self.value == other.value

    def manhattanDistance(self,other):
        return abs(self.pos[0] - other.pos[0]) + abs(self.pos[1] - other.pos[1])

class Agent:

    def __init__( self, game):
        self.game = game
        self.start_state = game.valves[0][1] if game.valves else None

    def update_game_state(self,pos,value):
        self.game.game_state.update(pos,value)
    
    def get_valid_neighbouring_agent_states(self,agent_state):
        valid_neighbouring_agent_states = []
        x,y = agent_state.pos
        if y > 0 and (self.game.game_state.board_occupancy[x][y-1].value <= -1 or (self.game.game_state.board_occupancy[x][y-1].isValve and self.game.game_state.board_occupancy[x][y-1].value == agent_state.value)):
            valid_neighbouring_agent_states.append(AgentState(pos=(x,y-1),value=agent_state.value)) # North
        if y < self.game.size[1] - 1 and (self.game.game_state.board_occupancy[x][y+1].value <= -1 or (self.game.game_state.board_occupancy[x][y+1].isValve and self.game.game_state.board_occupancy[x][y+1].value == agent_state.value)):
            valid_neighbouring_agent_states.append(AgentState(pos=(x,y+1),value=agent_state.value)) # South
        if x > 0 and (self.game.game_state.board_occupancy[x-1][y].value <= -1 or (self.game.game_state.board_occupancy[x-1][y].isValve and self.game.game_state.board_occupancy[x-1][y].value == agent_state.value)):
            valid_neighbouring_agent_states.append(AgentState(pos=(x-1,y),value=agent_state.value)) # West
        if x < self.game.size[0] - 1 and (self.game.game_state.board_occupancy[x+1][y].value <= -1 or (self.game.game_state.board_occupancy[x+1][y].isValve and self.game.game_state.board_occupancy[x+1][y].value == agent_state.value)):
            valid_neighbouring_agent_states.append(AgentState(pos=(x+1,y),value=agent_state.value)) # East
        return valid_neighbouring_agent_states

    def pos_path_to_state_path(self,pos_path,value):
        state_path = []
        for pos in pos_path:
            state_path.append(AgentState(pos,value))
        return state_path

    def get_next_states_from_path(self,path):
        if not path: return None
        current_state = path[-1]
        next_states = self.get_valid_neighbouring_agent_states(current_state)
        if len(path) < 2: return next_states
        next_states.remove(path[-2]) # don't allow direct backtracking. We take care of this anyway in the search algorithm
        new_next_states = []
        for next_state in next_states:
            direction_vector = util.tupleAdd(next_state.pos,util.tupleScale(current_state.pos,-1))
            forward_tracked_positions = [util.tupleAdd(next_state.pos,direction_vector), util.tupleAdd(next_state.pos,util.tupleSwap(direction_vector)), util.tupleAdd(next_state.pos,util.tupleScale(util.tupleSwap(direction_vector),-1))]
            forward_tracked_states = [AgentState(pos=pos,value=current_state.value) for pos in forward_tracked_positions]
            add_state = True
            for forward_tracked_state in forward_tracked_states:
                if forward_tracked_state in path:
                    add_state = False
                    break
            if add_state: new_next_states.append(next_state)
        return new_next_states

    def solve_for_value(self,value,all_solutions=False, priority_queue=None):
        valves = [valve for valve in self.game.valves if valve[0]==value]
        start_state = AgentState(pos=valves[0][1],value=valves[0][0])
        goal_state = AgentState(pos=valves[1][1],value=valves[1][0])
        search = Search()
        paths,new_priority_queue = search.aStarSearch(start_state=start_state,goal_state=goal_state,next_states_function=self.get_next_states_from_path,all_solutions=all_solutions, priority_queue=priority_queue, return_priority_queue=True)
        if paths:
            for state in paths[0]:
                self.update_game_state(pos=state.pos,value = state.value)
        return paths,new_priority_queue

    def solve_recursively(self,value=0,priority_queue=None):
        solutions,priority_queue = self.solve_for_value(value=value, priority_queue=priority_queue)
        if not solutions: return solutions
        for state in solutions[0]:
            self.update_game_state(pos=state.pos,value = state.value)
        if value == self.game.num_pairs - 1:
            return solutions[0]
        else:
            next_solution = self.solve_recursively(value=value+1,priority_queue=None)
            if not next_solution:
                for state in solutions[0]:
                    self.update_game_state(pos=state.pos,value = -1)
                if priority_queue.items():
                    return self.solve_recursively(value=value,priority_queue=priority_queue)
                else:
                    return []
            else:
                return next_solution