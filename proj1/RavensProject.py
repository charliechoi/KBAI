# DO NOT MODIFY THIS FILE.
#
# Any modifications to this file will not be used when grading your project.
# If you have any questions, please email the TAs.
#
#

import os
import sys
from Agent import Agent
from ProblemSet import ProblemSet
import numpy as np
import sys, traceback

# The main driver file for Project2. You may edit this file to change which
# problems your Agent addresses while debugging and designing, but you should
# not depend on changes to this file for final execution of your project. Your
# project will be graded using our own version of this file.
def main():
    sets=[] # The variable 'sets' stores multiple problem sets.
            # Each problem set comes from a different folder in /Problems/
            # Additional sets of problems will be used when grading projects.
            # You may also write your own problems.

    r = open("Problems" + os.sep + "ProblemSetListTemp.txt")    # ProblemSetList.txt lists the sets to solve.
    line = getNextLine(r)                                   # Sets will be solved in the order they appear in the file.
    while not line=="":                                     # You may modify ProblemSetList.txt for design and debugging.
        sets.append(ProblemSet(line))                       # We will use a fresh copy of all problem sets when grading.
        line=getNextLine(r)                                 # We will also use some problem sets not given in advance.

    # Initializing problem-solving agent from Agent.java
    agent=Agent()   # Your agent will be initialized with its default constructor.
                    # You may modify the default constructor in Agent.java

    # Running agent against each problem set
    results=open("ProblemResults.csv","w")      # Results will be written to ProblemResults.csv.
                                                # Note that each run of the program will overwrite the previous results.
                                                # Do not write anything else to ProblemResults.txt during execution of the program.
    setResults=open("SetResults.csv","w")       # Set-level summaries will be written to SetResults.csv.
    results.write("Problem,Correct Confidence\n")
    setResults.write("Set,Sum Correct Confidence\n")
    for set in sets:
        sum_correct_comfidence = 0
        for problem in set.problems:   # Your agent will solve one problem at a time.
            try:
                problem.setAnswerReceived(agent.Solve(problem))     # The problem will be passed to your agent as a RavensProblem object as a parameter to the Solve method
                                                                    # Your agent should return its answer at the conclusion of the execution of Solve.
                                                                    # Note that if your agent makes use of RavensProblem.check to check its answer, the answer passed to check() will be used.
                                                                    # Your agent cannot change its answer once it has checked its answer.
             

                correct_comfidence = 0
                if type(problem.givenAnswer) is list:
                    answer = problem.givenAnswer
                    if len(answer) >= problem.correctAnswer:
                        if sum(answer) > 1:
                            sum_answer = float(sum(answer))
                            answer = [i/sum_answer for i in answer]            
                        correct_comfidence = answer[problem.correctAnswer-1]
                sum_correct_comfidence += correct_comfidence
                result=problem.name + "," + str(correct_comfidence)
                results.write("%s\n" % result)
            except Exception as e:
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                print("*** print_tb:")
                traceback.print_tb(exceptionTraceback, limit=1, file=sys.stdout)
                print("*** print_exception:")
                traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback,
                                          limit=2, file=sys.stdout)
                print("*** print_exc:")
                traceback.print_exc()
                print("*** format_exc, first and last line:")
                formatted_lines = traceback.format_exc().splitlines()
                print(formatted_lines[0])
                print(formatted_lines[-1])
                print("*** format_exception:")
                print(repr(traceback.format_exception(exceptionType, exceptionValue,
                                                      exceptionTraceback)))
                print("*** extract_tb:")
                print(repr(traceback.extract_tb(exceptionTraceback)))
                print("*** format_tb:")
                print(repr(traceback.format_tb(exceptionTraceback)))
                #print("*** tb_lineno:", traceback.tb_lineno(exceptionTraceback))'''
                print("Error encountered in " + problem.name + ":")
                print(sys.exc_info()[0])
                #result=problem.name + "," + str(problem.givenAnswer) + ",Error,"
                #results.write("%s\n" % result)
        setResult=set.name + "," + str(sum_correct_comfidence)
        setResults.write("%s\n" % setResult)
    results.close()
    setResults.close()

def getNextLine(r):
    return r.readline().rstrip()

if __name__ == "__main__":
    main()