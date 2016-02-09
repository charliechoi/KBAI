# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image

# Install Numpy and uncomment this line to access matrix operations.
import numpy as np

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        self.frames = {}
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return a list representing its
    # confidence on each of the answers to the question: for example 
    # [.1,.1,.1,.1,.5,.1] for 6 answer problems or [.3,.2,.1,.1,0,0,.2,.1] for 8 answer problems.
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will *not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # Make sure to return your answer *as a python list* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):

        ## code suggested by Ryan Peach @115 + slight editing
        ## feel free to use
        ## Where a is the input list
        #t = float(sum(a))
        #out = [x/t for x in a]
        self.parseProblem(problem) #parseproblem into frames
        transAB = self.getRelationship(self.frames['A'], self.frames['B']) #compare A and B

        return [.05,.1,.11,.12,.13,.14,.15,.2]

    def parseProblem(self,problem):
        for key in problem.figures:
            self.frames[key] = problem.figures[key].objects

    def getRelationship(self, frame1, frame2):
        transformations = {} #dictionary of transformation, 1st key=object, 2nd key = attribute
        #find out if any object has been deleted or added
        if len(frame1)>len(frame2): #something has been deleted
            scoredict={}
            for key in frame1:
                obj1=frame1[key]
                scoredict[key] = {}
                obj1key = key
                for key in frame2:
                    simscore = 0
                    obj2 = frame2[key]
                    obj2key = key
                    for key in obj1.attributes:
                        if key in obj2.attributes:
                            if obj1.attributes[key]==obj2.attributes[key]:
                                simscore+=1
                    scoredict[obj1key][obj2key] = simscore
            difference = self.findDiff(scoredict)
            transformations['deleted'] = difference

        return None

    def findDiff(self, scoredict):
        max = {}
        diff=[]
        std=next(iter (scoredict.values()))
        for key in std:
            obj2 = key
            maxval = 0
            maxkey = None
            for key in scoredict:
                value=scoredict[key][obj2]
                if value>=maxval:
                    maxval =value
                    maxkey = key
            max[maxkey] = obj2
        for key in scoredict:
            if key not in max:
                diff.append(key)
        return diff