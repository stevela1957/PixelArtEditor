import pygame as pg
import numpy as np
from PIL import Image
from settings import *

pg.init()

def get_input(events, sizes, available_colors, actions):
    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            if GRID_LEFT <= pos[0] <= GRID_RIGHT and GRID_TOP <= pos[1] <= GRID_BOTTOM:
                process_grid_entry(pos)
            if pos[0] >= SCALE_LEFT and pos[0] <= SCALE_RIGHT:
                update_grid_size(pos)
            if 20 <= pos[0] <= 600 and 720 <= pos[1] <= 840:
                get_color(pos)
            if 20 <= pos[0] <= 600 and 860 <= pos[1] <= 920:
                get_actions(pos)
    create_grid(block_size)
    #print(grid_array)
    show_size_selections(sizes)
    show_colors(available_colors)
    show_actions(actions)
    create_image()

def update_grid_size(pos):
    global grid_size,block_size
    size = -1
    if pos[1] >= 50 and pos[1] < 90:
        size = 0
    if pos[1] >= 90 and pos[1] < 130:
        size = 1
    if pos[1] >= 130 and pos[1] < 170:
        size = 2
    if pos[1] >= 170 and pos[1] < 210:
        size = 3
    if size != -1:
        for ix in range(len(sizes)):
            sizes[ix][3] = False
        if 0 <= size <= len(sizes) - 1:
            sizes[size][3] = True
            grid_size = sizes[size][4]
            block_size = GRID_WIDTH // grid_size

def create_grid(block_size):
    global grid_array
    grid_array = []
    for row in range(0, GRID_HEIGHT // block_size):
        temp_arr = []
        for col in range(0, GRID_WIDTH // block_size):
            if (col + row) % 2: color = LIGHT_GRAY
            else: color = GRAY
            temp_arr.append(color)
            pg.draw.rect(screen, color, (col * block_size + 20, row * block_size + 50, block_size, block_size))
        grid_array.append(temp_arr)
def process_grid_entry(pos):
    print(f"Processing grid entry at position({pos[0]}, {pos[1]}.  Current color is {current_color}")
    # Identify block, based on current block_size

def create_grid_array():
    # Determine grid size, then create RGB list/array based on that list
    # Initial pass will be a list created with (0, 0, 0) in each grid position
    # This will then be converted via Numpy and PIL into a .png image
    # This image will be displayed in the bottom right corner of the screen display
    pass

def show_size_selections(sizes):
    for size in sizes:
        plot_rect(size[0], size[1], size[2], size[3])

def show_colors(color_palette):
    rect_x, rect_y = (40, 740)
    color_size = 30
    for color in color_palette:
        pg.draw.rect(screen, GRAY, ((rect_x - 5, rect_y - 5, color_size + 10, color_size + 10)))
        pg.draw.rect(screen, color, ((rect_x, rect_y, color_size, color_size)))
        rect_x += 50
        if rect_x >= 600:
            rect_x, rect_y = (40, rect_y + 60 )
        if rect_y > 800:
            break  # Limit to 2 rows

def get_color(pos):
    global current_color
    start_x, start_y = 40, 740
    num_cols = (GRID_WIDTH - 40) // 50
    if 735 <= pos[1] <= 775: row = 0
    else: row = 1
    col_start = (pos[0] - 40) // 50
    col_end = ((pos[0] -40) % 50)
    if col_end <= 30:
        ix = row * num_cols + col_start
        if ix < len(COLOR_NAMES):
            print(f"You selected {COLOR_NAMES[ix]}")
            current_color = COLORS[ix]

def show_actions(actions):
    rect_width = 90
    spacing = (GRID_WIDTH - rect_width * len(actions)) // (len(actions) + 1)
    start_pos = spacing
    for ix in actions:
        pg.draw.rect(screen, BLACK, (start_pos, 860, rect_width, 50), 3)
        action_name = button_font.render(ix, True, BLACK)
        screen.blit(action_name, (start_pos + (rect_width - action_name.get_width())//2, 880))
        start_pos += spacing + rect_width

def get_actions(pos):
    global active, block_size, current_color
    rect_width = 90
    spacing = (GRID_WIDTH - rect_width * len(APP_ACTIONS)) // (len(APP_ACTIONS) + 1)
    start_pos = spacing
    col = (pos[0] - start_pos) // (rect_width + spacing)
    col_end = (pos[0] - start_pos) % (rect_width + spacing)
    if col_end <= 90:
        if APP_ACTIONS[col] == "QUIT": active = False
        if APP_ACTIONS[col] == "CLEAR":
            print("Clearing grid")
            create_grid(block_size)
            current_color = (0, 0, 0)
        if APP_ACTIONS[col] == "FILL": print("You chose 'FILL'")
        if APP_ACTIONS[col] == "IMPORT": print("You chose 'IMPORT'")
        if APP_ACTIONS[col] == "EXPORT": print("You chose 'EXPORT'")

def create_image():
    array = np.array(grid_array, dtype=np.uint8)
    img = Image.fromarray(array)
    img.save('pixel_img.png')
    pixel_image = pg.transform.scale(pg.image.load('pixel_img.png'), (200, 200))
    screen.blit(pixel_image, (640, 720))

def plot_rect(text, pos, size, selected):
    label = title_font.render(text, True, BLACK)
    if selected: color = CYAN
    else: color = LIGHT_GRAY
    pg.draw.rect(screen, color, (pos[0], pos[1], size[0], size[1]))
    screen.blit(label, (pos[0] + 20, pos[1] + 5))

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Pixel Art Editor")

button_font = pg.font.Font(None, 30)
title_font = pg.font.Font(None, 50)
app_title = title_font.render("PIXEL ART EDITOR", True, ROYAL_PURPLE)

clock = pg.time.Clock()

# App variables
grid_size = 32
current_color = (255, 255, 255)
block_size = GRID_WIDTH // grid_size
grid_array = []
sizes = [
    ["8x8",(680, 50), (140, 40), False, 8],
    ["16x16",(680, 90), (140, 40), False, 16],
    ["32x32",(680, 130), (140, 40), True, 32],
    ["64x64",(680, 170), (140, 40), False, 64]
]

active = True

while active:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            active = False

    screen.fill(DARK_GRAY)
    screen.blit(app_title, (WIDTH/2 - app_title.get_width()/2, 10))
    get_input(events, sizes, COLORS, APP_ACTIONS)
    pg.display.update()
    clock.tick(FPS)

pg.quit()
