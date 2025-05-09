from enum import Enum

# settings.py

# Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
class Color(Enum):
  WHITE = (255, 255, 255)
  BLACK = (0, 0, 0)
  RED = (255, 0, 0)
  GREEN = (0, 255, 0)
  BLUE = (0, 0, 255)

# Font settings
FONT_NAME = 'arial'
FONT_SIZE = 32

# Sound settings
SOUND_VOLUME = 0.5