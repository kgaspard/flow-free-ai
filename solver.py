import game as Game
from agent import SearchAgent,GameStateAgent,QLearningAgent,ApproximateQLearningAgent
import util
from trainModel import model_accuracy

def search_based(options):
  agent = SearchAgent(options.game)
  agent.solve_recursively()
  print(util.get_duration(options.game.start_time,'game solved'))
  options.game.draw()

def exactQ(options):
  qLearningAgent = QLearningAgent(options.game,numTraining=options.numTraining,alpha=options.alpha)
  state,result = qLearningAgent.playGame(reset_game=False, draw=False)
  learn = qLearningAgent.learn()
  print(util.get_duration(options.game.start_time,'game solved'))
  print(qLearningAgent.adopt_policy(draw=True))

def approxQ(options):
  qLearningAgent = ApproximateQLearningAgent(options.game,numTraining=options.numTraining,epsilon=options.epsilon)
  learn = qLearningAgent.learn()
  print(learn)
  print(util.get_duration(options.game.start_time,'game solved'))
  print(qLearningAgent.adopt_policy(draw=True, game=options.game))

def cnn(options):
  options = util.parseCommandLine()
  build_model = options.buildmodel or False
  model_accuracy(model_path=options.modelpath,epochs=options.numTraining,build_model=build_model,draw=False)

def main():
  options = util.parseCommandLine()
  options.game = Game.generate_game(options.game) # tiny, small, medium, large
  if options.algorithm=='search': search_based(options)
  elif options.algorithm == 'exactQ': exactQ(options)
  elif options.algorithm == 'approxQ': approxQ(options)
  elif options.algorithm == 'cnn': cnn(options)
  else: print('invalid algorithm')

if __name__ == "__main__":
  main()