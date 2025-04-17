import pygame, random
from Rules.rules import FlockingRules

class Bird(FlockingRules):
    def __init__(self, x, y, velocity=(0, 0), field_of_view=100, fov_angle=120,
                 use_avoidance=True, use_alignment=True, use_cohesion=True,
                 avoidance_strength=1.5, alignment_strength=1.0, cohesion_strength=1.0):
        # Position and velocity vectors
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(velocity)
        self.acceleration = pygame.Vector2(0, 0)
        # Vision parameters
        self.field_of_view = field_of_view
        self.fov_angle = fov_angle
        # Movement constraints
        self.max_speed = 0.5
        self.max_force = 0.1
        # Rule toggles and strengths
        self.use_avoidance = use_avoidance
        self.use_alignment = use_alignment
        self.use_cohesion = use_cohesion
        self.avoidance_strength = avoidance_strength
        self.alignment_strength = alignment_strength
        self.cohesion_strength = cohesion_strength
        # Smooth movement parameters
        self.speed = self.max_speed
        self.heading = self.velocity.normalize()
        self.angular_velocity = 0.0
        self.angular_accel_sigma = 0.1
        self.angular_damping = 0.3 # Keep this between 0.0 - 1.0

    def apply_force(self, force):
        """Accumulate steering forces."""
        self.acceleration += force

    def flock(self, neighbors):
        """
        Compute and apply separation (avoidance), alignment, and cohesion
        based on nearby neighbors.
        """
        if self.use_avoidance:
            steer = self.avoidance(neighbors, self.avoidance_strength)
            self.apply_force(steer)
        if self.use_alignment:
            steer = self.alignment(neighbors, self.alignment_strength)
            self.apply_force(steer)
        if self.use_cohesion:
            steer = self.cohesion(neighbors, self.cohesion_strength)
            self.apply_force(steer)

    def update(self):
        """
        Update velocity and position, limit speed, and reset acceleration.
        Includes a small random perturbation for exploration.
        """
        # Random heading perturbation (optional)
        if random.random() < 0.05:
            angle = random.uniform(-30, 30)
            self.velocity = self.velocity.rotate(angle)

        # Integrate acceleration
        self.velocity += self.acceleration
        # Limit speed
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        # Update position
        self.position += self.velocity
        # Reset acceleration for next frame
        self.acceleration = pygame.Vector2(0, 0)
        
    def randomWalkUpdate(self):
        accel = random.gauss(0, self.angular_accel_sigma)
        self.angular_velocity += accel
        self.angular_velocity *= (1.0 - self.angular_damping)
        self.heading.rotate_ip(self.angular_velocity)
        self.velocity = self.heading * self.speed
        self.position += self.velocity

    def draw(self, screen):
        """Draw the bird as a triangle pointing in direction of its velocity."""
        if self.velocity.length() == 0:
            angle = 0
        else:
            angle = self.velocity.angle_to(pygame.Vector2(1, 0))
        s = 0.5
        head  = self.position + pygame.Vector2(10, 0).rotate(-angle) * s
        left  = self.position + pygame.Vector2(-5, 5).rotate(-angle) * s
        right = self.position + pygame.Vector2(-5, -5).rotate(-angle) * s
        pygame.draw.polygon(screen, (255, 255, 255), [head, left, right])

    def draw_field_of_view(self, screen):
        """Optionally visualize the bird's field of view."""
        pygame.draw.circle(screen, (0, 255, 0),
                           (int(self.position.x), int(self.position.y)),
                           self.field_of_view, 1)
        heading = (self.velocity.angle_to(pygame.Vector2(1, 0))
                   if self.velocity.length() else 0)
        half = self.fov_angle / 2
        left_b  = self.position + pygame.Vector2(self.field_of_view, 0).rotate(-heading - half)
        right_b = self.position + pygame.Vector2(self.field_of_view, 0).rotate(-heading + half)
        pygame.draw.line(screen, (0, 255, 0), self.position, left_b, 1)
        pygame.draw.line(screen, (0, 255, 0), self.position, right_b, 1)

    def is_in_field_of_view(self, other_pos):
        """
        Check if a given position is within this bird's field of vision.
        """
        to_other = other_pos - self.position
        dist = to_other.length()
        if dist > self.field_of_view:
            return False
        direction = (self.velocity.normalize()
                     if self.velocity.length() else pygame.Vector2(1, 0))
        return abs(direction.angle_to(to_other)) < self.fov_angle / 2
