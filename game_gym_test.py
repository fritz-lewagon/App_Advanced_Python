import numpy as np
import gym
from gym import spaces
from stable_baselines3 import PPO
import pygame
from ball_gym import Ball

class game(gym.Env):
    '''Modified game class to test reinforcement learning AI'''
    
    def __init__(self) -> None:
        super(game, self).__init__()
        pygame.init()

        self.dis_width = 800
        self.dis_height = 600

        self.objects = []

        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(low=0, high=np.inf, shape = (27,))

        self.counter_caught = 0
        self.counter_miss = 0
        self.time_elapsed_since_last_action = 0
        self.total_time_elapsed = 0
        self.clock = 0

        self.p_x1 = self.dis_width-500
        self.p_y1 = self.dis_height-20

        self.terminal = False
        self.state = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,self.p_x1])
        self.total_reward = 0
        self.reward_memory = []

        # Grafical interface
        self.white = (255, 255, 255)
        self.blue = (50, 153, 213)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 102)
        self.dis_width = 800
        self.dis_height = 600
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption('Game')
        self.score_font = pygame.font.SysFont("comicsansms", 35)
        self.dis.fill(self.blue)
        self.display_score(self.counter_caught, self.counter_miss)

    def display_score(self, score, missed):
        value = self.score_font.render(
            "Your Score: " + str(score), True, self.yellow)
        value2 = self.score_font.render(
            "You missed: "+str(missed), True, self.yellow)
        self.dis.blit(value, [0, 0])
        self.dis.blit(value2, [0, 50])


    def step(self, actions):

        reward = 0

        if actions == 1:
            x1_change = -1
        elif actions == 0:
            x1_change = 1
        

        if self.p_x1 >= self.dis_width-20:
            self.p_x1 = self.dis_width-30
        elif self.p_x1 <= 0:
            self.p_x1 = 5
        else:
            self.p_x1 += x1_change

        self.dis.fill(self.blue)
        self.display_score(self.counter_caught, self.counter_miss)
               
        self.time_elapsed_since_last_action += 1
        self.total_time_elapsed += 1

        if self.time_elapsed_since_last_action > 500:
            self.objects.append(Ball())
            self.time_elapsed_since_last_action = 0

        
        position = 0
        for balls in self.objects:
            x_ball, y_ball = balls.check_coordinates()
    
            self.state[position*2] = x_ball
            self.state[position*2+1] = y_ball
            position = position +1

        self.state[-1] = self.p_x1

        for balls in self.objects:
                pygame.draw.rect(self.dis, balls.colour, balls.coordinates)
                balls.move_ball()

        pygame.draw.rect(self.dis, self.black, [self.p_x1, self.p_y1, 50, 15])

        #print("objects",self.objects)  
        #print("state",self.state)

        for item in self.objects:
            x_item, y_item = item.check_coordinates()
            length_regler = [i for i in range(int(self.p_x1)-5, int(self.p_x1)+55)]

            if (not (int(x_item) in length_regler and int(y_item) == self.dis_height-15)) and (int(y_item) in [i for i in range(self.dis_height-5, self.dis_height)]):
                self.counter_miss += 1
                self.objects.remove(item)
                if self.counter_miss == 3:
                    self.Terminal = True
                    pygame.quit()
                    break

            if (int(x_item) in length_regler and int(y_item) == self.dis_height-15):
                self.counter_caught += 1
                reward += 1
                self.total_reward += 1
                self.objects.remove(item)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("quiet")
                

        return self.state, reward, self.terminal, {}


    def reset(self):

        self.objects = []
        self.terminal = False
        self.state = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,self.p_x1])
        self.reward_memory.append(self.total_reward)
        self.total_reward = 0

        self.counter_caught = 0
        self.counter_miss = 0
        self.time_elapsed_since_last_action = 0
        self.total_time_elapsed = 0
        self.clock = 0

        return self.state

test_environment = game()
current_model_ppo2 = PPO.load("current_model")
obs = test_environment.reset()

for i in range(10000):
    action, _states = current_model_ppo2.predict(obs)
    obs, rewards, done, info = test_environment.step(action)



    
    