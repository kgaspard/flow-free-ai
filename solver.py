import game
from agent import SearchAgent,GameStateAgent,QLearningAgent,ApproximateQLearningAgent
import util
import threading
import sys, types

def parseCommandLine():
    from optparse import OptionParser
    usageStr = "example"
    parser = OptionParser(usageStr)
    parser.add_option('-g', '--game', dest='game', help='the game to play', default='small')
    options, rest_of_command = parser.parse_args()
    if len(rest_of_command) != 0: raise Exception('Command line input not understood: ' + str(rest_of_command))
    return options

options = parseCommandLine()
game = game.generate_game(options.game) # tiny, small, medium, large
qLearningAgent = ApproximateQLearningAgent(game)

# x = threading.Thread(target=agent.solve)
# x.start()

#### Search-based solving:
# agent = SearchAgent(game)
# agent.solve_recursively()
# print(util.get_duration(game.start_time,'game solved'))
# game.draw()

### Reinforcement learning-based solving:
state,result = qLearningAgent.playGame(reset_game=False, draw=True)
print(qLearningAgent.getFeatures(state,None))
# print(result)
# learn = qLearningAgent.learn()
print(util.get_duration(game.start_time,'game solved'))
# print(qLearningAgent.adopt_policy(draw=True))

