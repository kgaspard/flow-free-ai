import game
from agent import Agent,AgentState,QLearningAgent
import util
import threading

game = game.generate_game('tiny')
agent = Agent(game)
qLearningAgent = QLearningAgent(game)

# x = threading.Thread(target=agent.solve_recursively)
# x.start()

# agent.solve_recursively()
# agent.solve()
counter = 0
while counter <= 50:
  print(qLearningAgent.play_game())
  counter += 1
print(util.get_duration(game.start_time,'game solved'))
game.draw()
