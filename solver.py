import game
from agent import SearchAgent,GameStateAgent,QLearningAgent
import util
import threading

game = game.generate_game('medium') # tiny, small, medium, large
qLearningAgent = QLearningAgent(game)

# x = threading.Thread(target=agent.solve)
# x.start()

#### Search-based solving:
# agent = SearchAgent(game)
# agent.solve_recursively()
# print(util.get_duration(game.start_time,'game solved'))
# game.draw()

### Reinforcement learning-based solving:
state,result = qLearningAgent.playGame(reset_game=False, draw=False)
# print(result)
learn = qLearningAgent.learn()
print(util.get_duration(game.start_time,'game solved'))
print(qLearningAgent.adopt_policy(draw=True))

