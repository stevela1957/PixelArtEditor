import pygame as pg
from settings import *

pg.init()

def get_input(events, sizes, available_colors):
    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            if pos[0] >= 680 and pos[0] <= 840:
                update_grid_size(pos)
            if 20 <= pos[0] <= 600 and 720 <= pos[1] <= 840:
                print("Selecting color")
            if 20 <= pos[0] <= 600 and 860 <= pos[1] <= 920:
                print("Selecting action")
    create_grid(block_size)
    show_size_selections(sizes)
    show_colors(available_colors)
    show_actions()

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
    for row in range(0, GRID_HEIGHT // block_size):
        for col in range(0, GRID_WIDTH // block_size):
            if (col + row) % 2: color = LIGHT_GRAY
            else: color = GRAY
            pg.draw.rect(screen, color, (col * block_size + 20, row * block_size + 50, block_size, block_size))

def show_size_selections(sizes):
    for size in sizes:
        plot_rect(size[0], size[1], size[2], size[3])

def show_colors(available_colors):
    rect_x, rect_y = (40, 740)
    color_size = 30
    for color in available_colors:
        pg.draw.rect(screen, GRAY, ((rect_x - 5, rect_y - 5, color_size + 10, color_size + 10)))
        pg.draw.rect(screen, color, ((rect_x, rect_y, color_size, color_size)))
        rect_x += 45
        if rect_x >= 600:
            rect_x, rect_y = (40, rect_y + 60 )
        if rect_y > 800:
            break  # Limit to 2 rows

def show_actions():
    pass

def plot_rect(text, pos, size, selected):
    label = title_font.render(text, True, BLACK)
    if selected: color = CYAN
    else: color = LIGHT_GRAY
    pg.draw.rect(screen, color, (pos[0], pos[1], size[0], size[1]))
    screen.blit(label, (pos[0] + 20, pos[1] + 5))

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Pixel Art Editor")

button_font = pg.font.Font(None, 20)
title_font = pg.font.Font(None, 50)
app_title = title_font.render("PIXEL ART EDITOR", True, GREEN)

clock = pg.time.Clock()

# App variables
grid_size = 32
block_size = GRID_WIDTH // grid_size
sizes = [
    ["8x8",(680, 50), (140, 40), False, 8],
    ["16x16",(680, 90), (140, 40), False, 16],
    ["32x32",(680, 130), (140, 40), True, 32],
    ["64x64",(680, 170), (140, 40), False, 64]
]
available_colors = [BLACK, WHITE, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, xxx, xxx, xxx, \
                    xxx, xxx, xxx, xxx, xxx, xxx, xxx]

active = True

while active:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            active = False

    screen.fill(DARK_GRAY)
    screen.blit(app_title, (WIDTH/2 - app_title.get_width()/2, 10))
    #pg.draw.rect(screen, BLUE, (20, 720, 580, 120), 3)
    pg.draw.rect(screen, CYAN, (20, 860, 580, 60), 3)
    pg.draw.rect(screen, MAGENTA, (620, 720, 200, 200), 3)
    get_input(events, sizes, available_colors)
    pg.display.update()

pg.quit()
