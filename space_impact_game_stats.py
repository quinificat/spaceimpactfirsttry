from space_impact_settings import Settings

class GameStats():
    """
    Track stats for main game
    """
    def __init__(self, ai_settings):
        """
        Initialize statistics
        """
        self.ai_settings = ai_settings
        self.reset_stats()
        
        # Start game in an active state
        self.game_active = False

        # High score should never be reset
        with open('highscore.txt', 'r') as file:
            high_score = file.read()

        self.high_score = int(high_score)

    def reset_stats(self):
        """
        Initialize statistics that can change during the game
        """
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1