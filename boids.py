import pygame
from Environment.base_env import BaseEnvironment

pygame.init()

env = BaseEnvironment(800, 600)
env.populate_environment()
env.render()

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()