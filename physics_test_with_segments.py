import pygame
import pymunk
import pymunk.pygame_util

WIDTH = 1280
HEIGHT = 660
FPS = 60
DT = 1.0 / FPS
BLOCK_SIZE = 8

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
options = pymunk.pygame_util.DrawOptions(screen)

pymunk.pygame_util.positive_y_is_up = False
space = pymunk.Space()
space.gravity = 0.0, 900.0
draw_options = False

walls = []
metal = []
water = []

metal_image = pygame.image.load('images/metal_frame.png')
water_image = pygame.image.load('images/water_frame_2.png')

segment_floor = pymunk.Segment(
    space.static_body, (1, HEIGHT), (WIDTH, HEIGHT), 10)

segment_left_wall = pymunk.Segment(
    space.static_body, (1, 0), (1, HEIGHT), 10)

segment_right_wall = pymunk.Segment(
    space.static_body, (WIDTH - 11, 0), (WIDTH - 11, HEIGHT), 10)

space.add(segment_floor)
space.add(segment_left_wall)
space.add(segment_right_wall)

walls.append(segment_floor)
walls.append(segment_left_wall)
walls.append(segment_right_wall)


def create_metal(space, mouse_pos):
    x_cord = mouse_pos[0] // 8 * 8
    y_cord = mouse_pos[1] // 8 * 8
    metal_block = pymunk.Segment(
        space.static_body,
        (x_cord + BLOCK_SIZE // 2, y_cord + BLOCK_SIZE // 2 - 1),
        (x_cord + BLOCK_SIZE // 2, y_cord + BLOCK_SIZE // 2 + 1),
        BLOCK_SIZE // 2 - 1)
    metal_block.x_cord = x_cord
    metal_block.y_cord = y_cord
    space.add(metal_block)
    return metal_block


def create_water(space, mouse_pos):
    water_body = pymunk.Body(10, 100)
    water_body.position = mouse_pos
    water_shape = pymunk.Circle(water_body, 5, (0, 0))
    space.add(water_body, water_shape)
    return water_shape


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 1:
        #         water.append(create_water(space, event.pos))
        #     elif event.button == 3:
        #         metal.append(create_metal(space, event.pos))
    if pygame.mouse.get_pressed()[2]:
        metal.append(create_metal(space, pygame.mouse.get_pos()))
    if pygame.mouse.get_pressed()[0]:
        for i in range(10):
            water.append(create_water(space, pygame.mouse.get_pos()))

    space.step(DT)
    screen.fill(pygame.Color("white"))

    for water_shape in water:
        radius = water_shape.radius
        x, y = water_shape.body.position[0], water_shape.body.position[1]
        water_surface = pygame.Surface((16, 16))
        water_surface.blit(water_image, (0, 0))
        screen.blit(water_surface, (x - 8, y - 8))

    for metal_shape in metal:
        radius = metal_shape.radius
        x, y = metal_shape.x_cord, metal_shape.y_cord
        metal_surface = pygame.Surface((8, 8))
        metal_surface.blit(metal_image, (0, 0))
        screen.blit(metal_surface, (x, y))

    key = pygame.key.get_pressed()

    if key[pygame.K_d]:
        draw_options = True

    elif key[pygame.K_s]:
        draw_options = False

    if draw_options:
        space.debug_draw(options)
        pygame.display.flip()

    pygame.display.flip()
    pygame.display.set_caption(f'{clock.get_fps()} quantity:{len(water)}')
    clock.tick(FPS)
