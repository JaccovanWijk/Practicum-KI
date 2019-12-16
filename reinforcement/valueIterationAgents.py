# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        for i in range(self.iterations):    #First create a for-loop for the amount of iterations
            storevalues = util.Counter()    #Because self.values is a util.Counter() we create a temporary one
            for s in mdp.getStates():       #to store the new values in. This way we update all values simultaniously
                snewvalue = None            #After that we create a for loop for all the states in the iteration
                for a in mdp.getPossibleActions(s):     #Then we create a for loop for every action for one state
                    temp = 0
                    for NextState, prob in mdp.getTransitionStatesAndProbs(s,a):    #We then loop over every transition for that action
                        temp += prob * (mdp.getReward(s,a,NextState) + discount * self.values[NextState])   #And calculate the Value of that action
                    snewvalue = max((snewvalue, temp))      #This max-funtion is to complete the Bellman function we have to integrate
                if snewvalue is not None:
                    storevalues[s] = snewvalue              #store the new values in the above created Util.Counter()
            self.values = storevalues                       #replace the old values with the new values in one go


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        mdp = self.mdp
        qvalue = 0
        for NextState, prob in mdp.getTransitionStatesAndProbs(state,action):
            qvalue += prob * (mdp.getReward(state,action,NextState) + self.discount * self.values[NextState]) #calcutaion of q value per nextState for an action
        return qvalue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        mdp = self.mdp
        highestQ = None
        bestA = None
        if mdp.isTerminal(state):       #return none if a terminal state
            return None
        else:
            for a in mdp.getPossibleActions(state):                 #loop over actions in a state
                aQvalue = self.computeQValueFromValues(state,a)     #Compute qvalue for an action
                if (max((highestQ, aQvalue)) == aQvalue):           #If the q value is higher then the last one switch action
                    highestQ = aQvalue
                    bestA = a
            return bestA                                            #return the best action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
