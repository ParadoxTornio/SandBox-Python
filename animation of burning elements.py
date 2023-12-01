import pygame

pygame.init()

WIDTH = 316
HEIGHT = 208

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test animations")

pygame.init()

ld_1_1 = pygame.image.load(
    'images/oak burning frames/left down/burning oak frame 1_1.png')
ld_1_2 = pygame.image.load(
    'images/oak burning frames/left down/burning oak frame 1_2.png')
ld_1_3 = pygame.image.load(
    'images/oak burning frames/left down/burning oak frame 1_3.png')
ld_2_1 = pygame.image.load(
    'images/oak burning frames/left down/burning oak frame 2_1.png')
ld_2_2 = pygame.image.load(
    'images/oak burning frames/left down/burning oak frame 2_2.png')
ld_2_3 = pygame.image.load(
    'images/oak burning frames/left down/burning oak frame 2_3.png')
ld_3_1 = pygame.image.load(
    'images/oak burning frames/left down/burning oak frame 3_1.png')
ld_3_2 = pygame.image.load(
    'images/oak burning frames/left down/burning oak frame 3_2.png')
ld_3_3 = pygame.image.load(
    'images/oak burning frames/left down/burning oak frame 3_3.png')

lu_1_1 = pygame.image.load(
    'images/oak burning frames/left up/burning oak frame 1_1.png')
lu_1_2 = pygame.image.load(
    'images/oak burning frames/left up/burning oak frame 1_2.png')
lu_1_3 = pygame.image.load(
    'images/oak burning frames/left up/burning oak frame 1_3.png')
lu_2_1 = pygame.image.load(
    'images/oak burning frames/left up/burning oak frame 2_1.png')
lu_2_2 = pygame.image.load(
    'images/oak burning frames/left up/burning oak frame 2_2.png')
lu_2_3 = pygame.image.load(
    'images/oak burning frames/left up/burning oak frame 2_3.png')
lu_3_1 = pygame.image.load(
    'images/oak burning frames/left up/burning oak frame 3_1.png')
lu_3_2 = pygame.image.load(
    'images/oak burning frames/left up/burning oak frame 3_2.png')
lu_3_3 = pygame.image.load(
    'images/oak burning frames/left up/burning oak frame 3_3.png')

rd_1_1 = pygame.image.load(
    'images/oak burning frames/right down/burning oak frame 1_1.png')
rd_1_2 = pygame.image.load(
    'images/oak burning frames/right down/burning oak frame 1_2.png')
rd_1_3 = pygame.image.load(
    'images/oak burning frames/right down/burning oak frame 1_3.png')
rd_2_1 = pygame.image.load(
    'images/oak burning frames/right down/burning oak frame 2_1.png')
rd_2_2 = pygame.image.load(
    'images/oak burning frames/right down/burning oak frame 2_2.png')
rd_2_3 = pygame.image.load(
    'images/oak burning frames/right down/burning oak frame 2_3.png')
rd_3_1 = pygame.image.load(
    'images/oak burning frames/right down/burning oak frame 3_1.png')
rd_3_2 = pygame.image.load(
    'images/oak burning frames/right down/burning oak frame 3_2.png')
rd_3_3 = pygame.image.load(
    'images/oak burning frames/right down/burning oak frame 3_3.png')

ru_1_1 = pygame.image.load(
    'images/oak burning frames/right up/burning oak frame 1_1.png')
ru_1_2 = pygame.image.load(
    'images/oak burning frames/right up/burning oak frame 1_2.png')
ru_1_3 = pygame.image.load(
    'images/oak burning frames/right up/burning oak frame 1_3.png')
ru_2_1 = pygame.image.load(
    'images/oak burning frames/right up/burning oak frame 2_1.png')
ru_2_2 = pygame.image.load(
    'images/oak burning frames/right up/burning oak frame 2_2.png')
ru_2_3 = pygame.image.load(
    'images/oak burning frames/right up/burning oak frame 2_3.png')
ru_3_1 = pygame.image.load(
    'images/oak burning frames/right up/burning oak frame 3_1.png')
ru_3_2 = pygame.image.load(
    'images/oak burning frames/right up/burning oak frame 3_2.png')
ru_3_3 = pygame.image.load(
    'images/oak burning frames/right up/burning oak frame 3_3.png')


ld_n_1_1 = pygame.image.load(
    'images/oak frames/left down/burning oak frame 1_1.png')
ld_n_1_2 = pygame.image.load(
    'images/oak frames/left down/burning oak frame 1_2.png')
ld_n_1_3 = pygame.image.load(
    'images/oak frames/left down/burning oak frame 1_3.png')
ld_n_2_1 = pygame.image.load(
    'images/oak frames/left down/burning oak frame 2_1.png')
ld_n_2_2 = pygame.image.load(
    'images/oak frames/left down/burning oak frame 2_2.png')
ld_n_2_3 = pygame.image.load(
    'images/oak frames/left down/burning oak frame 2_3.png')
ld_n_3_1 = pygame.image.load(
    'images/oak frames/left down/burning oak frame 3_1.png')
