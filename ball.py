import random
import pygame
from object import Object

class Ball(Object):
    '''A class to represent a ball to be caught falling down the screen.
    Inherits from object class.
    '''

    def __init__(self, time) -> None:
        '''Initializes a ball falling down the screen
        Parameters:
        time(int): total game time that has been passed'''
        
        self.time = time
        # Pass the attribute time to determine speed of object
        super(Ball, self).__init__(self.time)
        
        
        self.colour = (0,0,0)

        # Randomly select an image from list of available images
        self.l_ball_type = ["images//basketball.png","images//football.png","images//volleyball.png"]       
        ball_type = self.l_ball_type[random.randint(0,2)]

        # Randomly select an object size
        size = random.randint(15,20)

        # Give ball object texture
        self.danger_object = pygame.transform.scale(
            pygame.image.load(
            ball_type).convert_alpha(), (30, 30))

        # Randomly initialize coordinates of the object
        self.coordinates = [random.randint(5,800-size-5),0, size, size]

    def get_image(self) -> None:
        '''Function that returns the image object
        Paramters: None
        '''
        return self.danger_object   


       



    