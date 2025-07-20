import random
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """
    A class representing a single alien in a fleet.
    """
    def __init__(self, ai_settings, screen):
        """
        Initialize alien and its starting position.
        """
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load alien image and set rect attribute
        self.image = pygame.image.load('D:/ew/Technical Skills/LAWG coding/space impact/alien_ship_removedbg.png').convert_alpha()
#        self.image = pygame.image.load('D:/ew/Technical Skills/LAWG coding/space impact/dollar_sign-removedbg.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        # Set starting position of alien
        self.rect.x = ai_settings.screen_width - (2 * self.rect.width)
        self.rect.y = random.randint(0, ai_settings.screen_height - self.rect.height)
        
        # Store float of alien's exact position
        self.x = float(self.rect.x)

    def check_edges(self):
        """
        Return True if alien is at edge of screen
        """
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom:
            return True
        elif self.rect.top <= 70:
            return True

    def blitme(self):
        """
        Draw alien at its current location
        """
        self.screen.blit(self.image, self.rect)

    def update(self):
        """
        Move the alien up or down
        
        """
        self.y += (self.ai_settings.alien_speed * self.ai_settings.fleet_direction)
        self.rect.y = self.y