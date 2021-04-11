import numpy as np
import world as w
#gloval paramters

class Ant:
    def __init__(self,pos,t):
        self.oldpos = None
        self.pos = pos
        self.edge = None
        self.food = False
        self.path = [pos]

    def move(self,newpos):
        self.oldpos = self.pos
        self.pos=newpos 
        self.path.append(self.pos)

    def decide(self,edges):
        alpha = 1
        children=w.getChildren(self.pos,w.N,w.M)        

        weight = []
        children2 = []
        for child in children:

            if child!=self.oldpos:
                children2.append(child)
                edge=tuple(sorted([self.pos, child]))
                x = edges[edge]
                weight.append(x)
        idx = self.get_direction(np.array(weight),alpha)
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

    def deposit(self,x,edges):
        assert(self.oldpos!=None)
        key =tuple(sorted([self.oldpos,self.pos]))
        if self.food==True:
            #print('lalalala',x)
            edges[key]+=x
        
    def deposit2(self,x,edges):
    
        assert(self.oldpos!=None)
        key =tuple(sorted([self.oldpos,self.pos]))
        if self.food==True:
            #print('lalalala',x)
            for i in range(0,len(self.path)-1):
                key = tuple(sorted([self.path[i],self.path[i+1]))
                edges[key]+=x
                 


if __name__ == "__main__":
    ant=Ant(50,1)
     
