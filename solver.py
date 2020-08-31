import game as Game
from agent import SearchAgent,GameStateAgent,QLearningAgent,ApproximateQLearningAgent
import util
import threading
import dataParser

options = util.parseCommandLine()
game = Game.generate_game(options.game) # tiny, small, medium, large

# x = threading.Thread(target=agent.solve)
# x.start()

#### Search-based solving:
# agent = SearchAgent(game)
# agent.solve_recursively()
# print(util.get_duration(game.start_time,'game solved'))
# game.draw()

### Reinforcement learning-based solving:

## Exact qAgent:
# qLearningAgent = QLearningAgent(game,numTraining=options.numTraining)
# state,result = qLearningAgent.playGame(reset_game=False, draw=False)
# print(result)
# learn = qLearningAgent.learn()
# print(util.get_duration(game.start_time,'game solved'))
# print(qLearningAgent.adopt_policy(draw=True))

## Approximate qAgent:
# qLearningAgent = ApproximateQLearningAgent(game,numTraining=options.numTraining,epsilon=options.epsilon)
# learn = qLearningAgent.learn()
# print(learn)
# print(util.get_duration(game.start_time,'game solved'))
# print(qLearningAgent.adopt_policy(draw=True, game=game))
# print(qLearningAgent.adopt_policy(draw=True, game=Game.generate_game('large')))

new_game = dataParser.test_game()
new_game.draw()