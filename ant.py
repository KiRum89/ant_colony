import numpy as np
import world as w
#gloval paramters

class Ant:
    def __init__(self,pos,t):
        self.oldpos = None
        self.pos = pos
        self.food = False
        self.path = [pos]
        self.t = 0
        self.going_back = False        

    def move(self,newpos):
        self.oldpos = self.pos
        self.pos=newpos 
        self.path.append(self.pos)

    def decide(self,pherom_arr):
        alpha = 1
        children=w.getChildren(self.pos,w.N,w.M)        

        weights = []
        children2 = []
        for child in children:
            # only forward
            if child!=self.oldpos:
                #TODO: replace the loop with numpy
                children2.append(child)
                x =pherom_arr[child]
                weights.append(x)
        idx = self.get_direction(np.array(weights),alpha)
        return children2[idx]


    def get_direction(self,weights,alpha):

        if np.all(weights==0):
            idx = np.random.randint(len(weights))
            return idx
        PP = self.get_P(weights,alpha)
        s0=np.hstack((0,PP.cumsum()))            
        v = np.random.random()
        idx = np.where(s0<=v)[0][-1]
        return idx

    def get_P(self,weights,alpha):
        return weights**alpha/np.sum(weights**alpha)
         
    def deposit(self,x,pherom_arr):
    
        assert(self.oldpos!=None)
        for pos in self.path:

            pherom_arr[pos]+=x
             


if __name__ == "__main__":
    ant=Ant(50,1)
     
