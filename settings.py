class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        self.game_active = False
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        
        self.laser_width = 5
        self.laser_height = 30
        self.laser_color = 255, 0, 0
        self.lasers_every = 10           # change to 1 to see faster lasers

        self.aliens_shoot_every = 120    # about every 2 seconds at 60 fps

        self.alien_point0 = 10
        self.alien_point1 = 20
        self.alien_point2 = 40
        self.ufo_point = 500

        self.ship_limit = 3         # total ships allowed in game before game over

        self.fleet_drop_speed = 1
        self.fleet_direction = 1     # change to a Vector(1, 0) move to the right, and ...
        self.fleet_direction_ufo = 1  # change to a Vector(1, 0) move to the right, and ...
        self.initialize_speed_settings()

    def initialize_speed_settings(self):
        self.alien_speed_factor = 1
        self.ufo_speed_factor = 1
        self.ship_speed_factor = 1.5
        self.laser_speed_factor = 3

    def increase_speed(self):
        scale = self.speedup_scale
        self.ship_speed_factor *= scale
        self.laser_speed_factor *= scale
