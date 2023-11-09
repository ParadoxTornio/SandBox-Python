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

pymunk.pygame_util.positive_y_is_up = False
space = pymunk.Space()
space.gravity = 0.0, 900.0

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
        space.static_body, (x_cord, y_cord + BLOCK_SIZE),
        (x_cord + BLOCK_SIZE, y_cord + BLOCK_SIZE), BLOCK_SIZE)
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                water.append(create_water(space, event.pos))
            elif event.button == 3:
                metal.append(create_metal(space, event.pos))

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
        x, y = metal_shape.a[0], metal_shape.a[1] - BLOCK_SIZE
        metal_surface = pygame.Surface((8, 8))
        metal_surface.blit(metal_image, (0, 0))
        screen.blit(metal_surface, (x, y))

    pygame.display.flip()
    clock.tick(FPS)


# Модуль  pymunk.pygame_util  предоставляет класс  drawOptions ,
# который может быть использован для отрисовки объектов
# физического пространства Pymunk в окне Pygame.
# Вот пример использования  drawOptions :



# python
# import pygame
# import pymunk
# from pymunk.pygame_util import draw_options

# pygame.init()

# screen = pygame.display.set_mode((800, 600))

# space = pymunk.Space()
# space.gravity = (0, -900)

# body = pymunk.Body(1, 100)
# body.position = (400, 300)
# shape = pymunk.Circle(body, 30)
# space.add(body, shape)

# options = draw_options.DrawOptions(screen)

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     screen.fill((255, 255, 255))

#     space.debug_draw(options)

#     pygame.display.flip()

#     space.step(1 / 60)

# pygame.quit()



# В этом примере мы создаем окно размером 800x600 пикселей и физическое
# пространство  space . Затем мы создаем объект  drawOptions  и передаем в
# него наше окно  screen . В основном цикле программы мы очищаем экран,
# вызываем метод  debug_draw()  объекта  space , который отрисовывает
# объекты физического пространства с использованием  drawOptions ,
# и обновляем экран.
#  drawOptions  предоставляет различные параметры и методы для настройки
# отображения объектов физического пространства, такие как цвета,
# масштабирование и т. д. Вы можете ознакомиться с документацией Pymunk,
# чтобы узнать больше о возможностях  drawOptions .
