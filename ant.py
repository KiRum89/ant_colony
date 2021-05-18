import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import matplotlib.patches as patches
import world as w
#TODO: proper reflecton from the walls!
class Ant:

    
    def __init__(self,r,R,phi,speed,t):
        self.r = r

        self.phi = phi # direction of propagation 
        self.speed  = speed #speed < R 
        self.dr = np.array([self.speed*np.cos(self.phi),self.speed*np.sin(self.phi)]) 
        self.next_dr = np.array([self.speed*np.cos(self.phi),self.speed*np.sin(self.phi)]) 
        self.R = R # radius of the vision sector
        self.scout = True
        self.beta = np.pi/10
        self.t = 0
        self.alpha = np.pi/5 # angular aperture of the ant eye (width of the vision region)
        self.path = [self.r]
        NUM_SEC = 4 
        self.angles = np.linspace(-self.alpha/2,self.alpha/2,NUM_SEC)
        self.X=np.linspace(0,w.W,w.W//self.speed)
        self.Y = np.linspace(0,w.H,w.H//self.speed)

    def rotMatrix(self,dphi):
        return np.array([[np.cos(dphi),-np.sin(dphi)],[np.sin(dphi),np.cos(dphi)]])

    def rotate(self,vec,dphi):
        vec2 = np.dot(self.rotMatrix(dphi),vec)
        return vec2

    def move(self):
        
        r = self.r + self.dr 
        if r[0]>w.W or r[0]<0:
            self.dr[0] =-self.dr[0]
        elif r[1]>w.H or r[1]<0:
             self.dr[1] =-self.dr[1]
        self.r = self.r + self.dr 
        self.path.append(self.r)
        

    def decide(self,*trail):
        dphi = np.random.uniform(-self.beta/2,self.beta/2) 
        ex = self.dr/self.norm(self.dr) 
        self.dr = self.speed*self.rotate(ex,dphi)
        if len(trail)!=0:
            arr=self.get_pherom_counts(trail[0])  
            if len(arr)!=0:
                arr=sorted(arr, key = lambda el: el[1]) 
                counts=np.asarray([el[1] for el in arr])
                if np.any(counts!=0):
                    self.dr = np.asarray(arr[2][0])
                else:
                    pass
     
        self.next_dr = self.dr 

    def get_cell(self,r):
        idx_x = np.where(self.X<=r[0])[0][-1]
        idx_y = np.where(self.Y<=r[1])[0][-1]

        return [idx_x,idx_y]

    def mark_trail(self,trail):
        # trail can be scout trail - trail ant passed before food
        # trail_cargo - ant has food and goes follows the trail_scout
        i,j=self.get_cell(self.r)
        val = (self.r,self.t)
        if (i,j) not in trail:
            trail[(i,j)]=[val]
        else:
            trail[(i,j)].append(val)
        return (i,j)

    def get_pherom_counts(self,trail):
        #trail is a dict. Keys are cell (i,j), values are pheromome coordinates
        # count of pheromes in the central part 
        # count pgeromes in the sides

        m = {}
        #ant system of coordinates
        ex = self.dr/self.norm(self.dr) 
        ey = self.rotate(ex,np.pi/2)

        angles_av = 0.5*(self.angles[0:-1]+self.angles[1:])
        for angle in angles_av:
            dr = tuple(self.speed*(np.cos(angle)*ex+np.sin(angle)*ey)) # convert to touple for hashable
            m[dr]=0
        sector_cells = self.get_sector_cells()
        count = 0
        for (i,j) in sector_cells:
            count+=1
            pheroms = trail.get((i,j),None)         
            if pheroms!=None:
                for pher in pheroms:
                    #print('pher',len(pheroms))
                    coor = pher[0] 
                    vec=(coor-self.r)
                    if self.norm(vec)<=self.R:
                        vec = vec/self.norm(vec)
                        vec_y_ant = np.dot(vec,ey)
                        idx1=np.where(np.sin(self.angles)<=vec_y_ant)[0] # last element with smaller angle
                        idx2=np.where(np.sin(self.angles)>=vec_y_ant)[0] # first element with larger angle 
                        if len(idx1)!=0 and len(idx2)!=0: 
                            idx1 = idx1[-1]
                            idx2 = idx2[0]
                            angle = 0.5*(self.angles[idx1] + self.angles[idx2])
                            assert(np.abs(idx1-idx2)==1)
                            dr = tuple(self.speed*(np.cos(angle)*ex+np.sin(angle)*ey)) # convert to touple for hashable
                            m[dr]+=1
        ret = []
        for k in m:
            ret.append((k,m[k]))
        return ret

             
    def norm(self,vec):
        return (vec**2).sum()**0.5
        
        
    def get_sector_cells(self):
        #finidh finding the cells that a covered by the sector (it will be a rectangular. Find the min y, cover till y max, move until the x of the 3d vortex) 

        vertices = [self.r]
        ex = self.dr/self.norm(self.dr)
        ey = self.rotate(ex,np.pi/2)
        
         
        for ang in [-self.alpha/2,self.alpha/2]:
                d = self.R*np.cos(ang)*ex + self.R*np.sin(ang)*ey
                r = self.r + d    
                vertices.append(r)        
        idxs = [] 
        
        for r in vertices: 
            if r[0]<0:
                r[0]=0
            elif r[0]>w.W:
                r[0]=w.W
            if r[1]<0:
                r[1]=0
            elif r[1]>w.H:
                r[1]=w.H

            idxs.append(self.get_cell(r))
        
        idxs = np.array(idxs)
        idx_x_min=np.min(idxs[:,0])
        idx_y_min=np.min(idxs[:,1])
        idx_x_max=np.max(idxs[:,0])
        idx_y_max=np.max(idxs[:,1])



        for i in range(idx_x_min,idx_x_max+1):  
            for j in range(idx_y_min,idx_y_max+1):  
                yield (i,j)
        




 
if __name__ == "__main__":

    plt.ion()
    def run2(ants,cells,T):
        trail_home = {}

        cells = np.array(cells)
        fig,ax = plt.subplots(1,1)
        def draw_grid(ax):
            ax.vlines(np.linspace(0,w.W,w.W),0,w.H)
            ax.hlines(np.linspace(0,w.H,w.H),0,w.W)

        def plot(ants,T1,T2):            
            for ant in ants:
                path = np.array(ant.path)
                ax.plot(path[T1:T2,0],path[T1:T2,1],'+')
                #ax.plot(cells[:,0],cells[:,1],'+') 
                    
        #ant.get_pherom_counts(trail)                
        for ant in ants:   
            for t in range(0,T):
                if t<T//2:
                    ant.mark_trail(trail_home)
                    ant.move()
                    ant.decide()            
                
                else:
                    if t==T//2:
                       ant.dr = -ant.dr 

                       ant.move()
                #ant.mark_trail(trail)
                    else:
                        if t%5==0:
     
                            #draw_sight(ant)
                            #print('lalal',ant.dr) 
                            ax.arrow(ant.r[0],ant.r[1],ant.dr[0],ant.dr[1])

                        ant.decide(trail)            
                        ax.arrow(ant.r[0],ant.r[1],ant.next_dr[0],ant.next_dr[1],color='red')
                        ant .move()

        plot(ants,0,T//2)    
        plot(ants,T//2,T)
        #draw_grid(ax)


        ax.set_xlim([0,w.W])
        ax.set_ylim([0,w.H])



        #plt.show()
    
        return trail 


    ants=[Ant(np.array([1,1]),5,np.pi/2,0.1,0)]

    cells = []

    trail=run2(ants,cells,6000)
    
