import pygame as pg

clock = pg.time.Clock()

frames = ["F1", "F2", "F3", "F4"]

frames_length = len(frames)

FPS = 30

current_frame = 0

then = 0

while True:
    clock.tick(FPS)
    now = pg.time.get_ticks()
    if now - then > 250:
        print(now)
        then = now

        print(frames[current_frame % frames_length])
        current_frame += 1
