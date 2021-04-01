import numpy as np
import time
from contextlib import redirect_stdout
import random
class node:
            o =  np.array([[0,0,0], [0,0,0],[0,0,0]])
            def __init__(self):    
                    self.o =  np.array([[0,0,0], [0,0,0],[0,0,0]])
      
                    self.Depth=1
                    self.children = []     

            def Set(self,value):
                    self.o=value

            def add_parent(self, p):
                    self.parent=p

            def setDepth(self, d):
                    self.Depth=d
        
            def getDepth(self):
                    return self.Depth
            def ret(self): 
                    return self.o   
            def retparent(self): 
                    return self.parent  


            def retchild(self): 
                    return self.children    
            def IsLeaf(self):
                    if(len(self.children)==0):
       
                                      return True
                    else:
                                      return False
class Node:
            def __init__(self, value):
                    self.value = value
                    self.next = None
class Stack:
            def __init__(self):
                    self.head = Node("head")
                    self.size = 0
            def __str__(self):
                    cur = self.head.next
                    out = ""
                    while cur:
                        out += str(cur.value) + "->"
                        cur = cur.next
                    return out[:-3]
            def getSize(self):
                    return self.size
            def isEmpty(self):
                    return self.size==0
            def peek(self):

                    if self.isEmpty():
                            raise Exception("Peeking from an empty stack")
                    return self.head.next.value
            def push(self, value):
                    node = Node(value)
                    node.next = self.head.next
                    self.head.next = node
                    self.size += 1  
            def pop(self):
                    if self.isEmpty():
                           raise Exception("Popping from an empty stack")
                    remove = self.head.next
                    self.head.next = self.head.next.next
                    self.size -= 1
                    return remove.value
