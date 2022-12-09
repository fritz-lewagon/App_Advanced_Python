import time
import numpy as np

import gym
from gym import spaces

from stable_baselines3 import PPO


import pygame

from ball_gym import Ball


class game(gym.Env):
    '''Modified game class to train the reinfocement learning AI'''
    
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


    def step(self, actions):

        reward = 0

        if actions == 1:
            x1_change = -1/2
        elif actions == 0:
            x1_change = 1/2
        

        if self.p_x1 >= self.dis_width-20:
            self.p_x1 = self.dis_width-30
        elif self.p_x1 <= 0:
            self.p_x1 = 5
        else:
            self.p_x1 += x1_change
               
        self.time_elapsed_since_last_action += 1
        self.total_time_elapsed += 1

        if self.time_elapsed_since_last_action > 500:
            self.objects.append(Ball())
            self.time_elapsed_since_last_action = 0

        
        position = 0
        for balls in self.objects:
            #print(position)
            x_ball, y_ball = balls.check_coordinates()
    
            self.state[position*2] = x_ball
            self.state[position*2+1] = y_ball
            position = position +1

        self.state[-1] = self.p_x1

        #print("objects",self.objects)  
        #print("state",self.state)

        for balls in self.objects:
            balls.move_ball()

        for item in self.objects:
            x_item, y_item = item.check_coordinates()
            length_regler = [i for i in range(int(self.p_x1)-5, int(self.p_x1)+55)]

            if (not (int(x_item) in length_regler and int(y_item) == self.dis_height-15)) and (int(y_item) in [i for i in range(self.dis_height-5, self.dis_height)]):
                self.counter_miss += 1
                print(self.counter_miss)
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

            print(self.state, reward, self.terminal)

        return self.state, reward, self.terminal, {}


    def reset(self):

        self.objects = []
        self.terminal = False
        self.state = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,self.p_x1])
        self.reward_memory.append(self.total_reward)
        print(self.reward_memory)
        self.total_reward = 0

        self.counter_caught = 0
        self.counter_miss = 0
        self.time_elapsed_since_last_action = 0
        self.total_time_elapsed = 0
        self.clock = 0

        return self.state

    def render(self, mode='human'):
        return self.state
  

def train_PPO(env_train, model_name, timesteps=30000):
    """PPO2 model"""

    start = time.time()
    model = PPO('MlpPolicy', env_train, verbose=1)
    model.learn(total_timesteps=timesteps)
    end = time.time()

    model.save("current_model")
    print('Training time (A2C): ', (end - start) / 60, ' minutes')
    return model

import os
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv


log_dir = "tmp/"
save_path = os.path.join(log_dir, 'current_model')

env_train = game()
env_train = Monitor(env_train, log_dir)
model_ppo = train_PPO(env_train, model_name="Fall_down_AI", timesteps=1170)
model_ppo.save(save_path)





