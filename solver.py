import game
from agent import Agent
import util
import threading

game = game.generate_game('small')
agent = Agent(game)

# next = agent.get_next_states_from_path(agent.pos_path_to_state_path([(3, 0), (2,0)],0))
# print(next)

# x = threading.Thread(target=agent.solve_recursively)
# x.start()
print('solved..',agent.solve_recursively())
game.draw()
print(util.get_duration(game.start_time,'game solved'))