######################################################################################
def DFS(RandomInitialState,index):
    start_time = time.time() 
    def PossibleActions(row,col,dim,State,goal,fr,fc):
       
        right=0
        left=0
        up=0
        down=0
        
        if(row==0 and col==0):
                                right=1
                                left=0
                                up=0
                                down=1
        if(row==0 and col==dim-1):
                                right=0
                                left=1
                                up=0
                                down=1
        
        if(row==dim-1 and col==0):
                                right=1
                                left=0
                                up=1
                                down=0
        if(row==dim-1 and col==dim-1):
                                right=0
                                left=1
                                up=1
                                down=0
                              
        if(row==0 and col>0 and col<dim-1):
                                right=1
                                left=1
                                up=0
                                down=1
                              
        if(col==0 and row>0 and row<dim-1):
                                right=1
                                left=0
                                up=1
                                down=1
        if(row==dim-1 and col>0 and col<dim-1):
                                right=1
                                left=1
                                up=1
                                down=0
                              
        if(col==dim-1 and row>0 and row<dim-1):
                                right=0
                                left=1
                                up=1
                                down=1
                                                    
        if(col>0 and col<dim-1 and row>0 and row<dim-1):
                                right=1
                                left=1
                                up=1
                                down=1
                             
        return [right,left,up,down]
    def examinedcell2(goal,state):
    
        r, c = state.shape
        for i in range(r) :
            for j in range(c):
            
                if(goal[i,j]!=state[i,j]):
                     for x in range(r) :
                             for y in range(c):
                                    if(goal[i,j]==state[x,y]):
                                        return x,y
        return 9999,9999
    def examinedcell(goal,state):
    
        r, c = state.shape
        for i in range(r) :
            for j in range(c):
            
                if(goal[i,j]!=state[i,j]):
                     for x in range(r) :
                             for y in range(c):
                                    if(goal[i,j]==state[x,y]):
                                        return x,y,i,j
        return 9999,9999,9999,9999
    def Done(dcr,dcl,r,c):
        for x in range(len(dcr)):
            if(r==dcr[x] and c==dcl[x]):
                return False
        return True
    Goal =  np.array([[1,2,3], [4,5,6],[7,8,9]])## this is the Goal Node
    o =  RandomInitialState## this is initial Node the root
    root =  np.array([[0,0,0],[0,0,0] ,[0,0,0]])
    OL = Stack()
    OL2 = Stack()
    S = node()
    S.Set(o)
    S.add_parent(S)           
  
   
    CL=[]
    X2=[]
    a=root
    OL.push(S.ret())
    OL2.push(S)
    X2.append(S.ret())
    doneflag=0
    DoneCellsr=[]
    DoneCellsc=[]
    flagr=0
    flagc=0
    dr=0
    dc=0
    i,j,dr,dc=examinedcell(Goal,o)
    
    SolutionPath=[]
    while OL.getSize()>0:
                        X = OL.pop()
                        Xc= OL2.pop()                
                       
                        X2.pop(len(X2)-1)
                     
                        GC=[]

                        if(np.array_equal(X,Goal)):
                                #print("succeded")
                                doneflag=1
                                SolutionPath.append(Xc.ret())
                                checker=0
                                CL.append(X)
                       
                                while(checker==0):
                                    if(np.array_equal(a,o)):
                                        
                                        checker=1
                                        break
                                    else:
                                        checker=0
                                        Xc=Xc.retparent()
                                        a=Xc.ret()
                                        ##print(Xc.getDepth())
                                        SolutionPath.append(a)
                                    
                                break
                        else:
                                CL.append(X)

                                r, c = X.shape
                                
                                if Goal[dr,dc]==X[dr,dc]:
                                    DoneCellsr.append(dr)
                                    DoneCellsc.append(dc)
                                    i,j,dr,dc=examinedcell(Goal,X)
                                else:
                                     i,j=examinedcell2(Goal,X)

                                if(i!=9999 and j!=9999):
                                                       
                                                                    PA=PossibleActions(i,j,r,X,Goal,DoneCellsr,DoneCellsc)
                                                                   
  
                                                                  ##  print(PA)
                                                                               
                                                                    if PA[0]==1:                       
                                                                                           
                                                                                            A=X.copy()
                                                                                          
                                                                                            temp=A[i,j+1]
                                                                                            A[i,j+1]=A[i,j]
                                                                                            A[i,j]=temp
                                                                                            res=Done(DoneCellsr,DoneCellsc,i,j+1)      
                                                                                            
                                                                                            if(res==True):
                                                                                                PA[0]==0
                                                                                                GC.append(A)
                                                                                                         
                                 
                                                                    if PA[1]==1:
                                                                                           
                                                                                            B=X.copy()
                                                                                      
                                                                                            temp=B[i,j-1]
                                                                                            B[i,j-1]=B[i,j]
                                                                                            B[i,j]=temp
                                                                                        
                                                                                            res=Done(DoneCellsr,DoneCellsc,i,j-1)      
                                                                                        
                                                                                            if(res==True):
                                                                                                PA[1]==0
                                                                                                GC.append(B)
                 
                                                                    if PA[2]==1:
                                                                                           
                                                                                            C=X.copy()
                                                                                           
                                                                                            temp=C[i-1,j]
                                                                                            C[i-1,j]=C[i,j]
                                                                                            C[i,j]=temp
                                                                                          
                                                                                            res=Done(DoneCellsr,DoneCellsc,i-1,j)      
                                                                                        
                                                                                            if(res==True):
                                                                                                PA[2]==0
                                                                                                GC.append(C)
             
                                                                    if PA[3]==1:
                                                                                           
                                                                                            D=X.copy() 
                                                                                           
                                                                                            temp=D[i+1,j]
                                                                                            D[i+1,j]=D[i,j]
                                                                                            D[i,j]=temp
                                                                                            
                                                                                            res=Done(DoneCellsr,DoneCellsc,i+1,j)      
                                                                                        
                                                                                            if(res==True):
                                                                                                PA[1]==0
                                                                                                GC.append(D)

                                                                    ##print("After")
                                                                    ##print(PA)               

                                generatedChildren =[]
                                GC.reverse()
                                count=0
                                count2=0
                                s=OL
                                l=0
                                count1=[]
                                count2=0
                                for G in GC:
                                                            for C in CL:
                                             
                                                                       
                                                                    if(np.array_equal(C,G)):
                                                                           
                                                                           count1.append(l)
                                                                            
                                                            for x in X2:
                                             
                                                                       
                                                                   if(np.array_equal(x,G)):
                                                                           
                                                                           count1.append(l)

                                                            l=l+1                                  
                                w=0
                                
                                flag=0
                                for G in GC:
                                            
                                        
                                        for y in count1: 
                                            if y==w:
                                                flag=1
                                                break

                                        if flag==0:
                                            generatedChildren.append(G)
                                        else:
                                            flag=0
                                        
                                            
                                        w=w+1

                                for g in generatedChildren:

                                                                S = node()
                                                                S.Set(g)
                                                                d=Xc.getDepth()
                                                                d=d+1
                                                                S.setDepth(d)
                                                                S.add_parent(Xc)
                                                                OL.push(S.ret())
                                                                X2.append(S.ret())
                                                                OL2.push(S)

    end_time = time.time() 
    tm=end_time-start_time
    SolutionPath.reverse()
    spc=1
    ##output 
    
    if(tm>60):
                    with open('DFS-Solution-Path.'+str(index)+'txt', 'w') as f:
                        with redirect_stdout(f): 
                                      print("no solution")
                    with open('DFS-Search-Path'+str(index)+'.txt', 'w') as f:
                         with redirect_stdout(f):
                                       print("no solution")
                    return 99999,99999 ,99999,tm               
    else:    
                    with open('DFS-Solution-Path'+str(index)+'.txt', 'w') as f:
                        with redirect_stdout(f):            
                                    SolutionPath.reverse()
                                    spc=1
                                    print("DFS Solution Path")
                                    for  sp in SolutionPath:
    
                                                    print("Step:",spc)
                                                    print(sp)
                                                    print("#############")
                                                    spc=spc+1
                
                    with open('DFS-Search-Path'+str(index)+'.txt', 'w') as f:
                         with redirect_stdout(f):                          
                                     print("DFS Search Path")
                                     clc=1
                                     for  cl in CL:
    
                                                print("Step:",clc)
                                                print(cl)
                                                print("#############")
                                                clc=clc+1
                    return clc,spc,spc,tm
