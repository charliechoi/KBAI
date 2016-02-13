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
from collections import defaultdict
from RavensObject import RavensObject
from collections import OrderedDict
class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        self.frames = OrderedDict()
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
        print("Problem: "+str(problem.name))
        self.parseProblem(problem) #parseproblem into frames
        transAB, connAB, connAB2 = self.getRelationship(self.frames['A'], self.frames['B']) #compare A and B
        #print(transAB)
        transAC, connAC, connAC2 = self.getRelationship(self.frames['A'], self.frames['C']) #compare A and C
        genCD = self.generate(self.frames['C'], connAC, connAC2, transAB)
        probArray= self.test(case=genCD, transAB=transAB, connAC=connAC, connAC2=connAC2)
        print(problem.checkAnswer(probArray))
        return probArray
        #return [0.1, 0.1, 0.2, 0.2, 0.4]

    def parseProblem(self,problem):
        for key in problem.figures:
            self.frames[key] = problem.figures[key].objects

    def test(self, case, transAB, connAC, connAC2):
        probability=[]
        total = 0
        for i in range(1,7):
            weight=0
            temp=0
            figure = self.frames[str(i)]
            if len(figure)!=len(case):
                probability.append(0)
            else:
                scores = self.getScore(case, figure)
                #print(scores)
                (difference, connected) = self.findDiff(scores)
                translation = self.compAnswer(case, figure, connected)
                print(translation)
                maxscore = len(translation)
                for key in translation:
                    if len(translation[key])==0:
                        temp+=1
                if temp==maxscore:
                    probability.append(100)
                else:
                    probability.append(temp)
                total+=temp
        if 100 in probability:
            probability = [0 if x is not 100 else 1 for x in probability]
            probability = [1.0 if x is not 0 else x for x in probability]
            total = sum(probability)
            probability=[x/total for x in probability]
        else:
            probability = [x/total for x in probability]
        print(probability)
        return probability

    #generate most probable frame as answer
    def generate(self, frameC, connAC, connAC2, transAB):
        #prep frame C for semantics in frame A
        newframe = {}
        if 'a' in connAC2:
            for key in connAC2:
                frameC[key] = frameC[connAC2[key]]
                del frameC[connAC2[key]]
        elif 'a' in connAC:
            for key in connAC:
                frameC[key] = frameC[connAC[key]]
                del frameC[connAC[key]]
        for key in transAB:
            tf = transAB[key]
            if len(tf)==0:
                for obj in frameC:
                    if obj not in newframe:
                        newframe[obj]={}
                    if key in frameC[obj].attributes:
                        newframe[obj][key]=frameC[obj].attributes[key]
            else:
                for obj in frameC:
                    if obj not in newframe:
                        newframe[obj]={}
                    if key in frameC[obj].attributes:
                        if obj in tf:
                            if key!='alignment':
                                if tf[obj][1]!='None':
                                    if key=='angle':
                                        difference = [(int(frameC[obj].attributes[key])+int(tf[obj][1])), (int(frameC[obj].attributes[key])-int(tf[obj][1]))]
                                        difference=[(x-360) if x>360 else x for x in difference]
                                        difference=[abs(x) if x<0 else x for x in difference]
                                        difference=[str(x) for x in difference]
                                        print("angle difference: ")
                                        print(difference)
                                        newframe[obj][key] = difference
                                    else:
                                        newframe[obj][key] = tf[obj][1]
                            else:
                                att = ''
                                splitC = frameC[obj].attributes[key].split('-')
                                if 'bottomup' in tf[obj]:
                                    buC = splitC[0]
                                    if buC =='bottom':
                                        final = 'up'
                                    else:
                                        final = 'bottom'
                                    att +=final
                                else:
                                    final = splitC[0]
                                    att+=final
                                if 'leftright' in tf[obj]:
                                    lrC = splitC[1]
                                    if lrC =='left':
                                        final = 'right'
                                    else:
                                        final = 'left'
                                    att=att+'-'+final
                                else:
                                    final =splitC[1]
                                    att=att+'-'+final
                                newframe[obj][key]=att
                        else:
                            newframe[obj][key]=frameC[obj].attributes[key]
        if 'deleted' in transAB:
            for obj in transAB['deleted']:
                del newframe[obj]
        #print(newframe)
        for key in newframe:
            temp = RavensObject(key)
            temp.attributes = newframe[key]
            newframe[key] = temp
        return newframe

    #wrapper for getting relationships
    def getRelationship(self, frame1, frame2):
        #find out if any object has been deleted or added
        if len(frame1)>len(frame2): #something has been deleted
            scoredict=self.getScore(frame1, frame2)
            (difference, connected) = self.findDiff(scoredict)
            (abs,rel) = self.compAtt(frame1, frame2, connected)
            connected = {y:x for x,y in connected.items()}
            abs['deleted'] = difference
        elif len(frame1)<len(frame2):
            scoredict=self.getScore(frame2, frame1)
            (difference, connected) = self.findDiff(scoredict)
            (abs,rel) = self.compAtt(frame2, frame1, connected)
            abs['added'] = difference
        else:
            scoredict=self.getScore(frame1, frame2)
            (difference, connected) = self.findDiff(scoredict, equal=True)
            (abs,rel) = self.compAtt(frame1, frame2, connected)
        connected2 = {y:x for x,y in connected.items()}
        return abs, connected, connected2

    #compare each attribute in the object and find out what the transformation is
    def compAtt(self, larger, smaller, connected):
        abstransform = {}
        reltransform = {}
        attributes = ['shape', 'size', 'fill', 'inside', 'angle', 'alignment', 'above']
        #get attribute transformation
        for key in connected:
            L = larger[key].attributes
            S = smaller[connected[key]].attributes
            for att in attributes:
                if att in L and att in S:
                    if att not in abstransform:
                        abstransform[att]={}
                        reltransform[att]={}
                    if L[att]!=S[att]:
                        if att=='angle':
                            difference = str(int(L[att])-int(S[att]))
                            #print(difference)
                            abstransform[att][key] = ['0', difference]
                        elif att=='alignment':
                            config={}
                            splitL = L[att].split('-')
                            splitS = S[att].split('-')
                            if splitL[0]!=splitS[0]:
                                config['bottomup'] = [splitL[0], splitS[0]]
                            if splitL[1]!=splitS[1]:
                                config['leftright'] = [splitL[1], splitS[1]]
                            abstransform[att][key] = config
                        else:
                            abstransform[att][key] = [L[att], S[att]]
                        reltransform[att][key] = True
                elif att not in L and att in S:
                    if att not in abstransform:
                        abstransform[att]={}
                        reltransform[att]={}
                    abstransform[att][key]=['None', S[att]]
                    reltransform[att][key] = True
                elif att in L and att not in S:
                    if att not in abstransform:
                        abstransform[att]={}
                        reltransform[att]={}
                    abstransform[att][key]=[L[att], 'None']
                    reltransform[att][key] = True
                else:
                    pass
        return (abstransform, reltransform)

    def compAnswer(self, test, choice, connected):
        abstransform = {}
        reltransform = {}
        attributes = ['shape', 'size', 'fill', 'inside', 'angle', 'alignment', 'above']
        #print(connected)
        #get attribute transformation
        for key in connected:
            L = test[key].attributes
            S = choice[connected[key]].attributes
            for att in attributes:
                if att in L and att in S:
                    if att not in abstransform:
                        abstransform[att]={}
                        reltransform[att]={}
                    if L[att]!=S[att]:
                        if att=='inside' or att=='above':
                            testkey = L[att]
                            choicekey = S[att]
                            if testkey in connected:
                                test2choiceKey = connected[testkey]
                                if test2choiceKey==choicekey:
                                    abstransform[att][key] = {}
                                else:
                                    abstransform[att][key] = [L[att], S[att]]
                            elif choicekey in connected:
                                choice2testKey = connected[choicekey]
                                if choice2testKey==testkey:
                                    abstransform[att][key] = {}
                                else:
                                    abstransform[att][key] = [L[att], S[att]]
                        elif att=='angle':
                            choicekey=S[att]
                            #print('choicekey: '+choicekey)
                            for angle in L[att]:
                                if angle==choicekey:
                                    abstransform[att] = {}
                                    #print(angle)
                                    break
                                else:
                                    abstransform[att][key] = [L[att], S[att]]
                        else:
                            abstransform[att][key] = [L[att], S[att]]
                            reltransform[att][key] = True
                elif att not in L and att in S:
                    if att not in abstransform:
                        abstransform[att]={}
                        reltransform[att]={}
                    abstransform[att][key]=['None', S[att]]
                    reltransform[att][key] = True
                elif att in L and att not in S:
                    if att not in abstransform:
                        abstransform[att]={}
                        reltransform[att]={}
                    abstransform[att][key]=[L[att], 'None']
                    reltransform[att][key] = True
                else:
                    pass
        return abstransform

    #find out which objects correspond to which, and how each frame is different in terms of objects
    '''def findDiff(self, scoredict, equal=False):
        max = {}
        diff=[]
        temp=defaultdict(list)
        print(scoredict)
        for val in next(iter (scoredict.values())):
            obj2 = val
            maxval = 0
            maxkey = None
            for key2 in scoredict:
                value=scoredict[key2][obj2]
                if value>maxval:
                    maxval =value
                    maxkey = key2
                elif value==maxval:
                    temp[obj2].append(key2)
            if maxkey not in max:
                max[maxkey] = obj2
            elif maxkey in max:
                existing = max[maxkey]
                originalValue = scoredict[maxkey][existing]
                if originalValue<maxval:
                    max[maxkey]=obj2
                    if equal:
                        temparr = temp[existing]
                        max[temparr[0]]=existing
                else:
                    if equal:
                        temparr = temp[obj2]
                        max[temparr[0]]=obj2
        for key in scoredict:
            if key not in max:
                diff.append(key)
        return (diff, max)'''

    def findDiff(self, scoredict, equal=False):
        taken1 = []
        taken2 = []
        max = OrderedDict()
        diff=[]
        for i in range(5,-1, -1):
            for key in scoredict:
                if key not in taken1:
                    for key2 in scoredict[key]:
                        if key2 not in taken2:
                            value = scoredict[key][key2]
                            if value==i:
                                max[key] = key2
                                taken1.append(key)
                                taken2.append(key2)
        for key in scoredict:
            if key not in max:
                diff.append(key)
        return (diff, max)


    def getScore(self, larger, smaller):
        scoredict=OrderedDict()
        lengths = [len(x.attributes) for x in larger.values()]
        same = all([x==lengths[0] for x in lengths])
        for key in larger:
            obj1=larger[key]
            scoredict[key] = {}
            obj1key = key
            for key in smaller:
                simscore = 0
                obj2 = smaller[key]
                obj2key = key
                if len(obj1.attributes)==len(obj2.attributes):
                    for key in obj1.attributes:
                        if key in obj2.attributes:
                            if obj1.attributes[key]==obj2.attributes[key]:
                                simscore+=1
                else:
                    simscore=0
                scoredict[obj1key][obj2key] = simscore
        #print(scoredict)
        return scoredict