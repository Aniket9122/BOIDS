"""
File: base_env.py
Envirionment Name: Base Environment

DESCRIPTION:
This program defines a base environment from which all other environments will inherit.

Authour: Victor Gachoki
Module: COMP5400M Bio Inspired Computing
Date: To Be Added
"""

import pygame
import math
import numpy as np
from Animats.bird import Bird
import random

NUM_BIRDS = 5
WHITE = (255, 255, 255)

class BaseEnvironment:
    def __init__(self, width, height):
        """
        Initialize the environment with a given width and height.
        The environment is represented as a 2D space where BOIDs can move.
        """
        self.width = width
        self.height = height
        self.obstacles = []
        self.birds = []
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Base Environment')
        
    def populate_environment(self, **kwargs):
        """
        Initialise positions of birds
        """
        for _ in range(NUM_BIRDS):
            position = [random.uniform(0, self.width), random.uniform(0, self.height)]
            bird = Bird(x = position[0], y = position[1], velocity=0.5, use_avoidance=False, use_alignment=False, use_cohesion=False)
            self.birds.append(bird)
            
    """
    Generate valid postion function to be created later after testing with blank environment.
    """
    
    def create_obstacles(self, type, pos, length=0, width=0, radius=0):
        if type == 'Circle':
            pygame.draw.circle(self.screen, WHITE, pos, radius)
        elif type == 'Rectangle':
            pygame.draw.rect(self.screen, WHITE, (*pos, length, width))    
    
    def render(self):
        """
        Render the environment and all BOIDs within it.
        This function should be called in the main loop of the simulation.
        """
        self.screen.fill((0, 0, 0))
        for bird in self.birds:
            bird.draw(self.screen)
            bird.draw_field_of_view(self.screen)
        pygame.display.flip()
        
    def update(self):
        for bird in self.birds:
            bird.randomWalkUpdate()
            self.boundaries(bird)
            
    def boundaries(self, bird):
        x, y = bird.position
        bird.position[0] = x % self.width
        bird.position[1] = y % self.height
            