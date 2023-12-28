import pygame
from os import listdir


class LoadMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background_image = pygame.image.load('images/load_menu.png')
        self.red_diskette_image = pygame.image.load('images/diskette_red.png')
        self.surfaces = []
        files = listdir('saves')
        for i in range(6):
            surface = pygame.Surface((418, 278))
            surface.blit(self.red_diskette_image, (181, 114))
            self.surfaces.append(surface)
        for name in files:
            if name != 'game.save':
                number_of_file = int(name[0])
                image = pygame.image.load(
                    f'images/saved_screenshots/{number_of_file}.png')
                self.surfaces[number_of_file - 1].blit(image, )
