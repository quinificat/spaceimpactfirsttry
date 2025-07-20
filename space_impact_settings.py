import pygame

class Settings():
    """
    Settings for Space Impact: Reenvisioned
    """

    def __init__(self):
        """
        Initialize game's static settings
        """
        #Screen settings
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (40, 36, 66)
        self.ship_limit = 3

        #Bullet settings
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = 255, 255, 0
        self.bullets_allowed = 5

        #Alien settings
        self.fleet_movespeed = 7.5

        #Gamespeed
        self.speedup_scale = 1.25

        #Point increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()        
    
    def load_background(self):
        self.bg_image = pygame.image.load('D:\ew\Technical Skills\LAWG coding\space impact\space background.png').convert()
        self.bg_image = pygame.transform.scale(self.bg_image,
                                               (self.screen_width,
                                                self.screen_height)
        )

    def initialize_dynamic_settings(self):
        """
        Initialize settings that change throughout the game
        """
        self.ship_speed = 1.25
        self.bullet_speed = 3.5
        self.alien_speed = 0.75

        # direction of fleet
        self.fleet_direction = 1.2

        # score
        self.alien_points = 10

    def increase_speed(self):
        """
        Increase speed settings and alien point values
        """
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)