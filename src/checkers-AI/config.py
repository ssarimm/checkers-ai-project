
# Game Settings
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 12
SQUARE_SIZE = WIDTH // COLS
BTN_W, BTN_H  = 350, 70
BTN_RADIUS    = 12
ICON_SIZE     = 48
GAP = 20

# Colors
RED   = (138,   3,   3)   # blood red
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
BLUE  = (  0,   0, 255)
GREY  = (90, 90, 90)
YELLOW = (255,255,  0 )
BLACK = (0, 0, 0)
HIGHLIGHT = (100, 100, 255)
TOP_COLOR    = (10, 15, 77)   # deep navy
BOTTOM_COLOR = (0, 0, 0)      # black
BTN_COLOR    = (50, 50, 50)   # dark gray
BTN_HOVER    = (80,  80,  80)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
BEIGE = (245, 245, 220)


# Performance
FPS = 60

# AI Settings
DEPTH_LIMIT  = 4
STATE_SHAPE  = (8, 12, 1)
ACTION_SIZE  = 8 * 12 * 8 * 8  # max moves from any square to any
MODEL_PATH   = "data/best_model_50.weights.h5"