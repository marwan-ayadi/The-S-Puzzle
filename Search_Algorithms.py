from State import State
from queue import PriorityQueue
from queue import Queue
from queue import LifoQueue
import time

#Depth-first Search with limited depth
def DFS(given_state , n): 
    root = State(given_state, None, None, 0, 0, n)
    start = time.time()
    if root.test():
        return root.solution()
    frontier = LifoQueue()
    frontier.put(root)
    explored = []
    ans = []
    while not(frontier.empty()):
        current_node = frontier.get()
        max_depth = current_node.depth #current depth
#        for i, val in enumerate(current_node.state):
#            if val == 0:
#                current_node.state[i] = n*n
        explored.append(current_node.state)
        
#        if max_depth == 30:
#            continue #go to the next branch

        children = current_node.expand(n)
        for child in children:
            if child.state not in explored:
                if child.test():
                    return child.solution(), explored
                frontier.put(child)
        if time.time() - start > 60:
            return "no solution", "no solution"
        
    return (("Couldn't find solution in the limited depth."), len(explored))
