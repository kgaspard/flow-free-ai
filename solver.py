import game
from agent import Agent,AgentState
import util
import threading

game = game.generate_game('tiny')
agent = Agent(game)

# x = threading.Thread(target=agent.solve_recursively)
# x.start()

# agent.solve_recursively()
agent.solve()
print(util.get_duration(game.start_time,'game solved'))
game.draw()
