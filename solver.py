import game
from agent import Agent,AgentState,QLearningAgent
import util
import threading

game = game.generate_game('tiny') # small, medium, large
agent = Agent(game)
qLearningAgent = QLearningAgent(game)

# x = threading.Thread(target=agent.solve)
# x.start()

#### Search-based solving:
# agent.solve_recursively()
# agent.solve()

### Reinforcement learning-based solving:
# played = qLearningAgent.playGame(reset_game=False)
# print(played)
qLearningAgent.learn()
print(qLearningAgent.adopt_policy())

print(util.get_duration(game.start_time,'game solved'))
game.draw()