######################################################################################                
def IterativeDeepenng(RandomInitialState,index):
    
    def PossibleActions(row,col,dim,State,goal,fr,fc):
       
        right=0
        left=0
        up=0
        down=0
        
        if(row==0 and col==0):
                                right=1
                                left=0
                                up=0
                                down=1
        if(row==0 and col==dim-1):
                                right=0
                                left=1
                                up=0
                                down=1
        
        if(row==dim-1 and col==0):
                                right=1
                                left=0
                                up=1
                                down=0
        if(row==dim-1 and col==dim-1):
                                right=0
                                left=1
                                up=1
                                down=0
                              
        if(row==0 and col>0 and col<dim-1):
                                right=1
                                left=1
                                up=0
                                down=1
                              
        if(col==0 and row>0 and row<dim-1):
                                right=1
                                left=0
                                up=1
                                down=1
        if(row==dim-1 and col>0 and col<dim-1):
                                right=1
                                left=1
                                up=1
                                down=0
                              
        if(col==dim-1 and row>0 and row<dim-1):
                                right=0
                                left=1
                                up=1
                                down=1
                                                    
        if(col>0 and col<dim-1 and row>0 and row<dim-1):
                                right=1
                                left=1
                                up=1
                                down=1
                                       
        return [right,left,up,down]

    def examinedcell2(goal,state):
    
                    r, c = state.shape
                    for i in range(r) :
                             for j in range(c):
            
                                      if(goal[i,j]!=state[i,j]):
                                                     for x in range(r) :
                                                              for y in range(c):
                                                                     if(goal[i,j]==state[x,y]):
                                                                                         return x,y
                    return 9999,9999 
    def examinedcell(goal,state):
    
                    r, c = state.shape
                    for i in range(r) :
                            for j in range(c):
            
                                  if(goal[i,j]!=state[i,j]):
                                                for x in range(r) :
                                                        for y in range(c):
                                                               if(goal[i,j]==state[x,y]):
                                                                                 return x,y,i,j
                    return 9999,9999,9999,9999
    def Done(dcr,dcl,r,c):
                            for x in range(len(dcr)):
                                   if(r==dcr[x] and c==dcl[x]):
                                                         return False
                            return True
    CL=[]    
    ItDeep=1 
    start_time = time.time()
    while(ItDeep!=0):
                ##print("Depth:",ItDeep)
                Goal =  np.array([[1,2,3], [4,5,6],[7,8,9]])## this is the Goal Node
                o =  RandomInitialState## this is initial Node the root              
                root =  np.array([[0,0,0],[0,0,0] ,[0,0,0]])
                OL = Stack()
                OL2 = Stack()
                S = node()
                S.Set(o)
                S.add_parent(S)
                CL=[]
                X2=[]
                a=root
                OL.push(S.ret())
                OL2.push(S)
                X2.append(S.ret())
                doneflag=0
                DoneCellsr=[]
                DoneCellsc=[]
                flagr=0
                flagc=0
                dr=0
                dc=0
                i,j,dr,dc=examinedcell(Goal,o)
    
                SolutionPath=[]
                while OL.getSize()>0:
                        X = OL.pop()
                        Xc= OL2.pop()                
                        
                        X2.pop(len(X2)-1)
                     
                        GC=[]
   
                        if(np.array_equal(X,Goal)):
                               ## print("succeded")
                                doneflag=1
                                SolutionPath.append(Xc.ret())
                                checker=0
                                CL.append(X)
                                while(checker==0):
                                    if(np.array_equal(a,o)):
                                        
                                        checker=1
                                        break
                                    else:
                                        checker=0
                                        Xc=Xc.retparent()
                                        a=Xc.ret()
                                        ##print(Xc.getDepth())
                                        SolutionPath.append(a)
                                    
                                break
                        else:
                                CL.append(X)
                                if  Xc.getDepth()==ItDeep:
                                     continue

                                r, c = X.shape
                                
                                if Goal[dr,dc]==X[dr,dc]:
                                    DoneCellsr.append(dr)
                                    DoneCellsc.append(dc)
                                    i,j,dr,dc=examinedcell(Goal,X)
                                else:
                                     i,j=examinedcell2(Goal,X)

                                if(i!=9999 and j!=9999):
                                                                    PA=PossibleActions(i,j,r,X,Goal,DoneCellsr,DoneCellsc)
         
                                                                    if PA[0]==1:                       
                                                                                           
                                                                                            A=X.copy()
                                                                                          
                                                                                            temp=A[i,j+1]
                                                                                            A[i,j+1]=A[i,j]
                                                                                            A[i,j]=temp
                                                                                            res=Done(DoneCellsr,DoneCellsc,i,j+1)      
                                                                                        
                                                                                            if(res==True):
                                                                                                GC.append(A)
                    
                                                                    if PA[1]==1:
                                                                                           
                                                                                            B=X.copy()
                                                                                      
                                                                                            temp=B[i,j-1]
                                                                                            B[i,j-1]=B[i,j]
                                                                                            B[i,j]=temp
                                                                                        
                                                                                            res=Done(DoneCellsr,DoneCellsc,i,j-1)      
                                                                                        
                                                                                            if(res==True):
                                                                                                GC.append(B)
                   
                                                                    if PA[2]==1:
                                                                                           
                                                                                            C=X.copy()
                                                                                           
                                                                                            temp=C[i-1,j]
                                                                                            C[i-1,j]=C[i,j]
                                                                                            C[i,j]=temp
                                                                                          
                                                                                            res=Done(DoneCellsr,DoneCellsc,i-1,j)      
                                                                                        
                                                                                            if(res==True):
                                                                                                GC.append(C)         
                                                                    if PA[3]==1:
                                                                                           
                                                                                            D=X.copy() 
                                                                                           
                                                                                            temp=D[i+1,j]
                                                                                            D[i+1,j]=D[i,j]
                                                                                            D[i,j]=temp

                                                                                            res=Done(DoneCellsr,DoneCellsc,i+1,j)      
                                                                                        
                                                                                            if(res==True):
                                                                                                GC.append(D)

                                generatedChildren =[]
                                GC.reverse()
                                count=0
                                count2=0
                                s=OL
                                l=0
                                count1=[]
                                count2=0
                                for G in GC:
                                                            for C in CL:                                      
                                                                    if(np.array_equal(C,G)):
                                                                           count1.append(l)          
                                                            for x in X2:
      
                                                                   if(np.array_equal(x,G)):
                                                                           
                                                                           count1.append(l)

                                                            l=l+1                                  
                                w=0
                                
                                flag=0
                                for G in GC:
                                            
                                        for y in count1: 
                                            if y==w:
                                                flag=1
                                                break
                                               
 
                                        if flag==0:
                                            generatedChildren.append(G)
                                        else:
                                            flag=0
                    
                                        w=w+1

                                for g in generatedChildren:
                                                                S = node()
                                                                S.Set(g)
                                                                d=Xc.getDepth()
                                                                d=d+1
                                                                S.setDepth(d)
                                                                S.add_parent(Xc)
                                                                OL.push(S.ret())
                                                                X2.append(S.ret())
                                                                OL2.push(S)
                else:
                  ##  print("Failed")
                    ItDeep=ItDeep+1
                if doneflag==1:    
                    ItDeep=0
                end_time = time.time() 
                tm=end_time-start_time
                ##OUTPUT  FILE
                
                
    if(tm>60):
                    with open('Iterative-Deepening-Solution-Path'+str(index)+'.txt', 'w') as f:
                        with redirect_stdout(f): 
                                      print("no solution")
                    with open('Iterative-Deepening-Search-Path'+str(index)+'.txt', 'w') as f:
                         with redirect_stdout(f):
                                       print("no solution")
                    return 99999,99999 ,99999,tm               
    
    else:    
                    with open('Iterative-Deepening-Solution-Path'+str(index)+'.txt', 'w') as f:
                        with redirect_stdout(f):            
                                    SolutionPath.reverse()
                                    spc=1
                                    print("Iterative Deepening Solution Path")
                                    for  sp in SolutionPath:
    
                                                    print("Step:",spc)
                                                    print(sp)
                                                    print("#############")
                                                    spc=spc+1
                
                    with open('Iterative-Deepening-Search-Path'+str(index)+'.txt', 'w') as f:
                         with redirect_stdout(f):                          
                                     print("Iterative Deepening Search Path")
                                     clc=1
                                     for  cl in CL:
    
                                                print("Step:",clc)
                                                print(cl)
                                                print("#############")
                                                clc=clc+1
                    return clc,spc,spc,tm
