import numpy as np
import world as w
N,M = 100,100
def getChildren(n,N,M):
    children = []
    i,j=get_row_col(n,M)
   
    for child in [n-1,n+1]:

        ic,jc=get_row_col(child,M)
        if ic==i and 0<=child<N*M:
            children.append(child)
    for child in [n-M,n+M]:
        if 0<=child<M*N:
            children.append(child)
    
    return children

#create graph representation of the board
def get_row_col(n,M):
    # Matrix NxM elements enumerated column wise
    # 1 2 3 4
    # 5 6 7 8
    # 9 .....
    return (n//M, n%M)

def get_n(i,j,N,M):
    return i*M+j 


def init_board(N,M):
    board = [i for i in range(0,N*M)]
    for n in range(0,N*M):
        board[n] = getChildren(n,N,M) 
    
    return board

def init_weights(board):
    N,M = len(board),len(board)
    # weight of the edges
    m = {}
    for i in range(0,len(board)):
        
        for j in board[i]:
                key=tuple(sorted([i,j])) 
                m[key]=0.001#np.random.random()    
    return m
def region(ant,i,j,dx,dy,M):
    # todo: make a class from the world
    ai,aj = w.get_row_col(ant.pos,M)
    if i<ai<i+dx and j<aj<j+dy:
    
        return True
    else:
        return False
def edges2mat(edges,N,M):
    MM = np.zeros((N,M))
    for k in edges:
        i,j = k
        val = edges[k] 
        i,j = w.get_row_col(j,M)
         
        MM[i,j]=val
    return MM
#transform edges to matrix
def elimanateLoop(path):
    #too difficult to remove cycles
    #will simplify path by taking every n'th element
    pass
 
if __name__=="__main__":
    N,M = 100,100
    board = init_board(N,M)
    weights = init_weights(N,M)

