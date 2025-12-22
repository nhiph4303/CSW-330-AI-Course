# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        if successorGameState.isWin():
            return float("inf")
        if successorGameState.isLose():
            return -float("inf")
        
        # Bắt đầu từ score hiện có của successor state
        score = successorGameState.getScore()

        # --- ƯU TIÊN ĂN FOOD GẦN ---

        # Food list sau khi đi action này
        foodList = newFood.asList()

        # Càng ít food càng tốt → phạt nhẹ số lượng food còn lại
        score -= 2.0 * len(foodList)

        # Nếu còn food thì tính khoảng cách tới food gần nhất
        if foodList:
            minFoodDist = min(manhattanDistance(newPos, foodPos) for foodPos in foodList)
            # Dùng reciprocal: khoảng cách càng nhỏ → 1/(d+1) càng lớn → score cao hơn
            score += 10.0 / (minFoodDist + 1.0)

        # --- XỬ LÝ GHOST ---
        for ghostState, scaredTime in zip(newGhostStates, newScaredTimes):
            ghostPos = ghostState.getPosition()
            distToGhost = manhattanDistance(newPos, ghostPos)

            if scaredTime == 0:
                # Ghost bình thường: nếu quá gần thì cực kỳ nguy hiểm
                if distToGhost <= 1:
                    score -= 1000.0
                else:
                    # Càng lại gần ghost thường càng bị phạt nhẹ
                    score -= 2.0 / (distToGhost + 1.0)
            else:
                # Ghost đang scared: khuyến khích lại gần để ăn
                score += 5.0 / (distToGhost + 1.0)

        # --- HẠN CHẾ ĐỨNG YÊN ---
        if action == Directions.STOP:
            score -= 5.0
        return score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    
    numAgents = gameState.getNumAgents()
    def minimax(state, depth, agentIndex):
      # Điều kiện dừng: thắng/thua hoặc đạt độ sâu tối đa
      if state.isWin() or state.isLose() or depth == self.depth:
        return self.evaluationFunction(state)

      legalActions = state.getLegalActions(agentIndex)
      if not legalActions:
        return self.evaluationFunction(state)
      
      # Xác định agent tiếp theo
      nextAgent = (agentIndex + 1) % numAgents
      # Sau con ma cuối cùng quay lại Pacman → tăng depth (1 ply mới)
      nextDepth = depth + 1 if nextAgent == 0 else depth

      # Pacman = MAX
      if agentIndex == 0:
        value = float("-inf")
        for action in legalActions:
          successor = state.generateSuccessor(agentIndex, action)
          value = max(value, minimax(successor, nextDepth, nextAgent))
        return value
      # Ghost = MIN
      else:
        value = float("inf")
        for action in legalActions:
          successor = state.generateSuccessor(agentIndex, action)
          value = min(value, minimax(successor, nextDepth, nextAgent))
        return value

    # Ở root: Pacman chọn action có giá trị minimax lớn nhất
    bestValue = float("-inf")
    bestAction = Directions.STOP
    legalActions = gameState.getLegalActions(0)

    for action in legalActions:
      successor = gameState.generateSuccessor(0, action)
      # Sau Pacman là ghost đầu tiên (nếu có)
      nextAgent = 1 if numAgents > 1 else 0
      value = minimax(successor, 0, nextAgent)

      if value > bestValue:
        bestValue = value
        bestAction = action

    return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    numAgents = gameState.getNumAgents()

    def alphabeta(state, depth, agentIndex, alpha, beta):
      # Điều kiện dừng: thắng/thua hoặc đạt độ sâu tối đa
      if state.isWin() or state.isLose() or depth == self.depth:
        return self.evaluationFunction(state)

      legalActions = state.getLegalActions(agentIndex)
      if not legalActions:
        return self.evaluationFunction(state)

      # Xác định agent tiếp theo
      nextAgent = (agentIndex + 1) % numAgents
      # Sau con ma cuối cùng quay lại Pacman → tăng depth (1 ply mới)
      nextDepth = depth + 1 if nextAgent == 0 else depth

      # Pacman = MAX
      if agentIndex == 0:
        value = float("-inf")
        for action in legalActions:
          successor = state.generateSuccessor(agentIndex, action)
          childValue = alphabeta(successor, nextDepth, nextAgent, alpha, beta)
          if childValue > value:
            value = childValue

          # Cập nhật alpha
          if value > alpha:
            alpha = value

          # Prune khi value > beta (KHÔNG prune khi ==)
          if value > beta:
            break

        return value

      # Ghost = MIN
      else:
        value = float("inf")
        for action in legalActions:
          successor = state.generateSuccessor(agentIndex, action)
          childValue = alphabeta(successor, nextDepth, nextAgent, alpha, beta)
          if childValue < value:
            value = childValue

          # Cập nhật beta
          if value < beta:
            beta = value

          # Prune khi value < alpha (KHÔNG prune khi ==)
          if value < alpha:
            break

        return value

    # Ở root: Pacman chọn action có giá trị tốt nhất, đồng thời cập nhật alpha
    bestValue = float("-inf")
    bestAction = Directions.STOP
    alpha = float("-inf")
    beta = float("inf")

    legalActions = gameState.getLegalActions(0)

    for action in legalActions:
      successor = gameState.generateSuccessor(0, action)
      # Sau Pacman là ghost đầu tiên (nếu có)
      nextAgent = 1 if numAgents > 1 else 0
      value = alphabeta(successor, 0, nextAgent, alpha, beta)

      if value > bestValue:
        bestValue = value
        bestAction = action

      # Cập nhật alpha ở root
      if bestValue > alpha:
        alpha = bestValue

      # Không cần prune ở root quá gắt, nhưng có thể:
      if bestValue > beta:
        break

    return bestAction