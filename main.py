import pygame as pg
from settings import *

pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Pixel Art Editor")

button_font = pg.font.Font(None, 20)
title_font = pg.font.Font(None, 50)
app_title = title_font.render("PIXEL ART EDITOR", True, BLACK)

clock = pg.time.Clock()

active = True

while active:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            active = False

    screen.fill(GRAY)
    screen.blit(app_title, (WIDTH/2 - app_title.get_width()/2, 10))
    pg.draw.rect(screen, RED, (20, 50, 640, 640),3)
    pg.draw.rect(screen, GREEN, (680, 50, 140, 640), 3)
    pg.draw.rect(screen, BLUE, (20, 720, 580, 120), 3)
    pg.draw.rect(screen, CYAN, (20, 860, 580, 60), 3)
    pg.draw.rect(screen, MAGENTA, (620, 720, 200, 200), 3)
    pg.display.update()

pg.quit()
