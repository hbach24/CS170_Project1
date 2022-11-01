import queue
import copy
import time
'''
Problem space:
Operators: move blank left, right, up, or down

'''
#depth = 8
default = [[1, 3, 6],
           [5, 0, 2],
           [4, 7, 8]]

goal = [[1, 2, 3],
        [4, 5, 6],
        [7, 8 ,0]]

# default = [[1, 2, 3], [5, 0, 6], [4, 7, 8]] #depth=4
# default = [[1, 3, 6], [5, 0, 7], [4, 8, 2]] #depth=12
# default = [[1, 6, 7], [5, 0, 3], [4, 8, 2]] #depth=16
# default = [[7, 1, 2], [4, 8, 5], [6, 3, 0]] #depth=20
# default = [[0, 7, 2], [4, 6, 1], [3, 5, 8]] # depth=24

N = len(default) #size of NxN matrix
# print("Size N:", N);

nodes = queue.PriorityQueue() #initialize priority queue here so we can add children nodes to the queue

class Node:
     def __init__(self,state,h,g,f):
       self.state = state
       self.h = 0 #h should be set to 0 for Uniform Cost Search
       self.g = 0 #depth of the node
       self.f = self.h + self.g
       
     def __lt__(self, other): #REFERENCE: https://stackoverflow.com/questions/71201262/problem-using-priorityqueue-with-objects-python
        #building a min heap priority queue comparing the cost
        return self.f < other.f 

def main():
    
    print("Welcome to Hannah Bach's 8-Puzzle Solver!\n")
    choice = input("Enter '1' to use a default puzzle, or '2' to create your own.\n");
    if choice == '1':
        problem = defaultPuzzle()
        
    if choice == '2':
        problem = createPuzzle()
    
    print("\nSelect the algorithm to solve your puzzle with: ")
    algo = input("    Enter '1' for Uniform Cost Search.\n    Enter '2' for A* with the Misplaced Tile heuristic.\n    Enter '3' for A* with the Manhattan Distance heuristic.\n")
    root = Node(problem, 0, 0, 0)
    if(algo == '1'):
        algoName = "Uniform Cost Search"
    if(algo == '2'):
        algoName = "A* with the Misplaced Tile heuristic"
    if(algo == '3'):
        algoName = "A* with the Manhattan Distance heuristic"
    
    duration = time.time()
    generalSearch(root, algo, algoName)
    t1 = time.time() - duration
    print("Time elapsed: ", t1)


def defaultPuzzle():
    #initialize puzzle
    print("\nDefault Puzzle: ")
    puzzle = default
    print(puzzle)
    return puzzle

def createPuzzle():
    #referred to https://www.geeksforgeeks.org/take-matrix-input-from-user-in-python/ for help creating the puzzle
    print("\nTo create your puzzle, please input the number of each tile row-wise. Make sure to press 'enter' after inputting each number. Use a zero for the blank tile.")
    newPuzzle = []

    for i in range(N):
        row = []
        for j in range(N):
            tile = int(input())
            row.append(tile)
        newPuzzle.append(row)
    print("Your newly created puzzle: ")
    print(newPuzzle)
    return newPuzzle


def moveUp(currNode, blankRow, blankCol, algo):
    #REFERENCE: https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/
    childNode = copy.deepcopy(currNode)
    childNode.state[blankRow][blankCol] = currNode.state[blankRow-1][blankCol]
    childNode.state[blankRow-1][blankCol] = 0
    childNode.g = currNode.g + 1
    childNode.h = 0 #default heuristic h = 0 if algorithm chosen is Uniform Cost Search (i.e. algo == '1')
    print("New child node after moving up: ", childNode.state,  " Current depth:", childNode.g)

    #check which algorithm to use
    if(algo == '2'):
        #call misplaced() to compute the # of misplaced tiles compared to the goal state
        childNode.h = misplaced(childNode.state)
        print("Misplaced count:", childNode.h, "\n")

    if(algo == '3'):
        childNode.h = manhattan(childNode.state)
        print("Manhattan distance:", childNode.h, "\n")

    childNode.f = childNode.g + childNode.h
    
    return childNode
    
def moveDown(currNode, blankRow, blankCol, algo):
    childNode = copy.deepcopy(currNode)
    childNode.state[blankRow][blankCol] = currNode.state[blankRow+1][blankCol]
    childNode.state[blankRow+1][blankCol] = 0
    childNode.g = currNode.g + 1
    childNode.h = 0 #default heuristic h = 0 if algorithm chosen is Uniform Cost Search (i.e. algo == '1')
    print("New child node after moving down: ", childNode.state, " Current depth:", childNode.g)

    if(algo == '2'):
        #call misplaced() to compute the # of misplaced tiles compared to the goal state
        childNode.h = misplaced(childNode.state)
        print("Misplaced count:", childNode.h, "\n")

    if(algo == '3'):
        childNode.h = manhattan(childNode.state)
        print("Manhattan distance:", childNode.h, "\n")

    childNode.f = childNode.g + childNode.h
    
    return childNode

def moveLeft(currNode, blankRow, blankCol, algo):
    childNode = copy.deepcopy(currNode)
    childNode.state[blankRow][blankCol] = currNode.state[blankRow][blankCol-1]
    childNode.state[blankRow][blankCol-1] = 0
    childNode.g = currNode.g + 1
    childNode.h = 0 #default heuristic h = 0 if algorithm chosen is Uniform Cost Search (i.e. algo == '1')
    print("New child node after moving left: ", childNode.state,  " Current depth:", childNode.g)

    if(algo == '2'):
        #call misplaced() to compute the # of misplaced tiles compared to the goal state
        childNode.h = misplaced(childNode.state)
        print("Misplaced count:", childNode.h, "\n")

    if(algo == '3'):
        #call manhattan() to compute the manhattan distance (i.e. the total sum of each of the tile's distances from its current to goal position; ignoring the blank tile)
        childNode.h = manhattan(childNode.state)
        print("Manhattan distance:", childNode.h, "\n")

    childNode.f = childNode.g + childNode.h
    return childNode

