# Rules/rules.py
import pygame

class FlockingRules:
    def __init__(self, max_speed=4, max_force=0.1):
        self.max_speed = max_speed
        self.max_force = max_force
    
    def avoidance(self, neighbors, strength=1.5):
        steer = pygame.Vector2(0, 0)
        total = 0
        for other in neighbors:
            diff = self.position - other.position
            dist = diff.length()
            if dist > 0:
                steer += diff.normalize() / dist
                total += 1
        if total > 0:
            steer /= total
            steer.scale_to_length(self.max_speed)
            steer -= self.velocity
            if steer.length() > self.max_force:
                steer.scale_to_length(self.max_force)
        return steer * strength

    def alignment(self, neighbors, strength=1.0):
        avg_vel = pygame.Vector2(0, 0)
        total = 0
        for other in neighbors:
            avg_vel += other.velocity
            total += 1
        if total > 0:
            avg_vel /= total
            avg_vel.scale_to_length(self.max_speed)
            steer = avg_vel - self.velocity
            if steer.length() > self.max_force:
                steer.scale_to_length(self.max_force)
            return steer * strength
        return pygame.Vector2(0, 0)

    def cohesion(self, neighbors, strength=1.0):
        center = pygame.Vector2(0, 0)
        total = 0
        for other in neighbors:
            center += other.position
            total += 1
        if total > 0:
            center /= total
            desired = (center - self.position)
            desired.scale_to_length(self.max_speed)
            steer = desired - self.velocity
            if steer.length() > self.max_force:
                steer.scale_to_length(self.max_force)
            return steer * strength
        return pygame.Vector2(0, 0)
