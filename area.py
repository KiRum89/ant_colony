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
        
