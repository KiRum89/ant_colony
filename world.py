import numpy as np
import world as w
H,W = 100,100
R = 10
r0 = np.array([60,60])
 
def isFood(r):
    # r ant coordinate
    # r0 food circle center
    # R food circle radius
    if np.sum((r-r0)**2)**0.5<R:
        return True
    else:
        return False
    


def evaporate(pherom_arr, rate):
    pass

if __name__=="__main__":
    N,M = 100,100
    board = init_board(N,M)
    weights = init_weights(N,M)

