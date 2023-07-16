import pygame as pg
import numpy as np
from PIL import Image
import os
import shutil
from settings import *

pg.init()
pg.mixer.init()

def get_input(events, sizes):
    global fill, lshift_locked
    pos = pg.mouse.get_pos()
    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            if GRID_LEFT <= pos[0] <= GRID_RIGHT and GRID_TOP <= pos[1] <= GRID_BOTTOM:
                process_grid_entry(pos)
            if pos[0] >= SCALE_LEFT and pos[0] <= SCALE_RIGHT:
                update_grid_size(pos)
            if 20 <= pos[0] <= 620 and 720 <= pos[1] <= 840:
                get_color(pos)
            if 20 <= pos[0] <= 600 and 860 <= pos[1] <= 920:
                get_actions(pos)
        if event.type == pg.MOUSEBUTTONUP:
            fill = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LSHIFT:
                lshift_locked = not lshift_locked
    if lshift_locked and GRID_LEFT <= pos[0] <= GRID_RIGHT and GRID_TOP <= pos[1] <= GRID_BOTTOM:
        process_grid_entry(pos)

def update_grid_size(pos):
    global grid_size,block_size, grid_array
    size = -1
    scale_found = False
    while not scale_found:
        for ix in range(len(sizes)):
            if GRID_TOP + (ix * SCALE_HEIGHT) <= pos[1] < GRID_TOP + (ix * SCALE_HEIGHT) + SCALE_HEIGHT:
                size = ix
                scale_found = True
    if size != -1:
        for ix in range(len(sizes)):
            sizes[ix][3] = False
        if 0 <= size <= len(sizes) - 1:
            sizes[size][3] = True
            grid_size = sizes[size][4]
            block_size = GRID_WIDTH // grid_size
            create_grid(False)

