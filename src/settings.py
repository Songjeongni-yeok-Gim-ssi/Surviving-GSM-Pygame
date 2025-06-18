from enum import Enum, auto

# settings.py

# Game settings
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 1024
FPS = 120

# Colors
class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    LIGHT_GREEN = (144, 238, 144)  # 연한 녹색
    LIGHT_BLUE = (173, 216, 230)   # 연한 파란색
    GRAY = (128, 128, 128)         # 회색

# Screens
class GameState(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()

# Font settings
FONT_NAME = 'assets/fonts/neodgm.ttf'
FONT_SIZE = 32

# Sound settings
SOUND_VOLUME = 0.5