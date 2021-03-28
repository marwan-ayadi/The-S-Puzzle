from Search_Algorithms import DFS
import re
import math
#initial state
inp = input("Enter the input")
root = []
for i in inp:
    if i.isdigit():
        root.append(int(i))

#root = [1,3,5,4,2,0,7,8,6]
n = int(math.sqrt(len(root)))
for i, val in enumerate(root):
    if val == n*n:
        root[i] = 0
        break
print("The given state is:", root)


#count the number of inversions       
def inv_num(puzzle):
    inv = 0
    for i in range(len(puzzle)-1):
        for j in range(i+1 , len(puzzle)):
            if (( puzzle[i] > puzzle[j]) and puzzle[i] and puzzle[j]):
                inv += 1
    return inv

def solvable(puzzle): #check if initial state puzzle is solvable: number of inversions should be even.
    inv_counter = inv_num(puzzle)
    if (inv_counter %2 ==0):
        return True
    return False


from time import time

if solvable(root):
          
    DFS_solution = DFS(root, n)
#    DFS_time = time() - time2
    print('DFS Solution is ', DFS_solution[0])
    print('Search Path is ', DFS_solution[1])
#    print('DFS Time:', DFS_time, "\n")
    with open("DFS.txt","w") as f:
        f.write("Solution path is : ")
        f.write(str(DFS_solution[0]) + "\n")
        f.write("Search path is : ")
        f.write(str(DFS_solution[1]))
    
else:
    print("Not solvable")
    with open("DFS.txt","w") as f:
        f.write("Solution path is : no solution\n")
        f.write("Search path is : no solution")



     