ld_n_3_2 = pygame.image.load(
    'images/oak frames/left down/burning oak frame 3_2.png')
ld_n_3_3 = pygame.image.load(
    'images/oak frames/left down/burning oak frame 3_3.png')

lu_n_1_1 = pygame.image.load(
    'images/oak frames/left up/burning oak frame 1_1.png')
lu_n_1_2 = pygame.image.load(
    'images/oak frames/left up/burning oak frame 1_2.png')
lu_n_1_3 = pygame.image.load(
    'images/oak frames/left up/burning oak frame 1_3.png')
lu_n_2_1 = pygame.image.load(
    'images/oak frames/left up/burning oak frame 2_1.png')
lu_n_2_2 = pygame.image.load(
    'images/oak frames/left up/burning oak frame 2_2.png')
lu_n_2_3 = pygame.image.load(
    'images/oak frames/left up/burning oak frame 2_3.png')
lu_n_3_1 = pygame.image.load(
    'images/oak frames/left up/burning oak frame 3_1.png')
lu_n_3_2 = pygame.image.load(
    'images/oak frames/left up/burning oak frame 3_2.png')
lu_n_3_3 = pygame.image.load(
    'images/oak frames/left up/burning oak frame 3_3.png')

rd_n_1_1 = pygame.image.load(
    'images/oak frames/right down/burning oak frame 1_1.png')
rd_n_1_2 = pygame.image.load(
    'images/oak frames/right down/burning oak frame 1_2.png')
rd_n_1_3 = pygame.image.load(
    'images/oak frames/right down/burning oak frame 1_3.png')
rd_n_2_1 = pygame.image.load(
    'images/oak frames/right down/burning oak frame 2_1.png')
rd_n_2_2 = pygame.image.load(
    'images/oak frames/right down/burning oak frame 2_2.png')
rd_n_2_3 = pygame.image.load(
    'images/oak frames/right down/burning oak frame 2_3.png')
rd_n_3_1 = pygame.image.load(
    'images/oak frames/right down/burning oak frame 3_1.png')
rd_n_3_2 = pygame.image.load(
    'images/oak frames/right down/burning oak frame 3_2.png')
rd_n_3_3 = pygame.image.load(
    'images/oak frames/right down/burning oak frame 3_3.png')

ru_n_1_1 = pygame.image.load(
    'images/oak frames/right up/burning oak frame 1_1.png')
ru_n_1_2 = pygame.image.load(
    'images/oak frames/right up/burning oak frame 1_2.png')
ru_n_1_3 = pygame.image.load(
    'images/oak frames/right up/burning oak frame 1_3.png')
ru_n_2_1 = pygame.image.load(
    'images/oak frames/right up/burning oak frame 2_1.png')
ru_n_2_2 = pygame.image.load(
    'images/oak frames/right up/burning oak frame 2_2.png')
ru_n_2_3 = pygame.image.load(
    'images/oak frames/right up/burning oak frame 2_3.png')
ru_n_3_1 = pygame.image.load(
    'images/oak frames/right up/burning oak frame 3_1.png')
ru_n_3_2 = pygame.image.load(
    'images/oak frames/right up/burning oak frame 3_2.png')
ru_n_3_3 = pygame.image.load(
    'images/oak frames/right up/burning oak frame 3_3.png')

ld_counter = 0
lu_counter = 0
rd_counter = 0
ru_counter = 0

