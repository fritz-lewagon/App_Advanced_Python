import random
from object import Object
import pygame


class Danger(Object):
    '''A class to represent a dangerous object that should not be catched falling down the screen.
    Inherits from object class.
    '''

    def __init__(self, time) -> None:
        '''
        Initializes the dangerous object to fall down the screen
        Parameters:
        time(int): total game time that has been passed
        '''
        self.time = time
        # Pass the attribute time to determine speed of object
        super(Danger, self).__init__(self.time)

        self.colour = (255, 255, 255)

        # Give danger object texture
        self.danger_object = pygame.transform.scale(
            pygame.image.load(
            'images//bomb.png').convert_alpha(), (50, 30))

        # Set a standard size for the object
        size = 30 

        # Randomly initialize x-coordinate of the object
        self.coordinates = [random.randint(5, 800-size-5), 0, size, size]


    def get_image(self) -> None:
        '''Function that returns the image object
        Paramters: None
        '''
        return self.danger_object

    

