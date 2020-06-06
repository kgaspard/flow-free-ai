import game
from agent import Agent,AgentState,QLearningAgent
import util
import threading

game = game.generate_game('medium') # small, medium, large
agent = Agent(game)
qLearningAgent = QLearningAgent(game)

# x = threading.Thread(target=agent.solve_recursively)
# x.start()

agent.solve_recursively()
agent.solve()
# qLearningAgent.learn()
# print(qLearningAgent.adopt_policy())

print(util.get_duration(game.start_time,'game solved'))
game.draw()