def moveRight(currNode, blankRow, blankCol, algo):
    childNode = copy.deepcopy(currNode)
    childNode.state[blankRow][blankCol] = currNode.state[blankRow][blankCol+1]
    childNode.state[blankRow][blankCol+1] = 0
    childNode.g = currNode.g + 1
    childNode.h = 0 #default heuristic h = 0 if algorithm chosen is Uniform Cost Search (i.e. algo == '1')
    print("New child node after moving right: ", childNode.state,  " Current depth:", childNode.g)

    if(algo == '2'):
        #call misplaced() to compute the # of misplaced tiles compared to the goal state
        childNode.h = misplaced(childNode.state)
        print("Misplaced count:", childNode.h, "\n")

    if(algo == '3'):
        childNode.h = manhattan(childNode.state)
        print("Manhattan distance:", childNode.h, "\n")

    childNode.f = childNode.g + childNode.h
    return childNode


def expand(currNode, algo):
    #find the blank space/zero 
    for i in range(N):
        for j in range(N):
            if(currNode.state[i][j] == 0):
                blankRow = i 
                blankCol = j

    # (1) expand the node's children by performing the valid operations: move_up, move_down, move_left, move_right
    # (2) add the current node's children to the queue 'nodes'
    # NOTE: set the children's g value to (parent's node's depth + 1)

    #if 0 is not located on the first row, we can move up
    if(blankRow != 0):
        # print("moveUp")
        childNode = moveUp(currNode, blankRow, blankCol, algo)
        nodes.put(childNode)
    
    #if 0 is not in the last row, we can move down
    if(blankRow < N-1):
        # print("moveDown")
        childNode = moveDown(currNode, blankRow, blankCol, algo)
        nodes.put(childNode)

    #if 0 is not located in the first column, we can move left
    if(blankCol > 0):
        # print("moveLeft")
        childNode = moveLeft(currNode, blankRow, blankCol, algo)
        nodes.put(childNode)
    
    #if 0 is not located in the last column, we can move right
    if(blankCol < N-1):
        # print("moveRight")
        childNode = moveRight(currNode, blankRow, blankCol, algo)
        nodes.put(childNode)

def generalSearch(root, algo, algoName):
    expandCount = 0
    maxQsize = 0
    visited = []
    print("ROOT START:", root.state) 

    nodes.put(root)
    
    while(1):
        if(maxQsize < nodes.qsize()):
            maxQsize = nodes.qsize()
        if(nodes.qsize() == 0):
            print("Failed to find the solution.")
            return False
        currNode = nodes.get()

        if(checkGoal(currNode)):
            print("\t\t\tGOAL!!!\n")
            print("\tPuzzle", root.state, "solved!\n")
     
            print("Goal found at DEPTH", currNode.g, "using", algoName)   
            print("\t\t", currNode.state)
            print("\nExpanded a total of", expandCount, "nodes.") 
            print("Maximum queue size was", maxQsize, "nodes.")
            return currNode;
            
        else:
            if(currNode.state not in visited): #when expanding a node, only add children nodes that haven't been visited yet
                if(algo == '2'):
                    heur = misplaced(currNode.state)
                    print("The best state to expand with a g(n) =", currNode.g, ", h(n) =", heur, ", and cost", currNode.g + heur ,  "is:")
                elif(algo == '3'):
                    heur = manhattan(currNode.state)
                    print("The best state to expand with a g(n) =", currNode.g, ", h(n) =", heur, ", and cost", currNode.g + heur ,  "is:")
                else:
                    print("The best state to expand with a g(n) =", currNode.g, ", h(n) = 0 and cost", currNode.g,  "is:")

                print("Expanding node " , currNode.state, "at depth", currNode.g, "\n")  
                expandCount += 1;
                expand(currNode, algo)
                print("\n---------------------------------------------------------------------------------------\n")
                visited.append(currNode.state) #add currNode's state to visited list so we don't expand it again

def misplaced(currState):
    #calculates the number of misplaced tiles heuristic
    misCount = 0
    for i in range(N):
        for j in range(N):
            if((currState[i][j] != 0) and (goal[i][j] != currState[i][j])): #don't count the blank tile
                misCount+=1;
    return misCount

#REFERENCE: #https://stackoverflow.com/questions/19770087/can-somebody-explain-in-manhattan-dstance-for-the-8-puzzle-in-java-for-me?noredirect=1&lq=1
def manhattan(currState):
    result = 0;
    for i in range(N): 
        for j in range(N): 
            if (currState[i][j] != 0):  # ignore blank tile
                    expRow = (currState[i][j] - 1) // N; # expected row value (floor division)
                    expCol = (currState[i][j] - 1) % N; # expected column value
                    distRow = i - expRow; # row distance to goal/expected value
                    distCol = j - expCol; # col distance to goal/expected value
                    result = result + abs(distRow) + abs(distCol) # adds up the row and col distances
    return result

def checkGoal(currNode):
    #checks if the current node passed in here is equivalent to the goal state
    if(currNode.state == goal):
        # print("curr:", currNode.state)
        # print("goal:", goal)
        return 1
    else:
        return 0 #returns 0 or false if current node is not the goal state/node

if __name__ == '__main__':
    main()