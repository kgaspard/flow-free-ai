from game import Game
import time
import util

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

    def __init__( self, game):
        self.game = game
        self.start_state = game.valves[0][1] if game.valves else None

    def update_game_state(self,pos,value):
        self.game.game_state.update(pos,value)
    
    def get_valid_moves(self,agent_state):
        valid_moves = []
        x,y = agent_state.pos
        if y > 0 and (self.game.game_state.board_occupancy[x][y-1].value <= -1 or (self.game.game_state.board_occupancy[x][y-1].isValve and self.game.game_state.board_occupancy[x][y-1].value == agent_state.value)): valid_moves.append('North')
        if y < self.game.size[1] - 1 and (self.game.game_state.board_occupancy[x][y+1].value <= -1 or (self.game.game_state.board_occupancy[x][y+1].isValve and self.game.game_state.board_occupancy[x][y+1].value == agent_state.value)): valid_moves.append('South')
        if x > 0 and (self.game.game_state.board_occupancy[x-1][y].value <= -1 or (self.game.game_state.board_occupancy[x-1][y].isValve and self.game.game_state.board_occupancy[x-1][y].value == agent_state.value)): valid_moves.append('West')
        if x < self.game.size[0] - 1 and (self.game.game_state.board_occupancy[x+1][y].value <= -1 or (self.game.game_state.board_occupancy[x+1][y].isValve and self.game.game_state.board_occupancy[x+1][y].value == agent_state.value)): valid_moves.append('East')
        return valid_moves
    
    def get_next_agent_state_from_action(self,agent_state,action):
        x,y = agent_state.pos
        new_pos = agent_state.pos
        if action == 'North': new_pos = (x,y-1)
        if action == 'South': new_pos = (x,y+1)
        if action == 'West': new_pos = (x-1,y)
        if action == 'East': new_pos = (x+1,y)
        new_agent_state = AgentState(pos=new_pos, value=agent_state.value)
        return new_agent_state
    
    def get_valid_neighbouring_agent_states(self,agent_state):
        neighbouring_agent_states = []
        cost = 0
        for action in self.get_valid_moves(agent_state):
            neighbouring_agent_states.append((self.get_next_agent_state_from_action(agent_state,action),action,cost))
        return neighbouring_agent_states
        
    def graphSearch(self,start_state,goal_state,cost_function,**kwargs):
        all_solutions = kwargs.get('all_solutions', None)
        priority_queue = util.PriorityQueue()
        priority_queue.push((start_state,[start_state],0),0)
        global_visited = [start_state]   # need to use list for Python as can't have nested sets. Ok as anyway checking if exists before inserting
        heuristic = kwargs.get('heuristic', None)
        solution_paths = []

        while not priority_queue.isEmpty():
            state, path, total_cost = priority_queue.pop()
            if state == goal_state:
                if all_solutions:
                    solution_paths.append(path)
                else:
                    return [path]
            for successor in self.get_valid_neighbouring_agent_states(state):
                new_state, action, cost = successor
                if ((not all_solutions) and new_state not in global_visited) or (all_solutions and new_state not in path):
                    cost = cost_function(total_cost,cost)
                    heuristic_value = heuristic(new_state) if heuristic else 0
                    priority_queue.push((new_state,path+[new_state],cost),cost + heuristic_value)
                    if not all_solutions: global_visited.append(new_state)
        return solution_paths
    
    def breadthFirstSearch(self,start_state,goal_state,**kwargs):
        fn = lambda x,y : x+1
        return self.graphSearch(start_state,goal_state, fn, **kwargs)

    def depthFirstSearch(self,start_state,goal_state,**kwargs):
        fn = lambda x,y : x-1
        return self.graphSearch(start_state,goal_state, fn, **kwargs)

    def solve_for_value(self,value,all_solutions):
        valves = [valve for valve in self.game.valves if valve[0]==value]
        start_state = AgentState(pos=valves[0][1],value=valves[0][0])
        goal_state = AgentState(pos=valves[1][1],value=valves[1][0])
        paths = self.breadthFirstSearch(start_state=start_state,goal_state=goal_state,all_solutions=all_solutions)
        return paths
    
    def solve_recursively(self,value=0):
        solutions = self.solve_for_value(value=value,all_solutions=True)
        print('all: ',value,solutions)
        if not solutions: return solutions
        for solution in solutions:
            print(value,solution)
            for state in solution:
                self.update_game_state(pos=state.pos,value = state.value)
            if value == self.game.num_pairs - 1:
                return solution
            else:
                next_solution = self.solve_recursively(value=value+1)
                if not next_solution:
                    for state in solution:
                        self.update_game_state(pos=state.pos,value = -1)
                else:
                    return next_solution
        
        

game = Game((5,5),4, util.sample_valves())
agent = Agent(game)
print('done',agent.solve_recursively())
print(util.get_duration(game.start_time,'game solved'))
game.draw()