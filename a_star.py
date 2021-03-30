from queue import PriorityQueue
import math 

class Node():

    def __init__(self, parent=None, state=None):
        self.parent = parent
        self.state = state

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.state == other.state
    def __lt__(self, other):
        return self.f < other.f
    def __le__(self, other):
        return self.f <= other.f
    def __gt__(self, other):
        return self.f > other.f
    def __ge__(self, other):
        return self.f >= other.f


def use_heuristic(heuristic: str, node: Node, target_puzzle: list): 
    g = 0 
    h = 0 
    f = 0
   
    if(heuristic =="manhattan"):
        if(node.parent is not None):
            g = node.parent.g+1
        else:
            g = 0
        h = modified_manhattan_heuristic(node.state, target_puzzle)
        f = g+h
        return g ,h,f
    else:
        if(node.parent is not None):
            g = node.parent.g+1
        else:
            g = 0
        h = hamming_distance_heuristic(node.state, target_puzzle)
        f = g+h
        return g ,h,f
        
def tuple_of_tuple_to_list(tup:tuple)->list:
    return list(sum(tup, ()))

def hamming_distance_heuristic(puzzle:list, target_puzzle:list)->int:
    i=0
    score = 0
    for tile in target_puzzle:
        if(puzzle[i]!=tile):
            score+=1
        i+=1
    return score

def modified_manhattan_heuristic(puzzle:list, target_puzzle:list)->int:
    n =math.sqrt(len(puzzle))
    i=0
    score = 0
    linear_conflict = 0
    for tile in puzzle:
        index_1 = target_puzzle.index(tile)
        index_2 = target_puzzle.index(puzzle[tile-1])

        x_1 = math.floor(i/n)
        y_1 = i%n
        x_index_1 =math.floor(index_1/n) 
        y_index_1 =index_1%n

        x_2 = math.floor((tile-1)/n)
        y_2 = (tile-1)%n 
        x_index_2 =math.floor(index_2/n)
        y_index_2 =index_2%n

        if(i!=index_1):
            s1 = abs(x_index_1-x_1)+abs(y_index_1-y_1)
            s2 = abs(x_index_2-x_2)+abs(y_index_2-y_2)
            if ((x_1 == x_2 and x_index_1== x_index_2) or (y_1 == y_2 and y_index_1 == y_index_2) ):
                linear_conflict+=1
            score+=abs(s1-s2)
        i+=1
    return score+linear_conflict/2 

def get_children_nodes(node:Node, n, h)-> list:
    i = 0
    children=[]
   
    for e in node.state:
        if(i<(len(node.state)-1) and (i+1)%n!=0):
            children.append(Node(node,swap_tiles(node.state, i, i+1, n)))
        if(i<(len(node.state)-n)):
            children.append(Node(node,swap_tiles(node.state, i, i+n, n)))
        i+=1 
    return children

def swap_tiles(puzzle_list: list, index1: int, index2: int, n: int) -> list:  
   
    temp_puzzle = puzzle_list.copy()                                                                               
    temp_puzzle[index1], temp_puzzle[index2] = temp_puzzle[index2], temp_puzzle[index1]

    return temp_puzzle

def list_to_tuple_of_n_tuples(lst:list, n) -> tuple:
    sub = []
    res = []
    i=0
    for l in lst:
        if((i+1) % n == 0):
            sub.append(l)
            res.append(tuple(sub))
            sub=[]
        else:
            sub.append(l)    
        i+=1
    return tuple(res)
 
def a_star(start, target, n, heuristic):
    start_puzzle = tuple_of_tuple_to_list(start)
    target_puzzle = tuple_of_tuple_to_list(target)
   
    open_list=PriorityQueue()
    closed_list={}

    start_node = Node(None, start_puzzle)
    start_node.g, start_node.h,start_node.f = use_heuristic(heuristic, start_node, target_puzzle)
    end_node = Node(None, target_puzzle)
    end_node.g = end_node.h = end_node.f = 0

    open_list.put(start_node)
    
    while not open_list.empty():
        current_node =open_list.get()                                   
        closed_list[tuple(current_node.state)] = current_node
       
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current)
                current = current.parent
            return(path[::-1])
        children = get_children_nodes(current_node,n,heuristic)
        for child in children:
            previous_node = closed_list.get(tuple(child.state),Node(None,None))
            if previous_node != Node(None,None) and child.g >= previous_node.g:
                continue    
            child.g, child.h, child.f = use_heuristic(heuristic, child, target_puzzle)
            open_list.put(child)
    
def main():
    start_puzzle = ((5, 2, 8, 11), (9,3,7), (1,4,6))
    # start_puzzle = ((1,5,3,2),(4,6,9,8),(7,10,16,15),(11,12,13,14))
    target_puzzle = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
    # target_puzzle = ((1, 2, 3, 4), (5,6,7,8), (9,10,11,12),(13,14,15,16))
    print("mahattan")
    path = a_star(start_puzzle, target_puzzle, len(start_puzzle),"manhattan")
    print(f"solution length ----------------------------->: {len(path)}")   
    for node in path:
        print(f"f ----------------------------->: {node.h}")   
        for row in list_to_tuple_of_n_tuples(node.state,len(start_puzzle)):
            print(row)
        print("\n")
    print("hamming")
    path = a_star(start_puzzle, target_puzzle, len(start_puzzle),"hamming")
    print(f"solution length ----------------------------->: {len(path)}")  
    for node in path:
        print(f"f ----------------------------->: {node.h}")   
        for row in list_to_tuple_of_n_tuples(node.state,len(start_puzzle)):
            print(row)
        print("\n")
        
if __name__ == '__main__':
   main()