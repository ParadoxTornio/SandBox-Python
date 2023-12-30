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
            surface = pygame.Surface((410, 270))
            surface.blit(self.red_diskette_image, (180, 110))
            self.surfaces.append(surface)
        for name in files:
            if name != 'game.save':
                number_of_file = int(name[0])
                image = pygame.image.load(
                    f'images/saved_screenshots/{number_of_file}.png')
                w = image.get_width()
                h = image.get_height()
                new_image = image
                if w >= 410:
                    if h >= 270:
                        new_image = pygame.transform.scale(
                            image, (w // 2, h // 2))
                elif w <= 205:
                    if h <= 135:
                        new_image = pygame.transform.scale(
                            image, (w * 2, h * 2))
                elif w <= 152:
                    if h <= 67:
                        new_image = pygame.transform.scale(
                            image, (w * 4, h * 4))
                self.surfaces[number_of_file - 1].blit(new_image, (0, 0))
