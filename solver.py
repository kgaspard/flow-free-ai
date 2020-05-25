from game import Game
from agent import Agent
import util

game = Game((5,5),4, util.sample_valves())
# game = Game((14,14),12, util.sample_valves_big())
agent = Agent(game)
agent.solve_recursively()
print(util.get_duration(game.start_time,'game solved'))
game.draw()