from game import Game
import util

class AgentState:
    def __init__(self,pos = (0,0), value = -1):
        self.pos = pos
        self.value = value
    
    def __repr__(self):
        return '['+str(self.pos)+','+str(self.value)+']'

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
        if y < self.game.size[1] - 1 and (self.game.game_state.board_occupancy[x][y+1].value <= -1 or (self.game.game_state.board_occupancy[x][y-1].isValve and self.game.game_state.board_occupancy[x][y+1].value == agent_state.value)): valid_moves.append('South')
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
    
    def get_states_from_path(self,start_state,path):
        state_list = [start_state]
        state = start_state
        for action in path:
            state = self.get_next_agent_state_from_action(state,action)
            state_list.append(state)
        return state_list
        
    def graphSearch(self,start_state,goal_state,cost_function,**kwargs):
        priority_queue = util.PriorityQueue()
        priority_queue.push((start_state,[],0),0)
        visited = [start_state]   # need to use list for Python as can't have nested sets. Ok as anyway checking if exists before inserting
        heuristic = kwargs.get('heuristic', None)


        while not priority_queue.isEmpty():
            state, path, total_cost = priority_queue.pop()
            if state == goal_state:
                return path
            for successor in self.get_valid_neighbouring_agent_states(state):
                new_state, action, cost = successor
                if new_state not in visited:
                    cost = cost_function(total_cost,cost)
                    heuristic_value = heuristic(new_state) if heuristic else 0
                    priority_queue.push((new_state,path+[action],cost),cost + heuristic_value)
                    visited.append(new_state)
        return []
    
    def breadthFirstSearch(self,start_state,goal_state):
        fn = lambda x,y : x+1
        return self.graphSearch(start_state,goal_state, fn)

    def depthFirstSearch(self,start_state,goal_state):
        fn = lambda x,y : x-1
        return self.graphSearch(start_state,goal_state, fn)
    
    def solve(self):
        start_state = AgentState(pos=self.game.valves[0][1],value=self.game.valves[0][0])
        goal_state = AgentState(pos=self.game.valves[1][1],value=self.game.valves[1][0])
        states = self.get_states_from_path(start_state,self.breadthFirstSearch(start_state,goal_state))
        for state in states:
            self.update_game_state(pos=state.pos,value = state.value)
        return states

game = Game((5,5),4, util.sample_valves())
agent = Agent(game)
agent.solve()
game.game_state.print()
game.draw()
# agent.update_state()