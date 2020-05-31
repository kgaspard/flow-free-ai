from game import Game,GameState
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

class Agent:

    # General:

    def __init__( self, game):
        self.game = game
        self.start_state = game.valves[0][1] if game.valves else None

    def update_game_state(self,pos,value):
        self.game.game_state.update(pos,value)
    
    def get_valid_neighbouring_agent_states(self,agent_state):
        valid_neighbouring_agent_states = []
        x,y = agent_state.pos
        if y > 0 and (self.game.game_state.board_occupancy[x][y-1].value <= -1 or (self.game.game_state.board_occupancy[x][y-1].isValve and self.game.game_state.board_occupancy[x][y-1].value == agent_state.value and not self.game.game_state.board_occupancy[x][y-1].isStartValve)):
            valid_neighbouring_agent_states.append(AgentState(pos=(x,y-1),value=agent_state.value)) # North
        if y < self.game.size[1] - 1 and (self.game.game_state.board_occupancy[x][y+1].value <= -1 or (self.game.game_state.board_occupancy[x][y+1].isValve and self.game.game_state.board_occupancy[x][y+1].value == agent_state.value and not self.game.game_state.board_occupancy[x][y+1].isStartValve)):
            valid_neighbouring_agent_states.append(AgentState(pos=(x,y+1),value=agent_state.value)) # South
        if x > 0 and (self.game.game_state.board_occupancy[x-1][y].value <= -1 or (self.game.game_state.board_occupancy[x-1][y].isValve and self.game.game_state.board_occupancy[x-1][y].value == agent_state.value and not self.game.game_state.board_occupancy[x-1][y].isStartValve)):
            valid_neighbouring_agent_states.append(AgentState(pos=(x-1,y),value=agent_state.value)) # West
        if x < self.game.size[0] - 1 and (self.game.game_state.board_occupancy[x+1][y].value <= -1 or (self.game.game_state.board_occupancy[x+1][y].isValve and self.game.game_state.board_occupancy[x+1][y].value == agent_state.value and not self.game.game_state.board_occupancy[x+1][y].isStartValve)):
            valid_neighbouring_agent_states.append(AgentState(pos=(x+1,y),value=agent_state.value)) # East
        return valid_neighbouring_agent_states
    
    # Agent State based:

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
        new_next_states = []
        for next_state in next_states:
            if next_state==path[-2]: continue
            direction_vector = util.tupleAdd(next_state.pos,util.tupleScale(current_state.pos,-1))
            forward_tracked_positions = [util.tupleAdd(next_state.pos,direction_vector), util.tupleAdd(next_state.pos,util.tupleSwap(direction_vector)), util.tupleAdd(next_state.pos,util.tupleScale(util.tupleSwap(direction_vector),-1))]
            forward_tracked_states = self.get_valid_neighbouring_agent_states(next_state)
            forward_tracked_states.remove(current_state)
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
        paths,new_priority_queue = Search().aStarSearch(start_state=start_state,goal_state=goal_state,next_states_function=self.get_next_states_from_path,all_solutions=all_solutions, priority_queue=priority_queue, return_priority_queue=True)
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
    
    # Game State based:

    def get_valid_game_state_actions(self,game_state):
        valid_actions = []
        for i in range(len(game_state.path_edges)):
            agent_state = AgentState(game_state.path_edges[i],i)
            goal_agent_state = AgentState(game_state.game.valves[2*i+1][1],game_state.game.valves[2*i+1][0])
            if agent_state != goal_agent_state:
                valid_actions += [(i,next_state.pos) for next_state in self.get_valid_neighbouring_agent_states(agent_state)]
        if not valid_actions: valid_actions.append('exit')
        return valid_actions
    
    def get_next_game_state_from_action(self,game_state,action):
        if action != 'exit':
            new_game_state = game_state.copy()
            new_game_state.update(action[1],action[0])
            return new_game_state

    def get_next_game_states_from_state(self,game_state):
        actions = self.get_valid_game_state_actions(game_state)
        if actions == ['exit']: return []
        else: return [self.get_next_game_state_from_action(game_state,action) for action in self.get_valid_game_state_actions(game_state)]
    
    def solve(self):
        goal_state_checker_function = lambda game_state: game_state.check_complete()
        solution = Search().breadthFirstSearch(
            start_state=self.game.game_state
            ,goal_state_checker_function=goal_state_checker_function
            ,next_states_function=self.get_next_game_states_from_state
            ,track_visited=True)
        self.game.game_state = solution
        return solution

class QLearningAgent(Agent):
    
    def play_game(self):
        next_state = self.game.game_state
        while not self.game.game_state.check_complete() and next_state:
            next_states = self.get_next_game_states_from_state(self.game.game_state)
            if next_states:
                next_state = util.pickRandomElement(next_states)
                self.game.game_state = next_state
            else: next_state = None
        result = 0
        if self.game.game_state.check_complete(): result = 1
        elif not next_state: result = -1
        self.game.game_state.reset()
        return result
