import pygame
from ball import Ball
from danger import Danger
from pygame.locals import *

class Game():

    def __init__(self) -> None:
        '''Constructor to initalize an object of class game
        Paramters:
        -> None
        '''
        # Initialize pygame modules
        pygame.init()

        # Definition of all game colours
        self.white = (255, 255, 255)
        self.blue = (50, 153, 213)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 102)
        self.start_menu = True
        self.game_over = False
        self.game_close = False
        self.counter_miss = 0
        self.counter_caught = 0
        self.counter_danger = 0
        self.width = 50
        self.height = 15
        self.objects = []
        self.total_time_elapsed = 0
        self.time_elapsed_since_last_action = 0
        self.time_elapsed_since_last_action_danger = 0
        self.previous_score = 0
        self.high_score = 0

        # Definition of game font
        self.score_font = pygame.font.SysFont("comicsansms", 35)

        # Setting dimensions of the display
        self.dis_width = 800
        self.dis_height = 600
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))

        # Setting a caption for the display
        pygame.display.set_caption('CatchMe')

    def reset_game(self):
        self.total_time_elapsed = 0
        self.time_elapsed_since_last_action = 0
        self.time_elapsed_since_last_action_danger = 0
        self.objects.clear()
        self.counter_miss = 0
        self.counter_caught = 0
        self.counter_danger = 0
        self.game_close = False
        self.game_over = False

    def message(self, msg, color, position, font_size) -> None:
        '''Function to print a message to the display
        Paramters:
        msg (str): The message to be printed
        position (list): The position of the message to be printed on the screen
        '''
        mesg = font_size.render(msg, True, color)
        self.dis.blit(mesg, position)

    def display_score(self, score, missed, counter_danger, previous_score, high_score) -> None:
        score = "Your Score: " + str(score)
        missed = "You missed: " + str(missed)
        danger = "Dangerous objects: " + str(counter_danger)
        previous_score = "Previous score: " +str(previous_score)
        high_score = "Highest score: " +str(high_score)

        self.message(score, self.red, [0, 0], pygame.font.SysFont(None, 30))
        self.message(missed, self.red, [0, 20], pygame.font.SysFont(None, 30))
        self.message(danger, self.red, [0, 40], pygame.font.SysFont(None, 30))
        self.message(previous_score, self.red, [0, 60], pygame.font.SysFont(None, 30))
        self.message(high_score, self.red, [0, 80], pygame.font.SysFont(None, 30))

    def game_menu(self) -> bool:
        '''Function to display the starting menu of the game
        Paramters:
        -> None
        '''

        # Change background colour to white to intialize starting menu
        self.dis.fill(self.white)
        self.start_menu = True

        # Define options in the starting menu
        self.message("Welcome to our game", self.red, [
                     self.dis_width/3, self.dis_height/3], pygame.font.SysFont(None, 50))
        self.message("Here are the rules:", self.red, [
                     self.dis_width/3, self.dis_height/3+50], pygame.font.SysFont(None, 30))
        self.message("1. You have to catch the balls falling down.", self.red, [
                     self.dis_width/3, self.dis_height/3+100], pygame.font.SysFont(None, 25))
        self.message("2. You are only allowed to miss 3 balls.", self.red, [
                     self.dis_width/3, self.dis_height/3+150], pygame.font.SysFont(None, 25))
        self.message("3. Don't catch the bombs. If you catch 2, you loose!", self.red, [
                     self.dis_width/3, self.dis_height/3+200], pygame.font.SysFont(None, 25))
        self.message("Press A to play", self.red, [
                     self.dis_width/3, self.dis_height/3+250], pygame.font.SysFont(None, 30))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.start_menu = False

        return self.start_menu

    def end_screen(self):
        self.objects.clear()
        self.dis.fill(self.white)
        self.message("Game Over!", self.red, [
                     self.dis_width/3, self.dis_height/3], pygame.font.SysFont(None, 50))
        self.message("Your Score: " + str(self.counter_caught), self.red,
                     [self.dis_width/3, self.dis_height/3+50], pygame.font.SysFont(None, 30))
        self.message("Your High Score: " + str(self.high_score), self.red,
                     [self.dis_width/3, self.dis_height/3+100], pygame.font.SysFont(None, 30))
        self.message("Press Q-Quit or C-Play Again", self.red,
                     [self.dis_width/3, (self.dis_height/3)+150], pygame.font.SysFont(None, 30))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game_close = True
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    self.reset_game()

    def gameLoop(self) -> None:
        '''Main game loop
        Parameters:
        -> None
        '''
        # Setting game variables and initializing game clock
        clock = pygame.time.Clock()

        # Initializing position of player
        x1 = self.dis_width-500
        y1 = self.dis_height-20
        x1_change = 0

        while not self.game_close:
            while self.start_menu:
                self.start_menu = self.game_menu()

            # Initialize game score and set background colour
            self.dis.fill(self.white)
            self.display_score(self.counter_caught,
                               self.counter_miss, self.counter_danger, self.previous_score, self.high_score)

            pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

            # Check for user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_close = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -5
                    elif event.key == pygame.K_RIGHT:
                        x1_change = 5
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        x1_change = 0

            # Check if player is on the right corner of the screen and block movement
            if x1 >= self.dis_width-self.width:
                x1 = self.dis_width-self.width-10

            # Check if player is on the left corner of the screen and block movement
            elif x1 <= 0:
                x1 = 10

            # If player not on right or left corner move player according to user input
            elif x1 <= (self.dis_width-self.width) and x1 > 0:
                x1 += x1_change

            # Visualize player
            pygame.draw.rect(self.dis, self.black, [
                             x1, y1, self.width, self.height])

            # Capture game time
            dt = clock.tick()
            self.time_elapsed_since_last_action += dt
            self.time_elapsed_since_last_action_danger += dt
            self.total_time_elapsed += dt

            # Spawn objects if a certain amount of game time has passed
            if self.time_elapsed_since_last_action > 3000:
                self.objects.append(Ball(self.total_time_elapsed))
                self.time_elapsed_since_last_action = 0
            if self.time_elapsed_since_last_action_danger > 5000:
                self.objects.append(Danger(self.total_time_elapsed))
                self.time_elapsed_since_last_action_danger = 0

            # Move all objects
            for item in self.objects:
                pygame.draw.rect(self.dis, item.colour, item.coordinates)
                self.dis.blit(item.get_image(), item.coordinates)

                # check the type of the object
                if isinstance(item, Ball):
                    item.move()
                else:
                    item.move()

            # Check if player missed or captured an object
            for item in self.objects:
                is_danger = isinstance(item, Danger)

                # Get coordinates of item
                x_item, y_item = item.check_coordinates()
                # Intialize bounding box of player
                length_regler = [i for i in range(
                    (int(x1)-5), (int(x1)+self.width+10))]

                h_regler = [i for i in range(
                    self.dis_height-20, self.dis_height)]

                # Check if player captured an item

                # Check if coordinates of player and object agree
                if ((int(x_item) in length_regler) and (int(y_item) in h_regler)):
                    # If ball object increase objects caught count
                    if not is_danger:
                        self.counter_caught += 1
                    # If danger object increase danger count
                    else:
                        self.counter_danger += 1
                        if self.counter_danger == 2:
                            self.game_over = True
                            break

                    self.objects.remove(item)

                # Check if player missed an object
                elif (not (int(x_item) in length_regler and int(y_item) == self.dis_height-15)) and (int(y_item) in [i for i in range(self.dis_height-5, self.dis_height)]):
                    if not is_danger:
                        self.counter_miss += 1
                    self.objects.remove(item)

                    if self.counter_miss == 3:
                        self.previous_score = self.counter_caught
                        if self.counter_caught > self.high_score:
                            self.high_score = self.counter_caught

                        self.game_over = True
                        break

            # Display final screen if player missed three objects
            while self.game_over == True:
                self.end_screen()

            # Update screen with all changes made
            pygame.display.update()

        # Quit programm
        pygame.quit()
        quit()
