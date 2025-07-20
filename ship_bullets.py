import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """
    A class to manage bullets fired from ship
    """

    def __init__(self, ai_settings, screen, ship):
        """
        Create object at ship's position
        """

        super(Bullet, self).__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        # Start bullet at the center left of the screen.
        self.rect.centery = ship.rect.centery
        self.rect.right = ship.rect.right

        # Store decimal value of the bullet's position
        self.x = float(self.rect.x)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed

    def update(self):
        """
        Bullet is fired from the ship
        """
        #update decimal position of bullet
        self.x += self.speed_factor
        #update rect position
        self.rect.x = self.x

    def draw_bullet(self):
        """
        Draw bullet
        """
        pygame.draw.rect(self.screen, self.color, self.rect)