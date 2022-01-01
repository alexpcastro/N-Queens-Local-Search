# Author: Alexander Castro
# Description: Local search to solve n queens problem
#

import random
import copy

nqueen = 8
random.seed()

#generate a random nqueen
def randomqueen():
    '''Generate a random -queenboard position, returned as list'''
    b = [0]*nqueen
    for i in range(0,nqueen):
        b[i]= random.randint(0,nqueen-1)
    return b


#Expand the next level of the search tree by moving all queens in their column
def expandqueen(s):
    '''Generate a list of all n queens boards made by moving 1 queen in b'''
    expandList = []
    for i in range(0,nqueen):     # for each queen col
        newS = copy.deepcopy(s)       # make a new state from this one
        for j in range(0,nqueen): # all the rows for a Q
            if (j != newS[i]):
                newS[i]=j
                expandList.append(newS)
    return expandList

def conflict(x1,y1,x2,y2):
    '''Determine if conflict exists between two queens using their coordinates (x1,y1) and (x2,y2)
       Possible conflict types:
         horizontal line: y1 == y2
         vertical line: x1 == x2
         positive slope diagonal: y2 - y1 == x2 - x1
         negative slope diagonal: y2 - y1 == x1 - x2'''
    dy = y2 - y1
    dx = x2 - x1
    if dx == 0 or dy == 0 or dx == dy or dx == -dy:
        return True
    return False

def scorequeen(state,nqueen):
    '''Calculate number of conflicting queen pairs in board
       Considers the queen positions as x,y coordinates to simplify conflict resolution
       Checks columns from left to right
    '''
    score = 0

    for column in range(0,nqueen): # iterate over all columns
        #print('\nSelected column',column)
        if column+1 == nqueen: # right-most column reached
            break # no more matches possible
        #print('Queen position: (',column,',',state[column],')')
        #print('Checking columns', column+1,'to',nqueen-1,'for queens')
        for right_column in range(column+1,nqueen): # loop through columns on right of selected column
            #print('  Queen found: (',right_column,',',state[right_column],')')
            if conflict(column,state[column],right_column,state[right_column]):
                score += 1
    return score

# do a local beam search for nQ solution
def doLocalBeamNQ(k):
    '''Do a local search for NQ solution
       Initially: k random states generated
       Then: determine all successors of k states
       If any successor is a goal state we are finished
       Else select k best successors and repeat'''

    sfringe=[]
    states=[]
    # generate k random states
    for i in range(k):
        states.append(randomqueen()) # add a random state
        sfringe.append((states[i],scorequeen(states[i],nqueen))) # score the state

    #print('Start states:', states)
    #print('Scored start states:',sfringe)
    sfringe = sorted(sfringe,key=lambda node: node[1]) # sort by score ascending
    #print('Scored sorted start states:',sfringe)
    best = sfringe[0]
    bestScore,lastBestScore = best[1],best[1]+1
    iter=0

    # for each state, run the while loop checking successors and expanding them
    while (bestScore>0 and lastBestScore>bestScore):
        fringe = []

        for state in sfringe: # iterate over our k states that are now scored and sorted
            for expanded_state in expandqueen(state[0]): # expand each of k states
                score = scorequeen(expanded_state,nqueen) # score resulting expansion
                fringe.append((expanded_state,score)) # add expanded state and score to new fringe
        sfringe = sorted(fringe,key=lambda node: node[1]) # sort fringe of expanded states by score ascending
        #print('expanded sfringe',sfringe)
        best = sfringe[0]
        lastBestScore=bestScore
        bestScore=best[1]
        iter += 1

        # trim sfringe to k successors only
        sfringe = sfringe[:k]
        #print('trimmed expanded sfringe',sfringe)
        print("\nIter ",iter," fringe ",len(fringe)," bscore ",bestScore,lastBestScore,"\n")

    # To simplify reporting for the assignment, the program does not return the winning state but instead a 1 if it is a global optimum and 0 if it is a local optimum
    if bestScore==0: # Global Optimum is best[0]
        return 1 # solution found
    else: # Local Optimum is best[0]
        return 0

test_k_values = [1,10,50] #,10,50] # list of test k values

test_run_count = 50 # number of runs for each k to obtain an average score
test_runs_total_score = [0]*len(test_k_values)

num_nqueen_problems = 100 # number of desired test runs for each k value

for key,k in enumerate(test_k_values): # iterate over each test k test_k_values
    total_run_score = 0
    for runs in range(1,test_run_count+1): # count runs from 1 to total for proper count for later divison
        for i in range(num_nqueen_problems): # run local beam search num_nqueen_problems times for loop k value
            total_run_score += doLocalBeamNQ(k)
    test_runs_total_score[key] += total_run_score

for key,k in enumerate(test_k_values):
    print('K:', k, 'Num Queen Problems', num_nqueen_problems,'Runs:',test_run_count, 'Total Run Score:', test_runs_total_score[key], 'Average score:',test_runs_total_score[key]/test_run_count)
