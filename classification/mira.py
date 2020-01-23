# mira.py
# -------
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


# Mira implementation
import util
PRINT = True

class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys() # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        #  self.features = trainingData[0].keys() # could be useful later
        # DO NOT ZERO OUT YOUR WEIGHTS BEFORE STARTING TRAINING, OR
        # THE AUTOGRADER WILL LIKELY DEDUCT POINTS.
        allweights = {}

         #training for every c 
        for c in Cgrid:
          

            for iteration in range(self.max_iterations):
               # print "Starting iteration ", iteration, "..."
           
                for i in range(len(trainingData)):
                    #Set current f
                    f = trainingData[i]
                    #Set current real y
                    y = trainingLabels[i]
                    
                    #Find y' (maxY)
                    score = util.Counter()
                    for l in self.legalLabels:
                        score[l] = self.weights[l] * f
                    maxY = score.argMax()
                    
                    #Update weights
                    if maxY != y:
                        #calculate stepsize                        
                        fv = sum(map(lambda x: pow(x,2), f.values()))                       
                        stepsize = min(c, ((self.weights[maxY]-self.weights[y])*f+1.0)/(2.0*fv))
                        
                        
                        for key in self.features:
                            self.weights[y][key] = self.weights[y][key] + f[key] *stepsize                         
                            self.weights[maxY][key] = self.weights[maxY][key] - f[key] *stepsize     
                
            #calculcate accuracy
            guesslabels = self.classify(validationData)          
            accurate = [guesslabels[i] == validationLabels[i] for i in range(len(validationLabels))].count(True)
            #Store weights c and accuracy
            allweights[c,accurate] = self.weights 

        #Check which C is the best, in case of tie choose C with the lowest value 
        maxAccurate = 0
        minC = 100000000
        for key in allweights:
            print "key", key
            if key[1] == maxAccurate:
                if key[0] < minC:
                    self.weights = allweights[key].values()
                    minC = key[0]
                    print "lowestk", key

            if key[1] > maxAccurate:
                maxAccurate = key[1]
                minC = key[0]
                self.weights = allweights[key].values()      
                print "maxkey", key                

        

        

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses

    #for question 6c, in dataclassifier line 509, mira should be added to the option for findHighWeightFeatures 
    #(currently this option is only possible for the perceptron)
    def findHighWeightFeatures(self, label):
        """
        Returns a list of the 100 features with the greatest weight for some label
        """
        
        weights = self.weights[label]
        featuresWeights = weights.sortedKeys()[:100] 

        return featuresWeights

