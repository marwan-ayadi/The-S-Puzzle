class State:
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0] 
    
    def __init__(self, state, parent, direction, depth, cost, n):
        self.state = state
        self.parent = parent
        self.direction = direction
        self.depth = depth
        self.goal = [(i+1) for i in range(n*n-1)]
        self.goal.append(0)
        if parent:
            self.cost = parent.cost + cost
        else:
            self.cost = cost


    def test(self): #check if the given state is goal
        if self.state == self.goal:
            return True
        return False                   


    @staticmethod
    
    #this would remove illegal moves for a given state
    def available_moves(x,n): 
        moves = ['Left', 'Right', 'Up', 'Down']
        if x % n == 0:
            moves.remove('Left')
        if x % n == n-1:
            moves.remove('Right')
        if x - n < 0:
            moves.remove('Up')
        if x + n > n*n - 1:
            moves.remove('Down')

        return moves

    #produces children of a given state
    def expand(self , n):
        print(self.state)
        x = self.state.index(0)
        moves = self.available_moves(x,n)
        
        children = []
        for direction in moves:
            temp = self.state.copy()
            if direction == 'Left':
                temp[x], temp[x - 1] = temp[x - 1], temp[x]
            elif direction == 'Right':
                temp[x], temp[x + 1] = temp[x + 1], temp[x]
            elif direction == 'Up':
                temp[x], temp[x - n] = temp[x - n], temp[x]
            elif direction == 'Down':
                temp[x], temp[x + n] = temp[x + n], temp[x]
        
        
            children.append(State(temp, self, direction, self.depth + 1, 1, n)) #depth should be changed as children are produced
        return children

    
    #gets the given state and returns it's direction + it's parent's direction till there is no parent
    def solution(self):
        solution = []
        solution.append(self.direction)
        path = self
        while path.parent != None:
            path = path.parent
            solution.append(path.direction)
        solution = solution[:-1]
        solution.reverse()
#        print("solution is ", solution)
        return solution
         
