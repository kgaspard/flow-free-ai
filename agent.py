from game import Game,GameState
import time
import util
from util import Search
import featureFunctions

class AgentState:
    def __init__(self,pos = (0,0), value = -1):
        self.pos = pos
        self.value = value
    
    def __repr__(self):
        return str(self.pos)
        # return '['+str(self.pos)+','+str(self.value)+']'

    def __eq__(self,other):
        return self.pos == other.pos and self.value == other.value

class AgentFunctions:

    def __init__( self, game_state):
        self.game_state = game_state
        self.game = game_state.game

    def get_valid_neighbouring_agent_states(self,agent_state):
        valid_neighbouring_agent_states = []
        x,y = agent_state.pos
        if y > 0 and (self.game_state.board_occupancy[x][y-1].value <= -1 or (self.game_state.board_occupancy[x][y-1].isValve and self.game_state.board_occupancy[x][y-1].value == agent_state.value and not self.game_state.board_occupancy[x][y-1].isStartValve)):
            valid_neighbouring_agent_states.append(AgentState(pos=(x,y-1),value=agent_state.value)) # North
        if y < self.game.size[1] - 1 and (self.game_state.board_occupancy[x][y+1].value <= -1 or (self.game_state.board_occupancy[x][y+1].isValve and self.game_state.board_occupancy[x][y+1].value == agent_state.value and not self.game_state.board_occupancy[x][y+1].isStartValve)):
            valid_neighbouring_agent_states.append(AgentState(pos=(x,y+1),value=agent_state.value)) # South
        if x > 0 and (self.game_state.board_occupancy[x-1][y].value <= -1 or (self.game_state.board_occupancy[x-1][y].isValve and self.game_state.board_occupancy[x-1][y].value == agent_state.value and not self.game_state.board_occupancy[x-1][y].isStartValve)):
            valid_neighbouring_agent_states.append(AgentState(pos=(x-1,y),value=agent_state.value)) # West
        if x < self.game.size[0] - 1 and (self.game_state.board_occupancy[x+1][y].value <= -1 or (self.game_state.board_occupancy[x+1][y].isValve and self.game_state.board_occupancy[x+1][y].value == agent_state.value and not self.game_state.board_occupancy[x+1][y].isStartValve)):
            valid_neighbouring_agent_states.append(AgentState(pos=(x+1,y),value=agent_state.value)) # East
        return valid_neighbouring_agent_states

    def get_next_states_from_path(self,path):
        if not path: return None
        current_state = path[-1]
        next_states = self.get_valid_neighbouring_agent_states(current_state)
        goal_state = AgentState(pos=self.game.valves[2*current_state.value+1][1],value=current_state.value)
        if goal_state in next_states: return [goal_state]
        if len(path) < 2: return next_states
        new_next_states = []
        for next_state in next_states:
            if next_state==path[-2]: continue
            direction_vector = util.tupleDiff(next_state.pos,current_state.pos)
            forward_tracked_positions = [util.tupleAdd(next_state.pos,direction_vector), util.tupleAdd(next_state.pos,util.tupleSwap(direction_vector)), util.tupleAdd(next_state.pos,util.tupleScale(util.tupleSwap(direction_vector),-1))]
            forward_tracked_states = [AgentState(forward_tracked_position,current_state.value) for forward_tracked_position in forward_tracked_positions]
            add_state = True
            for forward_tracked_state in forward_tracked_states:
                if forward_tracked_state in path:
                    add_state = False
                    break
            if add_state: new_next_states.append(next_state)
        return new_next_states

class SearchAgent(AgentFunctions):

    def __init__( self, game):
        game_state = game.game_state
        AgentFunctions.__init__(self, game_state)
        self.game = game

    def update_game_state(self,pos,value):
        self.game.game_state.update(pos,value)
    
    
    def pos_path_to_state_path(self,pos_path,value):
        state_path = []
        for pos in pos_path:
            state_path.append(AgentState(pos,value))
        return state_path

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
    
