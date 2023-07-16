# Screen Constants
WIDTH = 860
HEIGHT = 940
GRID_WIDTH = 640
GRID_HEIGHT = 640
GRID_LEFT = 20
GRID_RIGHT = GRID_LEFT + GRID_WIDTH
GRID_TOP = 50
GRID_BOTTOM = GRID_TOP + GRID_HEIGHT
SCALE_LEFT = GRID_RIGHT + 20
SCALE_RIGHT = SCALE_LEFT + 160
SCALE_HEIGHT = 40

# Frame Rate
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIME = (205, 235, 52)
EMERALD = (110, 235, 52)
BLUE = (0, 0, 255)
SKY_BLUE = (52, 217, 235)
LIGHT_BLUE = (52, 201, 240)
ROYAL_BLUE = (52, 82, 235)
PURPLE = (110, 52, 235)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
PINK = (235, 52, 223)
STRAWBERRY = (235, 52, 98)
ORANGE = (235, 161, 52)
GRAY = (200, 200, 200)
LIGHT_GRAY = (170, 170, 170)
DARK_GRAY = (120, 120, 120)
BROWN = (150, 75, 0)
ROYAL_PURPLE = (140, 30, 60)
WHITE_SHADOW = (200, 150, 110)
BROWN_SHADOW = (170, 90, 0)

COLORS = [
    BLACK,
    WHITE,
    RED,
    GREEN,
    LIME,
    EMERALD,
    BLUE,
    SKY_BLUE,
    LIGHT_BLUE,
    ROYAL_BLUE,
    PURPLE,
    YELLOW,
    CYAN,
    MAGENTA,
    PINK,
    STRAWBERRY,
    ORANGE,
    GRAY,
    LIGHT_GRAY,
    DARK_GRAY,
    BROWN,
    ROYAL_PURPLE
]

COLOR_NAMES = [
     "Black",
     "White",
     "Red",
     "Green",
     "Lime",
     "Emerald",
     "Blue",
     "Sky Blue",
     "Light Blue",
     "Royal Blue",
     "Purple",
     "Yellow",
     "Cyan",
     "Magenta",
     "Pink",
     "Strawberry",
     "Orange",
     "Gray",
     "Light Gray",
     "Dark Gray",
     "Brown",
     "Royal Purple"
 ]

APP_ACTIONS = ["CLEAR", "FILL", "IMPORT", "EXPORT", "QUIT"]
INSTRUCTIONS = ["L-Shift: Continuous draw"]

sizes = [
    ["8x8",(692, 50), (140, 40), False, 8],
    ["16x16",(692, 90), (140, 40), False, 16],
    ["32x32",(692, 130), (140, 40), True, 32],
    ["64x64",(692, 170), (140, 40), False, 64]
]