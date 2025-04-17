import pygame
from Environment.env_1 import blank_environment
from Environment.base_env import BaseEnvironment

pygame.init()

env = BaseEnvironment()
env.populate_environment()
env.render()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    env.update()
    env.render()

pygame.quit()