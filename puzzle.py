import heapq
'''
Problem space:
Operators: move blank left, right, up, or down

'''
#GOOD REFERENCE: SLide 24 & 25 for Week 1 Heuristic Search Slides
default = [[1, 2, 3], [5, 0, 6], [4, 7, 8]] 
goal = [[1, 2, 3], [4, 5, 6], [7, 8 , 0]]
#the DEPTH of the tree at which we find a solution is the COST for that solution (Blind Search Part 1 Slide 28)

class Node:
     def __init__(self,state,h,g,f):
       self.state = state
       self.h = h #h should be set to 0 for Uniform Cost Search
       self.g = g #depth of the node
       self.f = self.h + self.g

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
        generalSearch(root)
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

    for i in range(3):
        row = []
        for j in range(3):
            tile = int(input())
            row.append(tile)
        newPuzzle.append(row)
    print("Your newly created puzzle: ")
    print(newPuzzle)
    return newPuzzle

def generalSearch(root):
    nodes = [] #queue for all the child nodes
    print("ROOT", root.state)
    heapq.heappush(nodes, (root.f, root)) 
    while(1):
        if(len(nodes) == 0):
            print("Failed to find the solution.")
            return False
        currNode = heapq.heappop(nodes) 
        # print(currNode, currNode[0], currNode[1].state)
        if(checkGoal(currNode[1].state)):
            return currNode[1].state;
        else:
            print("EXPAND currNode's children and add them to the priority queue")
        return True;
        

def expand():
    print("expand")

def UniformCostSearch():
    print("UCS")

def misplaced():
    print("A* with the Misplaced Tile heuristic")

def manhattan():
    print("A* with the Manhattan Distance heuristic")

def checkGoal(currNode):
    #TODO: check if the node passed in here is equivalent to the goal state






if __name__ == '__main__':
    main()