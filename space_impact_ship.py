import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        # Create ship for the game Space Impact
        # Initialize its starting position
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load ship image and get its rect(angle).
        self.image = pygame.image.load('D:/ew/Technical Skills/LAWG coding/space impact/ship_removedbg.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
#        self.image = pygame.image.load('D:/ew/Technical Skills/LAWG coding/space impact/ate issa.jpg').convert_alpha()
#        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start ship at the center left of the screen.
        self.rect.centery = self.screen_rect.centery + 35.0
        self.rect.left = self.screen_rect.left + 100.0

        # Store decimal value for the ship's center
        self.centery = float(self.rect.centery)
        self.centerx = float(self.rect.left)

        # Movement flags
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

    def update(self):
        """
        Update the ship's position based on the movement flag
        """
        speed_value = self.ai_settings.ship_speed
        # Move the ship up
        if self.moving_up and self.rect.top > 0:
            self.centery -= speed_value
        # Move the ship down
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += speed_value
        # Move the ship left
        if self.moving_left and self.rect.left > 0:
            self.centerx -= speed_value
        # Move the ship right
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += speed_value

        # Update rect object from self.center
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def center_ship(self):
        """
        Center ship on screen
        """
        self.rect.centery = self.screen_rect.centery
        self.rect.left = self.screen_rect.left + 50.0
        self.centery = float(self.rect.centery)
        self.centerx = float(self.rect.left)

    def blitme(self):
        # Draw ship at current location.
        self.screen.blit(self.image, self.rect)