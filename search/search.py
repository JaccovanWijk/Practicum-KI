# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    # """
    path = []
    closedList = []
    if problem.isGoalState(problem.getStartState()):
        return path

    #Create startstate and push it to the stack
    openList = util.Stack() 
    startState = ((problem.getStartState()), 'start', 1, [])
    openList.push(startState)

    while not openList.isEmpty():       
        #Get currentstate from queue
        currentState = openList.pop()

        #Check for goalstate and return path      
        if problem.isGoalState(currentState[0]):
            path = [element for element in currentState[3]]
            path.append(currentState[1])                       
            path.pop(0)                
            return path
        
        #Find new states and add them to stack
        if currentState[0] not in closedList:
            closedList.append(currentState[0])  
            path = [element for element in currentState[3]]
            path.append(currentState[1])  
            for nextState in problem.getSuccessors(currentState[0]):     
                nextState = (nextState[0], nextState[1], nextState[2], path)                
                openList.push(nextState) 
         
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    path = []
    closedList = []
    if problem.isGoalState(problem.getStartState()):
        return path

    #Create startstate and push it to the queue
    openList = util.Queue() 
    startState = ((problem.getStartState()), 'start', 1, [])
    openList.push(startState)

    while not openList.isEmpty():       
        #Get currentstate from queue
        currentState = openList.pop()

        #Check for goalstate and return path      
        if problem.isGoalState(currentState[0]):
            path = [element for element in currentState[3]]
            path.append(currentState[1])                       
            path.pop(0)                
            return path
        
        #Find new states and add them to queue
        if currentState[0] not in closedList:
            closedList.append(currentState[0])  
            path = [element for element in currentState[3]]
            path.append(currentState[1])  
            for nextState in problem.getSuccessors(currentState[0]):     
                nextState = (nextState[0], nextState[1], nextState[2], path)                
                openList.push(nextState) 

def uniformCostSearch(problem):
    openList = util.PriorityQueue()
    path = []
    closedList = []
    if problem.isGoalState(problem.getStartState()):
        return path

    #Create startstate and put it into openlist
    startState = ((problem.getStartState()), 'start', 0, [], 0)
    openList.push(startState, startState[2])

    while not openList.isEmpty():    
        #Get state from priorityqueue
        currentState, currentNode, costForCurrentStep, currentPath, totalCurrentCost = openList.pop()  
     
        #Check for goalstate and return path
        if problem.isGoalState(currentState):
            path = [element for element in currentPath]
            path.append(currentNode)                       
            path.pop(0)       #to remove  'start' which i added 
            return path      
        
        #Find new states and add them to priorityqueue using the uniform cost function     
        if currentState not in closedList:
            closedList.append(currentState)  
            path = [element for element in currentPath]
            path.append(currentNode)                     
            for nextState in problem.getSuccessors(currentState):                    
                nextState = (nextState[0], nextState[1], nextState[2], path, totalCurrentCost + nextState[2])  
                openList.update(nextState, nextState[4]) 



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
      

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    openList = util.PriorityQueue()
    path = []
    closedList = []
    if problem.isGoalState(problem.getStartState()):
        return path

    #Create startstate and put it into openlist
    startState = ((problem.getStartState()), 'start', 0, [], 0)
    openList.push(startState, startState[2])

    while not openList.isEmpty():    
        #Get state from priorityqueue
        currentState, currentNode, costForCurrentStep, currentPath, totalCurrentCost = openList.pop()  
     
        #Check for goalstate and return path
        if problem.isGoalState(currentState):
            path = [element for element in currentPath]
            path.append(currentNode)                       
            path.pop(0)       #to remove  'start' which i added 
            return path      
        
        #Find new states and add them to priorityqueue using the heuristic
        if currentState not in closedList:
            closedList.append(currentState)  
            path = [element for element in currentPath]
            path.append(currentNode)                     
            for nextState in problem.getSuccessors(currentState):                    
                nextState = (nextState[0], nextState[1], nextState[2], path, totalCurrentCost+nextState[2])  
                openList.update(nextState, totalCurrentCost + nextState[2] + heuristic(nextState[0], problem))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
