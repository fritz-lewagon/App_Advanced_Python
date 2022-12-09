import random

class Ball():
    '''Modified class to fit reinforcement learning environment'''

    def __init__(self):
        '''Initializes an object to fall down the screen
        Parameters:
        time(int): total game time that has been passed'''
        
        # Randomly select a colour from list of available colours
        self.l_colours = [(255,0,0),(0,255,0),(0,0,255)]       
        self.colour = self.l_colours[random.randint(0,2)]

        # Randomly select an object size
        size = random.randint(10,20)

        # Randomly initialize coordinates of the object
        self.coordinates = [random.randint(5,800-size-5),0, size, size]


    def move_ball(self):
        ''' Function to move the object one step
        Parameters:
        -> None
        '''
        # Falling speed increases with time 
        if self.coordinates[0] > 1:
            self.coordinates[1] += 0.5


    def check_coordinates(self):
        ''' Function to check the object's coordinates
        Parameters:
        -> None
        '''
        self.x = self.coordinates[0]
        self.y = self.coordinates[1] 

        return self.x, self.y      



    