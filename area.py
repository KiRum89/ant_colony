import numpy as np

# create a circular area
class CircArea:
    def __init__(self,col,r0,R):
        # color, r0 (coordinates center), Radius
        self.col = col 
        self.r0=r0
        self.R=R
    def inside(self,r):
     
        if np.sum((r-self.r0)**2)**0.5<self.R:
            return True
        else:
            return False

    def drag(self,pygame):

        x0,y0 = self.r0
        x,y=pygame.mouse.get_pos()
        if ((x0-x)**2+(y0-y)**2)**0.5<self.R:
            state = pygame.mouse.get_pressed(num_buttons=3) 
            if state[0]==True:
                x0,y0 = pygame.mouse.get_pos()
                self.r0 = np.array([x0,y0])
        
class CircAreaGranular:
    def __init__(self,col,r0,R,N,M):
        # color, r0 (coordinates center), Radius
        self.col = col 
        self.r0=r0
        self.R=R
        self.N = N
        self.M = M
    
    def create(self):
        arr=np.zeros((self.N,self.M))
        for i in range(0,self.N):
            for j in range(0,self.M):
                if (i-self.r0[0])**2+(j-self.r0[1])**2<self.R**2: 
                    arr[i,j]=1
        self.arr=arr 
    def inside(self,r):
        i,j = int(r[0]),int(r[1])
        if self.arr[i,j]==1:
            return True
        else:
            return False
            
        

    def plot(self,pygame,gameDisplay):
        for i in range(0,self.N):
            for j in range(0,self.M):
                if self.arr[i,j]==1:
                    rect = pygame.Rect(i,j,1,1)
                    pygame.draw.rect(gameDisplay,self.col,rect)


                 



