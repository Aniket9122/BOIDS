import pygame
import math
import random

class Bird:
    def __init__(self, x, y, velocity=(0, 0), field_of_view=100, fov_angle=120):
        # Initialize position and velocity as pygame vectors for easy math operations
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(velocity)
        # Field of view parameters
        self.field_of_view = field_of_view  # Maximum distance at which the bird can 'see'
        self.fov_angle = fov_angle          # Total angle (in degrees) of the field of view
        # Optional limits for movement, which you may adjust or use in your main boids rules
        self.max_speed = 4
        self.max_force = 0.1

    def update(self):
        """Update the bird's position based on its velocity and ensure it doesn't exceed max_speed."""
        if random.random() < 0.05:  # 5% chance each frame
            angle = random.uniform(-30, 30)
            self.velocity = self.velocity.rotate(angle)
            #self.velocity.scale_to_length(self.max_speed)  # ensure consistent speed

        self.position += self.velocity
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

    def draw(self, screen):
        """Draw the bird as a triangle pointing in the direction of its velocity."""
        if self.velocity.length() == 0:
            # Prevent division by zero; if velocity is zero, default the angle to 0.
            angle = 0
        else:
            angle = self.velocity.angle_to(pygame.Vector2(1, 0))
        # Define triangle points relative to the bird's position
        head = self.position + pygame.Vector2(10, 0).rotate(-angle)
        left = self.position + pygame.Vector2(-5, 5).rotate(-angle)
        right = self.position + pygame.Vector2(-5, -5).rotate(-angle)
        pygame.draw.polygon(screen, (255, 255, 255), [head, left, right])

    def draw_field_of_view(self, screen):
        """Optionally draw the bird's field of vision as a circle with two boundary lines."""
        # Draw the outer circle representing the range of vision
        pygame.draw.circle(screen, (0, 255, 0), (int(self.position.x), int(self.position.y)), self.field_of_view, 1)
        # Calculate the bird's current heading; default to right if velocity is zero
        if self.velocity.length() == 0:
            heading_angle = 0
        else:
            heading_angle = self.velocity.angle_to(pygame.Vector2(1, 0))
        half_angle = self.fov_angle / 2
        # Determine the end points for the boundary lines of the field of view
        left_boundary = self.position + pygame.Vector2(self.field_of_view, 0).rotate(-heading_angle - half_angle)
        right_boundary = self.position + pygame.Vector2(self.field_of_view, 0).rotate(-heading_angle + half_angle)
        pygame.draw.line(screen, (0, 255, 0), self.position, left_boundary, 1)
        pygame.draw.line(screen, (0, 255, 0), self.position, right_boundary, 1)

    def is_in_field_of_view(self, other_position):
        """
        Check if a given position (another bird or object) falls within this bird's field of vision.
        Returns True if within the field of view (both angle and distance); False otherwise.
        """
        to_other = other_position - self.position
        distance = to_other.length()
        if distance > self.field_of_view:
            return False
        # Normalize the direction vector; default to (1,0) if velocity is zero.
        if self.velocity.length() == 0:
            direction = pygame.Vector2(1, 0)
        else:
            direction = self.velocity.normalize()
        # Determine the angle between the bird's heading and the direction to the other object
        angle = direction.angle_to(to_other)
        return abs(angle) < self.fov_angle / 2
