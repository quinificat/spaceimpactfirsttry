import sys
import pygame
import os

from space_impact_settings import Settings
from space_impact_ship import Ship
from ship_bullets import Bullet
from space_impact_alien import Alien
from random import randint
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    #press key
    #downward movement
    if event.key == pygame.K_s:
        ship.moving_down = True
    #upward movement
    elif event.key == pygame.K_w:
        ship.moving_up = True
    #rightward movement
    elif event.key == pygame.K_d:
        ship.moving_right = True
    #leftward movement
    elif event.key == pygame.K_a:
        ship.moving_left = True
    #firing bullets
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_KP_ENTER:
        sys.exit()

def check_keyup_events(event, ship):
    #release key
    #downward movement
    if event.key == pygame.K_s:
        ship.moving_down = False
    #upward movement
    elif event.key == pygame.K_w:
        ship.moving_up = False
    #rightward movement
    elif event.key == pygame.K_d:
        ship.moving_right = False
    #leftward movement
    elif event.key == pygame.K_a:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """
    Respond to keyboard directional inputs.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #press key
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        #release key
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """
    Start a new game when the play button is clicked
    """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings
        ai_settings.initialize_dynamic_settings()
        
        # Hide mouse cursor
        pygame.mouse.set_visible(False)

        # Reset game stats
        stats.reset_stats()
        stats.game_active = True

        # Reset scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty lists
        aliens.empty()
        bullets.empty()

        # Create new ship or essentialy new game
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def fire_bullet(ai_settings, screen, ship, bullets):
    """
    Fire a bullet if bullet count has not been reached yet
    """
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Update position of bullets and get rid of old bullets.
    
    """
    bullets.update()
    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.left >= 1280:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Respond to bullet-alien collisions
    """
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If entire fleet is destroyed, start a new level
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def check_high_score(stats, sb):
    """
    Check to see if there's a new high score
    """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        new_high_score = str(stats.high_score)
        highscore_file = 'highscore.txt'
        store_new_high_score(highscore_file, new_high_score)
        stats.high_score = int(recall_high_score(highscore_file))

        sb.prep_high_score()
    
def store_new_high_score(highscore_file, current_game_high_score_str):
    # Store high score
    with open(highscore_file, 'w') as file_object:
        file_object.write(current_game_high_score_str)

def recall_high_score(highscore_file):
    # Recall previous high score
    if not os.path.exists(highscore_file):
        # Create the file with a default score of 0
        with open(highscore_file, 'w') as file:
            file.write("0")
    with open(highscore_file, 'r') as file:
        return file.read()

def get_number_aliens_y(ai_settings, alien_height):
    """
    Determine number of aliens that fit in a column
    """
    available_space_y = (ai_settings.screen_height - 70) - (2 * alien_height)
    number_aliens_y = int(available_space_y / (2 * alien_height))
    return number_aliens_y

def get_number_columns(ai_settings, ship_width, alien_width):
    """
    Determine the number of columns of aliens that fit the screen
    """
    available_space_x = (ai_settings.screen_width - (4 * ship_width))
    number_columns = int(available_space_x / (2 * alien_width))
    return number_columns

def create_alien(ai_settings, screen, ship, aliens, alien_number, column_number):
    """
    Create alien and place in column
    """
    alien = Alien(ai_settings, screen)
    alien_height = alien.rect.height
    alien.y = alien_height + 2 * alien_height * alien_number + 70
    alien.rect.y = alien.y
    alien.rect.x = (5 * ship.rect.width) + (2 * alien.rect.width * column_number)
    aliens.add(alien)

def check_fleet_edges(ai_settings, aliens):
    """
    Respond appropriately if any aliens have reached an edge
    """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """
    Move entire fleet left and its direction
    """
    for alien in aliens.sprites():
        alien.rect.x -= ai_settings.fleet_movespeed
    ai_settings.fleet_direction *= -1

def create_fleet(ai_settings, screen, ship, aliens):
    """
    Create fleet of aliens
    """
    alien = Alien(ai_settings, screen)
    number_aliens_y = get_number_aliens_y(ai_settings, alien.rect.height)
    number_columns = get_number_columns(ai_settings, ship.rect.width, alien.rect.width)
    for column_number in range(number_columns):
    # Pick one alien row index to skip in this column
        skip_alien = randint(0, number_aliens_y - 1)
        for alien_number in range(number_aliens_y):
            if alien_number == skip_alien:
                continue  # Skip one alien in this column
            create_alien(ai_settings, screen, ship, aliens, alien_number, column_number)

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """
    Respond to ship being hit by alien
    """
    # Reduce number of ship lives left
    if stats.ships_left > 0:
        stats.ships_left -= 1
        aliens.empty()
        bullets.empty()

        # Update scoreboard
        sb.prep_ships()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        ship.moving_right = False
        ship.moving_left = False
        
        sleep(1.0)

    else:
        # Empty the list of aliens and bullets
        stats.game_active = False
        pygame.mouse.set_visible(True)
#        aliens.empty()
#        bullets.empty()
#        ship.rect.centery = ai_settings.screen_height / 2
#        ship.rect.centerx = ai_settings.screen_width / 2

#        screen.fill(ai_settings.bg_color)
#        ship.blitme()
#        pygame.display.flip()

        # Pause
#        sleep(1.5)
#        sys.exit()

def check_aliens_left(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """
    Check if aliens have reached the left edge of the sreen
    """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.left == screen_rect.left:
            # This is an equivalent of the ship getting hit
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """
    Check if fleet is at an edge then update positions of all aliens in the fleet
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Watch out for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    
    # Check for aliens hitting the left edge of the screen
    check_aliens_left(ai_settings, stats, screen, sb, ship, aliens, bullets)

def update_screen(ai_settings, screen, stats, sb, ship, alien, bullets, play_button):
    """
    Redraw the screen during each pass through the loop.
    Update images on the screen and flip to the new screen.
    """
    if ai_settings.bg_image:
        #background image
        screen.blit(ai_settings.bg_image, (0, 0))
        # Redraw bullets behind ships and aliens
        for bullet in bullets.sprites():
            bullet.draw_bullet()
    else:
        #default background color
        screen.fill(ai_settings.bg_color)
        # Redraw bullets behind ships and aliens
        for bullet in bullets.sprites():
            bullet.draw_bullet()

    # Make the most recently drawn screen visible.
    ship.blitme()
    alien.draw(screen)

    # Draw the score information
    sb.show_score()

    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()