#####The Analysis                 
#construct matrix of random numbers                
            
NoSoltot=0 ##No  Solution Total Iterative deep
SearchPtot=0##Search path Total Iterative deep
SolPathtot=0##Sol path Total Iterative deep  
optimalPath=0      
##Number of samples  is 2
for rcount in range(2):
    List=[1,3,2,9,5,6,7,8,4]
                     
    RandomInitialState =  np.array([[0,0,0],[0,0,0] ,[0,0,0]])
    x=0
    rw=0
    cl=0

    RL=[]
    while len(List)>0:
            rad=random.choice(List)
            for x in range(len(List)):
                if List[x]==rad:
                     break
            RL.append(rad)
            del List[x]
            x=0
            rw=0
            cl=0
    for rw in range(3):
        for cl in range(3):
                RandomInitialState[rw,cl]=RL[x]
                x=x+1
    
    print("Initial State:"+str(rcount+1)) 
    print(RandomInitialState)
    print("Iterative-deepening:")      
    clc,spc,optimalPath,tm=IterativeDeepenng(RandomInitialState,rcount+1)
    
    if(clc==99999 and spc==99999 and optimalPath==99999):
        print("no solution")      
    else:
        
        print("Optimal Path:"+str(spc-1),",Search Path:"+str(clc-1),",Cost:"+str(spc-2),",Solution Path:"+str(spc-1),",Execution Time:"+str(tm)+" sec")
    print("DFS:")      
    clc,spc,optimalPath,tm=DFS(RandomInitialState,rcount+1)
    
    if(clc==99999 and spc==99999 and optimalPath==99999):
        print("no solution")      
    else:  
        print("Optimal Path:"+str(spc-1),",Search Path:"+str(clc-1),",Cost:"+str(spc-2),",Solution Path:"+str(spc-1),",Execution Time:"+str(tm)+" sec")    
    print("###############################################################################################################")           