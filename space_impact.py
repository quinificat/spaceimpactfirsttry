import pygame

from pygame.sprite import Group
from space_impact_settings import Settings
from space_impact_ship import Ship
from space_impact_alien import Alien
from space_impact_game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

import space_impact_game_functions as sigf

def run_game():
    """
    Initialize game and create start screen.
    """
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,
         ai_settings.screen_height)
    )
    ai_settings.load_background()
    pygame.display.set_caption("Space Impact: Reenvisioned")

    # Make the play button
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store game statistics and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship.
    ship = Ship(ai_settings, screen)

    # Make a group to store bullets in
    bullets = Group()

    # Make a group to store aliens in
    aliens = Group()

    # Create group of aliens
    sigf.create_fleet(ai_settings, screen, ship, aliens)

    # Start the main loop for the game.
    while True:
        # Watch for keyboard and mouse events.
        sigf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            sigf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            sigf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
        
        sigf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()