def create_grid(fill):
    global grid_array
    grid_array = []
    for row in range(0, GRID_HEIGHT // block_size):
        temp_arr = []
        for col in range(0, GRID_WIDTH // block_size):
            if fill:
                color = current_color
            else:
                if (col + row) % 2: color = LIGHT_GRAY
                else: color = GRAY
            temp_arr.append(color)
        grid_array.append(temp_arr)

def show_grid():
    for row in range(0, GRID_HEIGHT // block_size):
        for col in range(0, GRID_WIDTH // block_size):
            if fill:
                pg.draw.rect(screen, LIGHT_GRAY,(col * block_size + 20, row * block_size + 50, block_size, block_size),1)
                pg.draw.rect(screen, current_color, (col * block_size + 20, row * block_size + 50, block_size-3, block_size-3))
            else:
                pg.draw.rect(screen, grid_array[row][col], (col * block_size + 20, row * block_size + 50, block_size, block_size))
        for ix in range(0, GRID_WIDTH + block_size, block_size):
            pg.draw.line(screen, WHITE_SHADOW, (GRID_LEFT + ix, GRID_TOP), (GRID_LEFT + ix, GRID_BOTTOM), 1)
            pg.draw.line(screen, WHITE_SHADOW, (GRID_LEFT, GRID_TOP + ix), (GRID_RIGHT, GRID_TOP + ix), 1)

def process_grid_entry(pos):
    global grid_array
    col = (pos[0] - GRID_LEFT) // block_size
    row = (pos[1] - GRID_TOP) // block_size
    block_x = col * block_size + GRID_LEFT
    block_y = row * block_size + GRID_TOP
    grid_array[row][col] = current_color
    pg.draw.rect(screen, current_color, (block_x, block_y, block_size, block_size))
    show_grid()

def show_size_selections(sizes):
    for size in sizes:
        plot_rect(size[0], size[1], size[2], size[3])

def show_keycontrols():
    global lshift_locked
    for instruction in INSTRUCTIONS:
        instr = instruction_font.render(instruction, True, BLACK)
        screen.blit(instr, (680, 240))
    if lshift_locked: state = "On"
    else: state = "Off"
    lock = instruction_font.render(f"Left Shift Lock: {state}", True, BLACK)
    screen.blit(lock, (680, 282))
def show_colors(color_palette):
    rect_x, rect_y = (40, 740)
    color_size = 30
    for color in color_palette:
        if color == current_color:
            pg.draw.rect(screen, BROWN_SHADOW, ((rect_x - 5, rect_y - 5, color_size + 10, color_size + 10)))
        else:
            pg.draw.rect(screen, GRAY, ((rect_x - 5, rect_y - 5, color_size + 10, color_size + 10)))
        pg.draw.rect(screen, color, ((rect_x, rect_y, color_size, color_size)))
        rect_x += 50
        if rect_x >= 620:
            rect_x, rect_y = (40, rect_y + 60 )
        if rect_y > 800:
            break  # Limit to 2 rows

def get_color(pos):
    global current_color
    num_cols = (GRID_WIDTH - 40) // 50
    if 735 <= pos[1] <= 775: row = 0
    else: row = 1
    col_start = (pos[0] - 40) // 50
    col_end = ((pos[0] -40) % 50)
    if col_end <= 30:
        ix = row * num_cols + col_start
        if ix < len(COLOR_NAMES):
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
    global active, block_size, fill, current_color
    rect_width = 90
    spacing = (GRID_WIDTH - rect_width * len(APP_ACTIONS)) // (len(APP_ACTIONS) + 1)
    start_pos = spacing
    col = (pos[0] - start_pos) // (rect_width + spacing)
    col_end = (pos[0] - start_pos) % (rect_width + spacing)
    if col_end <= 90:
        if APP_ACTIONS[col] == "QUIT": active = False
        if APP_ACTIONS[col] == "CLEAR": fill = False; create_grid(fill)
        if APP_ACTIONS[col] == "FILL": fill = True; create_grid(fill); fill = False
        if APP_ACTIONS[col] == "IMPORT": import_image()
        if APP_ACTIONS[col] == "EXPORT": export_image()

def create_image():
    array = np.array(grid_array, dtype=np.uint8)
    img = Image.fromarray(array)
    img.save('pixel_img.png')
    pixel_image = pg.transform.scale(pg.image.load('pixel_img.png'), (200, 200))
    screen.blit(pixel_image, (642, 710))

def import_image():
    global grid_array
    filename = display_image_request("Import")
    print(filename)
    img = Image.open(filename)
    img = img.transpose(Image.ROTATE_90)
    pixels = img.load()  # this is not a list, nor is it list()'able
    width, height = img.size
    grid_array = []
    for x in range(width):
        temp_array = []
        for y in range(height):
            temp_array.append(pixels[x, y])
        grid_array.append(temp_array)

def export_image():
    export_name = display_image_request("Export")
    shutil.copy("pixel_img.png", export_name)
    create_grid(False)

def display_image_request(process):
    global grid_size, block_size
    text_in = False
    user_entry = ""
    pass_criteria = False
    while not text_in and pass_criteria == False:
        create_grid(True)
        label = button_font.render(f"{process} image name? {user_entry}", True, BLACK)
        screen.blit(label, (40, 150))
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if user_entry != "":
                        if process == "Import":
                            if user_entry in os.listdir('.'):
                                img = Image.open(user_entry)
                                if img.width <= 64 and img.height <= 64:
                                    print(f"Valid import. Filename {user_entry} ")
                                    grid_size = img.width
                                    block_size = GRID_WIDTH // grid_size
                                    img.close()
                                    for ix in range(len(sizes)):
                                        if grid_size == sizes[ix][4]:
                                            sizes[ix][3] = True
                                        else:
                                            sizes[ix][3] = False
                                    show_size_selections(sizes)
                                    text_in = True
                                    pass_criteria = True
                        elif process == "Export":
                            entry = user_entry.split(".")
                            print(entry)
                            if entry[0].isalpha():
                                if len(entry) == 1:
                                    user_entry += ".png"
                                text_in = True
                                pass_criteria = True
                        if not pass_criteria:
                            error.play()
                            user_entry = ""
                            print("Incorrect entry")
                            screen.fill(DARK_GRAY)
                            screen.blit(app_title, (WIDTH / 2 - app_title.get_width() / 2, 10))
                else:
                    user_entry += event.unicode
    return user_entry

def plot_rect(text, pos, size, selected):
    label = title_font.render(text, True, BLACK)
    if selected: color = CYAN
    else: color = LIGHT_GRAY
    pg.draw.rect(screen, color, (pos[0], pos[1], size[0], size[1]))
    screen.blit(label, (pos[0] + 20, pos[1] + 5))

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Pixel Art Editor")

instruction_font = pg.font.Font(None, 20)
button_font = pg.font.Font(None, 30)
title_font = pg.font.Font(None, 50)
app_title = title_font.render("PIXEL ART EDITOR", True, BLUE)
error = pg.mixer.Sound('error.wav')

# App variables
grid_size = 32
block_size = GRID_WIDTH // grid_size
fill = False
lshift_locked = False
current_color = WHITE

create_grid(False)
clock = pg.time.Clock()
active = True
while active:
    events = pg.event.get()
    screen.fill(DARK_GRAY)
    screen.blit(app_title, (WIDTH/2 - app_title.get_width()/2, 10))
    get_input(events, sizes)
    show_grid()
    show_size_selections(sizes)
    show_keycontrols()
    show_colors(COLORS)
    show_actions(APP_ACTIONS)
    create_image()
    pg.display.update()
    clock.tick(FPS)

pg.quit()
