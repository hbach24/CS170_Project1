import heapq
import queue
import copy
'''
Problem space:
Operators: move blank left, right, up, or down

'''
#GOOD REFERENCE: SLide 24 & 25 for Week 1 Heuristic Search Slides
default = [[1, 2, 3], [5, 0, 6], [4, 7, 8]]  #depth = 4 according to project instructions
goal = [[1, 2, 3], [4, 5, 6], [7, 8 , 0]]
N = 3 #size of NxN matrix
#the DEPTH of the tree at which we find a solution is the COST for that solution (Blind Search Part 1 Slide 28)

class Node:
     def __init__(self,state,h,g,f):
       self.state = state
       self.h = h #h should be set to 0 for Uniform Cost Search
       self.g = g #depth of the node
       self.f = self.h + self.g
       self.children = []

def main():
    print("Welcome to Hannah Bach's 8-Puzzle Solver!\n")
    choice = input("Enter '1' to use a default puzzle, or '2' to create your own.\n");
    if choice == '1':
        problem = defaultPuzzle()
        
    if choice == '2':
        problem = createPuzzle()
    
    print("\nSelect the algorithm to solve your puzzle with: ")
    choice = input("    Enter '1' for Uniform Cost Search.\n    Enter '2' for A* with the Misplaced Tile heuristic.\n    Enter '3' for A* with the Manhattan Distance heuristic.\n")
    if(choice == '1'):
        # UniformCostSearch()
        root = Node(problem, 0, 0, 0)
        UniformCostSearch(root)
    if(choice == '2'):
        misplaced()
    if(choice == '3'):
        manhattan()


def defaultPuzzle():
    #initialize puzzle
    print("\nDefault Puzzle: ")
    puzzle = default
    print(puzzle)
    return puzzle

def createPuzzle():
    ##referred to https://www.geeksforgeeks.org/take-matrix-input-from-user-in-python/ for help creating the puzzle
    print("\nTo create your puzzle, please input the number of each tile row-wise. Make sure to press 'enter' after inputting each number.")
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


def moveUp(currNode, blankRow, blankCol):
    childNode = copy.deepcopy(currNode)
    childNode.state[blankRow][blankCol] = currNode.state[blankRow-1][blankCol]
    childNode.state[blankRow-1][blankCol] = 0
    childNode.g = currNode.g + 1
    childNode.h = 0; #change this later
    childNode.f = childNode.g + childNode.h
    # print("NEW CHILDNODE: ", childNode.state, childNode.g, childNode.h, childNode.f)
    return childNode
    

def expand(currNode):
    #find the blank space/zero 
    for i in range(N):
        for j in range(N):
            if(currNode.state[i][j] == 0):
                blankRow = i 
                blankCol = j
                print("Row, Col: ", blankRow, blankCol)

    # (1) expand the node's children by performing the valid operations: move_up, move_down, move_left, move_right
    # (2) add the node's children to the curr node's curr.children list and return its list so we can add it to the queue when we return to UCS
    # NOTE: set the children's g value to 1 (depth = 1)

    #if located at corners, we only perform 2 moves
    if(blankRow != 0):
        print("enter")
        childNode = moveUp(currNode, blankRow, blankCol)
        currNode.children.append(childNode) #append the newly expanded/generated child node after performing a move_up operation to the current node's list of children



    print("exp")

def UniformCostSearch(root):
    nodes = queue.Queue() #queue for all the child nodes
    visited = []
    print("ROOT", root.state) 

    # heapq.heappush(nodes, root) 
    nodes.put(root)
    while(1):
       
        if(nodes.qsize() == 0):
            print("Failed to find the solution.")
            return False
        currNode = nodes.get()
        if(checkGoal(currNode)):
            # print("SIZE", nodes.qsize(), currNode)
            print("Goal found!")
            return currNode;
        else:
            if(currNode.state not in visited):
                expand(currNode)
                print(currNode.state)
                visited.append(currNode.state) #add currNode's state to visited list so we don't expand it again
                print("EXPAND currNode's children and add them to the queue") 
        # print("visited", visited)
    
    return True; 
        #TODO: https://stackoverflow.com/questions/71877490/checking-already-visited-states-in-a-solution-for-8-puzzle-problem
        
#when expanding a node, only add children nodes that haven't been visited yet

def misplaced():
    print("A* with the Misplaced Tile heuristic")

def manhattan():
    print("A* with the Manhattan Distance heuristic")

def checkGoal(currNode):
    #TODO: check if the node passed in here is equivalent to the goal state
    if(currNode.state == goal):
        print("curr:", currNode.state)
        print("goal:", goal)
        return 1
    else:
        return 0 

if __name__ == '__main__':
    main()