class GameStateAgent(AgentFunctions):

    def __init__( self, game):
        self.game = game

    def get_valid_game_state_actions(self,game_state):
        valid_actions = []
        if not game_state: return valid_actions
        valve_index = game_state.active_path
        agent_path = [AgentState(pos,valve_index) for pos in game_state.paths[valve_index]]
        agent_state = agent_path[-1]
        goal_agent_state = AgentState(game_state.game.valves[2*valve_index+1][1],game_state.game.valves[2*valve_index+1][0])
        state_searcher = AgentFunctions(game_state)
        if agent_state != goal_agent_state:
            valid_actions += [(valve_index,next_state.pos) for next_state in state_searcher.get_next_states_from_path(agent_path)]
            if not valid_actions: valid_actions.append('exit lose')
        elif game_state.active_path < game_state.game.num_pairs - 1:
            valid_actions.append('next color')
        else:
            valid_actions.append('exit win')
        return valid_actions
    
    def get_next_game_state_from_action(self,game_state,action):
        if action == 'exit lose': return None
        elif action == 'exit win': return None
        elif action == 'next color':
            new_active_path = game_state.active_path + 1
            new_game_state = game_state.update_and_copy(active_path=new_active_path)
            return new_game_state
        else:
            new_game_state = game_state.update_and_copy(position_tuple=action[1],value=action[0])
            return new_game_state

    def get_next_game_states_from_state(self,game_state):
        actions = self.get_valid_game_state_actions(game_state)
        if actions == ['exit lose'] or actions == ['exit win']: return []
        else: return [self.get_next_game_state_from_action(game_state,action) for action in self.get_valid_game_state_actions(game_state)]

    ############# DEPRECATED - for testing only ############# 
    def solve_with_search(self):
        goal_state_checker_function = lambda game_state: game_state.check_complete()
        solution = Search().breadthFirstSearch(
            start_state=self.game.game_state
            ,goal_state_checker_function=goal_state_checker_function
            ,next_states_function=self.get_next_game_states_from_state
            ,track_visited=True)
        self.game.game_state = solution
        return solution
    #########################################################

    def playGame(self):
        current_state = self.game.game_state.update_and_copy()
        next_state = 1
        while not current_state.check_complete() and next_state:
            next_states = self.get_next_game_states_from_state(current_state)
            if next_states:
                next_state = util.pickRandomElement(next_states)
                current_state = next_state.update_and_copy()
            else: next_state = None
        result = 0
        if current_state.check_complete(): result = 1
        elif not next_state: result = -1
        # self.game.game_state.reset()
        return result

class QLearningAgent(GameStateAgent):

    def __init__(self, game, alpha=0.5, epsilon=0.4, gamma=0.99, numTraining = 100, **args):
        GameStateAgent.__init__(self, game, **args)
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.numTraining = numTraining
        self.qValues = util.Counter()

    def getLegalActions(self, state):
        return self.get_valid_game_state_actions(state)

    def getQValue(self, state,action):
        return self.qValues[(state,action)]

    def getQValues(self):
        return self.qValues

    def computeValueFromQValues(self, state):
        q_values = [self.getQValue(state,action) for action in self.getLegalActions(state)]
        return max(q_values) if q_values else 0

    def getAction(self, state):
        legalActions = self.getLegalActions(state)
        action = None
        if legalActions:
          if util.flipCoin(self.epsilon):
            action = util.pickRandomElement(legalActions)
          else:
            action = max(legalActions, key = lambda action: self.getQValue(state,action))
        return action

    def getReward(self, state, action, nextState):
        if action == 'exit win': return 100
        elif action == 'exit lose': return -100
        elif action == 'next color': return 100/state.game.num_pairs
        else: return 0

    def updateQValue(self, state, action, nextState):
        current_q_value = self.getQValue(state,action)
        reward = self.getReward(state, action, nextState)
        q_value_increment = reward + (self.gamma * self.computeValueFromQValues(nextState))
        new_q_value = ((1-self.alpha)*current_q_value) + (self.alpha * q_value_increment)
        self.qValues[(state,action)] = new_q_value

    def playGame(self, reset_game=True, draw=False, trackReward=False, game=None):
        game = game if game else self.game
        state = game.game_state.update_and_copy()
        next_state = 1
        reward = 0
        while next_state:
            action = self.getAction(state)
            next_state = self.get_next_game_state_from_action(state,action)
            self.updateQValue(state, action, next_state)
            if trackReward: reward += self.getReward(state, action, next_state)
            if next_state:
                state = next_state.update_and_copy()
        result = 0
        if state.check_complete(): result = 1
        else: result = -1
        if draw: state.draw()
        # if reset_game: self.game.game_state.reset()
        return (state,result)
    
    def learn(self):
        counter = 0
        win_counter = 0
        while counter < self.numTraining:
            end_state,game_result = self.playGame()
            win_counter += game_result if game_result == 1 else 0
            counter += 1
        print(util.get_duration(self.game.start_time,'training done - won '+str(100*win_counter/counter)+'% of games'))
        return self.getQValues()

    def adopt_policy(self, draw=False, game=None):
        game = game if game else self.game
        epsilon_store = self.epsilon
        self.epsilon = 0
        state,result = self.playGame(reset_game=False, game=game)
        self.epsilon = epsilon_store
        if draw: state.draw()
        return result

