import numpy as np
import matplotlib
import matplotlib.pyplot as plt

plt.ion()
import matplotlib.patches as patches
import world as w
#TODO: proper reflecton from the walls!
class Ant:
    def __init__(self,r,R,phi,speed,t):
        self.r = r



        self.phi = phi # direction of propagation 
        self.speed  = speed #speed < R 
        self.dr = np.array([self.speed*np.cos(self.phi),self.speed*np.sin(self.phi)]) 

        self.R = R # radius of the vision sector
        self.scout = False
        self.t = 0
        self.alpha = 0.3 # angular aperture of the ant eye (width of the vision region)
        self.path = [self.r]
        self.phi_arr = [self.phi]

    def rotMatrix(self,dphi):
        return np.array([[np.cos(dphi),-np.sin(dphi)],[np.sin(dphi),np.cos(dphi)]])

    def rotate(self,vec,dphi):
        vec2 = np.dot(self.rotMatrix(dphi),vec)
        return vec2

    def move(self):

        self.r = self.r + self.dr 
        self.path.append(self.r)
        self.phi_arr.append(self.phi)

    def decide(self,*trail):
        dphi = np.random.uniform(-self.alpha/2,self.alpha/2) 

        if len(trail)!=0:
            arr=self.get_pherom_counts(trail[0])  
            arr=sorted(arr, key = lambda el: el[1]) 
            self.phi = arr[2][0]
            if arr[2][1] == 0:
            
                self.phi = self.phi + dphi
        else:
            self.phi = self.phi + dphi
               
            
              

    def get_cell(self,r):
        
        #TODO: improve 
        X=np.linspace(0,w.W,w.W)
        Y = np.linspace(0,w.H,w.H)
        idx_x = np.where(X<=r[0])[0][-1]
        idx_y = np.where(Y<=r[1])[0][-1]
        return [idx_x,idx_y]

    def mark_trail(self,trail):
        # trail can be scout trail - trail ant passed before food
        # trail_cargo - ant has food and goes follows the trail_scout
        i,j=self.get_cell(self.r)
        if (i,j) not in trail:
            trail[(i,j)]=[self.r]
        else:
            trail[(i,j)].append(self.r)

    def get_pherom_counts(self,trail):
        #trail is a dict. Keys are cell (i,j), values are pheromome coordinates
        # count of pheromes in the central part 
        # count pgeromes in the sides

        m = {}
        NUM_SEC = 4 
        angles = np.linspace(-self.alpha/2,self.alpha/2,NUM_SEC)
        
        # ant system of coordinates
        ex = self.dr/self.norm(self.dr) 
        ey = self.rotate(ex,np.pi/2)
        for (i,j) in self.get_sector_cells():
            pheroms = trail.get((i,j),None)         
            if pheroms!=None:
                for pher in pheroms:
                    print('----')
                    print('pher', pher)
                    vec=(pher-self.r)
                    vec = vec/self.norm(vec)
                    vec_y_ant = np.dot(vec,ey)
                    idx1=np.where(np.sin(angles)<=vec_y_ant)[0] # last element with smaller angle
                    idx2=np.where(np.sin(angles)>=vec_y_ant)[0] # first element with larger angle 
                    print('lalalal',idx1,idx2)
                    if len(idx1)!=0 and len(idx2)!=0: 


                        idx1 = idx1[-1]
                        idx2 = idx2[0]
                        angle = 0.5*(angles[idx1] + angles[idx2])

                        print('angle',angle)
                        angle = angle + self.phi
                        if angle in m:
                            print('asdasd',m)
                            m[angle]+=1
                        else:
                            print('ang', angle, self.phi)
                            m[angle]=1
        return m
        ret = []

        print('mm',m)  
        for k in m:
            ret.append((k,m[k]))
        return ret

             
    def norm(self,vec):
        return np.sum(vec**2)**0.5
        
        
    def get_sector_cells(self):
        # TODO: make more elegant 
        # return generator - yes

        #finidh finding the cells that a covered by the sector (it will be a rectangular. Find the min y, cover till y max, move until the x of the 3d vortex) 

        vertices = [self.r]
        for ang in [-self.alpha/2,self.alpha/2]:
                r = self.r + np.array([self.R*np.cos(self.phi-ang),self.R*np.sin(self.phi-ang)])    
                vertices.append(r)        
        idxs = [] 
        
        for r in vertices: 
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
    def run2(ants,cells,T,thome):
        trail = {}

        cells = np.array(cells)
        fig,ax = plt.subplots(1,1)
        def draw_grid(ax):
            ax.vlines(np.linspace(0,w.W,w.W),0,w.H)
            ax.hlines(np.linspace(0,w.H,w.H),0,w.W)

        def plot(ants):            
            for ant in ants:
                path = np.array(ant.path)
                ax.plot(path[:,0],path[:,1],'-')
                #ax.plot(cells[:,0],cells[:,1],'+') 

        def onclick(event):
            print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y, event.xdata, event.ydata))
            print(ant.get_cell(np.array([event.xdata,event.ydata])))
            cell = tuple(ant.get_cell(np.array([event.xdata,event.ydata])))
            if cell not in trail:
                trail[cell]=[[event.xdata,event.ydata]]
            else:
                trail[cell].append([event.xdata,event.ydata])
   
            #print(trail)
            print('pherom counts{}'.format(ant.get_pherom_counts(trail)))
            

        cid = fig.canvas.mpl_connect('button_press_event', onclick)



        def draw_sight(ant):
            phis = np.array(ant.phi_arr)
            path = np.array(ant.path)
            for pos,phi in zip(path[::1],phis[::1]):    
                x,y = pos
                phi1,phi2 = np.rad2deg(phi+np.array([-ant.alpha/2,ant.alpha/2]))
                ax.add_patch(
                patches.Wedge(
                    (x, y),         # (x,y)
                    ant.R,            # radius
                    phi1,             # theta1 (in degrees)
                    phi2,            # theta2
                    color="g", alpha=0.2
                    )
                )
                ax.add_patch(
                patches.Wedge(
                    (x, y),         # (x,y)
                    ant.R,            # radius
                    phi1+np.rad2deg(ant.alpha/3),             # theta1 (in degrees)
                    phi2-np.rad2deg(ant.alpha/3),            # theta2
                    color="r", alpha=0.2
                    )
               ) 
            
            ax.arrow(ant.r[0],ant.r[1],ant.dr[0],ant.dr[1])            
                    
        #ant.get_pherom_counts(trail)                

        plot(ants)    
        for ant in ants:   
            draw_sight(ant)
        draw_grid(ax)
        ax.set_xlim([0,w.W])
        ax.set_ylim([0,w.H])
        plt.show()
        return trail 


    ants=[Ant(np.array([1,1]),6,np.pi/3,0.6,0)]
    ant = ants[0] 

    cells = []


               
    trail=run2(ants,cells,1,1)
    
