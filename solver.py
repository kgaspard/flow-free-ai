import game
from agent import Agent
import util
import threading

game = game.generate_game('medium')
agent = Agent(game)

# x = threading.Thread(target=agent.solve_recursively)
# x.start()

agent.solve_recursively()
print(util.get_duration(game.start_time,'game solved'))
game.draw()