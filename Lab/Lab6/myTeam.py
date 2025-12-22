from captureAgents import CaptureAgent
import random
from game import Directions

def createTeam(firstIndex, secondIndex, isRed,
               first='AttackAgent', second='GuardAgent'):
    return [eval(first)(firstIndex), eval(second)(secondIndex)]

class BaseReflexAgent(CaptureAgent):
    def registerInitialState(self, state):
        CaptureAgent.registerInitialState(self, state)
        self.startPosition = state.getAgentPosition(self.index)

    def chooseAction(self, state):
        legalActions = state.getLegalActions(self.index)
        legalActions = [a for a in legalActions if a != Directions.STOP]

        actionScores = [self.evaluateAction(state, a) for a in legalActions]
        maxScore = max(actionScores)
        bestActions = [a for a, score in zip(legalActions, actionScores) if score == maxScore]

        return random.choice(bestActions)

    def evaluateAction(self, state, action):
        features = self.extractFeatures(state, action)
        weights = self.extractWeights(state, action)
        return sum(features[f] * weights[f] for f in features)

    def extractFeatures(self, state, action):
        return {}

    def extractWeights(self, state, action):
        return {}

class AttackAgent(BaseReflexAgent):
    def extractFeatures(self, state, action):
        features = {}
        successorState = state.generateSuccessor(self.index, action)
        myPos = successorState.getAgentPosition(self.index)

        foodPositions = self.getFood(successorState).asList()
        if foodPositions:
            features['closestFoodDist'] = min([self.getMazeDistance(myPos, food) for food in foodPositions])
        else:
            features['closestFoodDist'] = 0

        opponents = [successorState.getAgentState(i) for i in self.getOpponents(successorState)]
        ghosts = [o for o in opponents if not o.isPacman and o.getPosition() is not None]
        if ghosts:
            ghostDistances = [self.getMazeDistance(myPos, g.getPosition()) for g in ghosts]
            features['nearestGhostDist'] = min(ghostDistances)
        else:
            features['nearestGhostDist'] = 5

        return features

    def extractWeights(self, state, action):
        return {'closestFoodDist': -1.0, 'nearestGhostDist': 2.0}

class GuardAgent(BaseReflexAgent):
    def extractFeatures(self, state, action):
        features = {}
        nextState = state.generateSuccessor(self.index, action)
        myState = nextState.getAgentState(self.index)
        myPos = nextState.getAgentPosition(self.index)

        features['defending'] = 1
        if myState.isPacman:
            features['defending'] = 0

        opponents = [nextState.getAgentState(i) for i in self.getOpponents(nextState)]
        invaders = [o for o in opponents if o.isPacman and o.getPosition() is not None]
        features['invaderCount'] = len(invaders)

        if invaders:
            distances = [self.getMazeDistance(myPos, inv.getPosition()) for inv in invaders]
            features['closestInvaderDist'] = min(distances)
        else:
            features['closestInvaderDist'] = 0

        features['isStop'] = 1 if action == Directions.STOP else 0
        currentDir = state.getAgentState(self.index).configuration.direction
        reverseDir = Directions.REVERSE[currentDir]
        features['isReverse'] = 1 if action == reverseDir else 0

        return features

    def extractWeights(self, state, action):
        return {
            'invaderCount': -1000,
            'defending': 100,
            'closestInvaderDist': -10,
            'isStop': -100,
            'isReverse': -2
        }
