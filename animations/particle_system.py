import pygame
import random
import math

class Particle:
    def __init__(self, x, y, color, velocity, size, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.size = size
        self.lifetime = lifetime
        self.current_time = 0
        
    def update(self, dt):
        self.current_time += dt
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        self.size *= 0.95  # Shrink over time
        
    def is_dead(self):
        return self.current_time >= self.lifetime
        
    def draw(self, screen):
        alpha = int(255 * (1 - self.current_time / self.lifetime))
        color = (*self.color, alpha)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def emit(self, x, y, color, count=10):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(100, 200)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            size = random.uniform(2, 5)
            lifetime = random.uniform(0.5, 1.0)
            
            self.particles.append(Particle(x, y, color, velocity, size, lifetime))
            
    def update(self, dt):
        for particle in self.particles[:]:
            particle.update(dt)
            if particle.is_dead():
                self.particles.remove(particle)
                
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
            
    def clear(self):
        self.particles.clear() 