class ApproximateQLearningAgent(QLearningAgent):

    def __init__(self, game, alpha=0.9, epsilon=0.4, gamma=0.99, numTraining = 100, **args):
        QLearningAgent.__init__(self, game=game, alpha=alpha, epsilon=epsilon, gamma=gamma,  numTraining = numTraining, **args)
        self.weights = util.Counter()

    def getFeatures(self,state,action,nextState=None):
        next_state = nextState if nextState else self.get_next_game_state_from_action(state,action) # a feature only depends on state and action, but adding next_state as an option to not have to calculate it twice
        if not next_state: next_state=state.update_and_copy()
        features = util.Counter()
        features["number_of_turns"] = sum([featureFunctions.number_of_turns_in_path(path) for path in next_state.paths])
        features["number_of_boxes"] = sum([len(featureFunctions.boxes_in_path(path)) for path in next_state.paths])
        features["total_manhattan_distance_to_goal"] = sum([util.manhattanDistance(path[-1],next_state.game.valves[2*i+1][1]) for i,path in enumerate(next_state.paths)])
        valves_in_boxes = 0
        boxes_with_no_valves = 0
        for i,path in enumerate(next_state.paths):
            valves = [valve[1] for valve in next_state.game.valves if valve[0] != i]
            for box in featureFunctions.boxes_in_path(path):
                l = len(box.pointsInBoxRectangle(valves))
                valves_in_boxes += l
                if l==0: boxes_with_no_valves+=1
        features["valves_in_boxes"] = valves_in_boxes
        features["boxes_with_no_valves"] = boxes_with_no_valves
        features["is_wall_hug"] = featureFunctions.is_wall_hug(state,next_state)
        features.divideAll(1000.0) # prevent divergence of values
        return features

    def getQValue(self, state,action,features=None):
        features = features if features else self.getFeatures(state,action) #to not have to recalculate twice
        return features * self.weights

    def getQValues(self):
        return self.weights

    def computeValueFromQValues(self, state,features=None):
        q_values = [self.getQValue(state,action,features) for action in self.getLegalActions(state)]
        return max(q_values) if q_values else 0

    def updateQValue(self, state, action, nextState):
        features = self.getFeatures(state=state,action=action,nextState=nextState)
        reward = self.getReward(state, action, nextState)
        difference = (reward + (self.gamma * self.computeValueFromQValues(state=nextState))) - self.getQValue(state,action,features)
        for feature in features:
            self.weights[feature] += self.alpha * difference * features[feature]

    def plot_features(features):
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
        x=[]
        y=[]
        for key in features:
            x.append(key)
            y.append(features[key])
        ax.bar(x,y)
        ax.axhline(y=0, color='k')
        plt.xlabel('Approximate Q-learning feature weights')
        plt.show()