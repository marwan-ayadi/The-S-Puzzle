from queue import PriorityQueue
import argparse
import time
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
   
    if(heuristic =="h1"):
        if(node.parent is not None):
            g = node.parent.g+1
        else:
            g = 0
        h = modified_manhattan_heuristic(node.state, target_puzzle)
        f = g+h
        return g ,h,f

    elif(heuristic =="h2"):
        if(node.parent is not None):
            g = node.parent.g+1
        else:
            g = 0
        h = modified_hamming_distance_heuristic(node.state, target_puzzle)
        f = g+h
        return g ,h,f
        
def tuple_of_tuple_to_list(tup:tuple)->list:
    return list(sum(tup, ()))

def modified_hamming_distance_heuristic(puzzle:list, target_puzzle:list)->int:
    n =int(math.sqrt(len(puzzle)))
    i=0
    score = 0
    diff = 0
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
            diff+=abs(s1-s2)
            score+=1

        i+=1
  
    return round((2*score+diff)/n)

def modified_manhattan_heuristic(puzzle:list, target_puzzle:list)->int:
    n =math.sqrt(len(puzzle))
    i=0
    score = 0
    for tile in puzzle:
        x_1 = math.floor(i/n)
        y_1 = i%n
        x_2 = math.floor((tile-1)/n)
        y_2 = (tile-1)%n 
     
        score += abs(x_2 - x_1)+ abs(y_2 - y_1)
        i+=1
    return score/2

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
 
def a_star(start_puzzle: list, target_puzzle: list , n, heuristic):
    open_list=PriorityQueue()
    closed_list={}

    start_node = Node(None, start_puzzle)
    start_node.g, start_node.h,start_node.f = use_heuristic(heuristic, start_node, target_puzzle)
    end_node = Node(None, target_puzzle)
    end_node.g = end_node.h = end_node.f = 0

    open_list.put(start_node)
    start_time = time.time()
    search_space = []
    while not open_list.empty():
        
        current_node =open_list.get()                                   
        closed_list[tuple(current_node.state)] = current_node
        search_space.append(current_node.state)
        if current_node == end_node:
            d = open(f"solutions/{heuristic}_search_path.txt", "a")
            for s in search_space:
                d.write(f"{list_to_tuple_of_n_tuples(s,n)}\n")
            d.close()
            total_time = time.time() - start_time
            solution_path = []
            c= current_node
            while c is not None:
                solution_path.append(c)
                c = c.parent
            isAdmissible = True
            for node in solution_path:
                if ((node.g > len(solution_path) and isAdmissible)):
                    isAdmissible = False
            f = open(f"{heuristic}_analysis.txt", "a")
            f.write("\n========================================\n")
            f.write(f"heuristic: \t\t\t {heuristic}\n")
            f.write(f"start puzzle: \t\t\t {list_to_tuple_of_n_tuples(start_puzzle, n)}\n")
            f.write(f"Length of Solution Path: \t {len(solution_path)}\n")
            f.write(f"Length of Search Path: \t\t {len(closed_list)}\n")    
            f.write(f"Excution time (s): \t\t\t {total_time}\n")
            if isAdmissible:
                f.write(f"Optimality \t\t\t IS OPTIMAL \n") 
            else:
                f.write(f"Optimality \t\t\t IS NOT OPTIMAL \n") 
            f.close()
            return(solution_path[::-1])

        total_time = round(time.time() - start_time, 5)
        if total_time > 60:
            f = open(f"{heuristic}_analysis.txt", "a")
            f.write("\n========================================\n")
            f.write(f"heuristic: \t\t\t {heuristic}\n")
            f.write(f"start puzzle: \t\t\t {list_to_tuple_of_n_tuples(start_puzzle, n)}\n")
            f.write("---- No Solution ----\n Time exceeded !! \n")
            f.close()
            return []

        children = get_children_nodes(current_node,n,heuristic)
        for child in children:
            previous_node = closed_list.get(tuple(child.state),Node(None,None))
            if previous_node != Node(None,None) and child.g >= previous_node.g:
                continue    
            child.g, child.h, child.f = use_heuristic(heuristic, child, target_puzzle)
            open_list.put(child)
    
def main(args):
    puzzles = []
    
    f = open(args.path, "r")
    for puzzle_txt in f:
        puzzle = []
        for row_txt in puzzle_txt.split(","):
            puzzle.append(int(row_txt.replace("(","").replace(")","")))
        puzzles.append(puzzle)
    f.close()
    puzzle_number = 0
    for start_puzzle in puzzles:
        puzzle_number+=1
        target_puzzle = []
        n = int(math.sqrt(len(start_puzzle)))
        for i in range(n ** 2):
                target_puzzle.append(i+1) 
        if(puzzle_number == 1):
            open('h1_analysis.txt', 'w').close()
            open('h2_analysis.txt', 'w').close()
            open('solutions/h1_solution_path.txt', 'w').close()
            open('solutions/h1_search_path.txt', 'w').close()
            open('solutions/h2_solution_path.txt', 'w').close()
            open('solutions/h2_search_path.txt', 'w').close()

        print("\n********************************************************************************")
        print(f"Puzzle #{puzzle_number}")
        print("********************************************************************************\n")
       
        path_h1 = a_star(start_puzzle, target_puzzle, n,"h1")
        f1 = open("solutions/h1_solution_path.txt", "a")
        f1.write("\n********************************************************************************\n")
        f1.write(f"Puzzle #{puzzle_number}\n")
        if(len(path_h1) == 0):
            f1.write(f"---- NO SOLUTION ---- \n")
        else:
            f1.write(f"COST =====> {len(path_h1)}\n")
        f1.write("********************************************************************************\n")
        
        for puzzle_state in path_h1:
            f1.write("\n======================================\n")
            f1.write(f"h(n) =====> {puzzle_state.h}\n")
            for row in list_to_tuple_of_n_tuples(puzzle_state.state,n):
                f1.write(f"{row}\n")
        f1.close()
        
        path_h2 = a_star(start_puzzle, target_puzzle, n,"h2")
        f2 = open("solutions/h2_solution_path.txt", "a")
        f2.write("\n********************************************************************************\n")
        f2.write(f"Puzzle #{puzzle_number}\n")
        if(len(path_h2) == 0):
            f2.write(f"---- NO SOLUTION ---- \n")
        else:
            f2.write(f"COST =====> {len(path_h2)}\n")
        f2.write("********************************************************************************\n")
        
        for puzzle_state in path_h2:
            f2.write("\n======================================\n")
            f2.write(f"h(n) =====> {puzzle_state.h}\n")
            for row in list_to_tuple_of_n_tuples(puzzle_state.state,n):
                f2.write(f"{row}\n")
          
        f2.close()
    
       
if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help = "Puzzle(s) path", required = False, default = "puzzles/start_puzzle.txt")
    args = parser.parse_args()
    main(args)