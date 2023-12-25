import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

scale = 20
width, height = screen.get_width() // scale, screen.get_height() // scale

fps = 120
speed = 0.05
timer = fps * speed

cells = [[False for _ in range(height)] for _ in range(width)]
playing = False


def render():
    for x in range(len(cells)):
        for y in range(len(cells[x])):
            color = (255, 255, 255) if cells[x][y] else (0, 0, 0)
            pygame.draw.rect(screen, color, (x * scale, y * scale, scale, scale))
    pygame.display.flip()


def key_handler(keys):
    global running, playing
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_SPACE]:
        playing = not playing


def mouse_handler(pos):
    x, y = pos
    x //= scale
    y //= scale
    if 0 <= x < width and 0 <= y < height:
        cells[x][y] = not cells[x][y]


def get_neighbor_number(x_pos, y_pos):
    number = 0
    try:
        for i in range(3):
            if cells[x_pos + 1][y_pos - 1 + i]:
                number += 1
        if cells[x_pos][y_pos - 1]:
            number += 1
        if cells[x_pos][y_pos + 1]:
            number += 1
        for i in range(3):
            if cells[x_pos - 1][y_pos - 1 + i]:
                number += 1
    except:
        pass

    return number


def refresh():
    new_cells = [[False for _ in range(height)] for _ in range(width)]
    for x in range(len(cells)):
        for y in range(len(cells[x])):
            neighbors = get_neighbor_number(x, y)
            if 1 < neighbors < 4 and cells[x][y]:
                new_cells[x][y] = True
            if neighbors == 3:
                new_cells[x][y] = True
    return new_cells


def tick():
    global timer, cells
    timer -= 1
    if timer <= 0 and playing:
        new_cells = refresh()
        cells = new_cells
        timer = fps * speed


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not playing:
            mouse_handler(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            key_handler(pygame.key.get_pressed())

    tick()
    render()
    clock.tick(fps)

pygame.quit()
sys.exit()