ld_counter_n = 0
lu_counter_n = 0
rd_counter_n = 0
ru_counter_n = 0


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    if ld_counter < 100:
        screen.blit(ld_1_1, (25, 25))
    elif ld_counter < 200:
        screen.blit(ld_1_2, (25, 25))
    else:
        screen.blit(ld_1_3, (25, 25))

    if ld_counter < 100:
        screen.blit(ld_2_1, (75, 25))
    elif ld_counter < 200:
        screen.blit(ld_2_2, (75, 25))
    else:
        screen.blit(ld_2_3, (75, 25))

    if ld_counter < 100:
        screen.blit(ld_3_1, (125, 25))
    elif ld_counter < 200:
        screen.blit(ld_3_2, (125, 25))
    else:
        screen.blit(ld_3_3, (125, 25))

    if lu_counter < 100:
        screen.blit(lu_1_1, (25, 75))
    elif lu_counter < 200:
        screen.blit(lu_1_2, (25, 75))
    else:
        screen.blit(lu_1_3, (25, 75))

    if lu_counter < 100:
        screen.blit(lu_2_1, (75, 75))
    elif lu_counter < 200:
        screen.blit(lu_2_2, (75, 75))
    else:
        screen.blit(lu_2_3, (75, 75))

    if lu_counter < 100:
        screen.blit(lu_3_1, (125, 75))
    elif lu_counter < 200:
        screen.blit(lu_3_2, (125, 75))
    else:
        screen.blit(lu_3_3, (125, 75))

    if ru_counter < 100:
        screen.blit(ru_1_1, (25, 125))
    elif ru_counter < 200:
        screen.blit(ru_1_2, (25, 125))
    else:
        screen.blit(ru_1_3, (25, 125))

    if ru_counter < 100:
        screen.blit(ru_2_1, (75, 125))
    elif ru_counter < 200:
        screen.blit(ru_2_2, (75, 125))
    else:
        screen.blit(ru_2_3, (75, 125))

    if ru_counter < 100:
        screen.blit(ru_3_1, (125, 125))
    elif ru_counter < 200:
        screen.blit(ru_3_2, (125, 125))
    else:
        screen.blit(ru_3_3, (125, 125))

    if rd_counter < 100:
        screen.blit(rd_1_1, (25, 175))
    elif rd_counter < 200:
        screen.blit(rd_1_2, (25, 175))
    else:
        screen.blit(rd_1_3, (25, 175))

    if rd_counter < 100:
        screen.blit(rd_2_1, (75, 175))
    elif rd_counter < 200:
        screen.blit(rd_2_2, (75, 175))
    else:
        screen.blit(rd_2_3, (75, 175))

    if rd_counter < 100:
        screen.blit(rd_3_1, (125, 175))
    elif rd_counter < 200:
        screen.blit(rd_3_2, (125, 175))
    else:
        screen.blit(rd_3_3, (125, 175))

    if ld_counter < 100:
        screen.blit(ld_n_1_1, (175, 25))
    elif ld_counter < 200:
        screen.blit(ld_n_1_2, (175, 25))
    else:
        screen.blit(ld_n_1_3, (175, 25))

    if ld_counter < 100:
        screen.blit(ld_n_2_1, (225, 25))
    elif ld_counter < 200:
        screen.blit(ld_n_2_2, (225, 25))
    else:
        screen.blit(ld_n_2_3, (225, 25))

    if ld_counter < 100:
        screen.blit(ld_n_3_1, (275, 25))
    elif ld_counter < 200:
        screen.blit(ld_n_3_2, (275, 25))
    else:
        screen.blit(ld_n_3_3, (275, 25))

    if lu_counter < 100:
        screen.blit(lu_n_1_1, (175, 75))
    elif lu_counter < 200:
        screen.blit(lu_n_1_2, (175, 75))
    else:
        screen.blit(lu_n_1_3, (175, 75))

    if lu_counter < 100:
        screen.blit(lu_n_2_1, (225, 75))
    elif lu_counter < 200:
        screen.blit(lu_n_2_2, (225, 75))
    else:
        screen.blit(lu_n_2_3, (225, 75))

    if lu_counter < 100:
        screen.blit(lu_n_3_1, (275, 75))
    elif lu_counter < 200:
        screen.blit(lu_n_3_2, (275, 75))
    else:
        screen.blit(lu_n_3_3, (275, 75))

    if ru_counter < 100:
        screen.blit(ru_n_1_1, (175, 125))
    elif ru_counter < 200:
        screen.blit(ru_n_1_2, (175, 125))
    else:
        screen.blit(ru_n_1_3, (175, 125))

    if ru_counter < 100:
        screen.blit(ru_n_2_1, (225, 125))
    elif ru_counter < 200:
        screen.blit(ru_n_2_2, (225, 125))
    else:
        screen.blit(ru_n_2_3, (225, 125))

    if ru_counter < 100:
        screen.blit(ru_n_3_1, (275, 125))
    elif ru_counter < 200:
        screen.blit(ru_n_3_2, (275, 125))
    else:
        screen.blit(ru_n_3_3, (275, 125))

    if rd_counter < 100:
        screen.blit(rd_n_1_1, (175, 175))
    elif rd_counter < 200:
        screen.blit(rd_n_1_2, (175, 175))
    else:
        screen.blit(rd_n_1_3, (175, 175))

    if rd_counter < 100:
        screen.blit(rd_n_2_1, (225, 175))
    elif rd_counter < 200:
        screen.blit(rd_n_2_2, (225, 175))
    else:
        screen.blit(rd_n_2_3, (225, 175))

    if rd_counter < 100:
        screen.blit(rd_n_3_1, (275, 175))
    elif rd_counter < 200:
        screen.blit(rd_n_3_2, (275, 175))
    else:
        screen.blit(rd_n_3_3, (275, 175))

    pygame.display.flip()
    ld_counter_n += 0.05
    if ld_counter_n >= 300:
        ld_counter_n = 0
    lu_counter_n += 0.05
    if lu_counter_n >= 300:
        lu_counter_n = 0
    rd_counter_n += 0.05
    if rd_counter_n >= 300:
        rd_counter_n = 0
    ru_counter_n += 0.05
    if ru_counter_n >= 300:
        ru_counter_n = 0

    ld_counter += 0.05
    if ld_counter >= 300:
        ld_counter = 0
    lu_counter += 0.05
    if lu_counter >= 300:
        lu_counter = 0
    rd_counter += 0.05
    if rd_counter >= 300:
        rd_counter = 0
    ru_counter += 0.05
    if ru_counter >= 300:
        ru_counter = 0

pygame.quit()
