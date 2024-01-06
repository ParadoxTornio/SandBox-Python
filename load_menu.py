import pygame
from config import FPS
from os import listdir
from sys import exit


class LoadMenu:
    def __init__(self, screen):
        self.screen = screen
        self.surface_width = 410
        self.surface_height = 270
        self.button_width = 420
        self.button_height = 282
        self.background_image = pygame.image.load('images/load_menu.png')
        self.red_diskette_image = pygame.image.load('images/diskette_red.png')
        self.selected_button_image = pygame.image.load(
            'images/selected button for load menu.png')
        self.surfaces = []
        self.clock = pygame.time.Clock()
        self.buttons_rects = []
        self.buttons_cords = [
            (13, 90), (435, 90), (857, 90),
            (13, 375), (435, 375), (857, 375)]
        self.esc_rect = pygame.Rect((1205, 25), (50, 50))
        self.is_open = True
        self.choosen_area_number = None
        self.load_images()
        self.run()

    def run(self):
        while self.is_open:
            self.events()
            self.draw()
            self.clock.tick(FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.esc_rect.collidepoint(mouse_pos):
                    self.is_open = False
                for number, rect in self.buttons_rects:
                    if rect.collidepoint(mouse_pos):
                        self.choosen_area_number = number
                        self.is_open = False

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        self.screen.blit(self.background_image, (0, 0))
        for number, surface in enumerate(self.surfaces):
            self.screen.blit(surface, self.buttons_cords[number])
        for number, rect in self.buttons_rects:
            if rect.collidepoint(mouse_pos):
                self.screen.blit(self.selected_button_image,
                                 (self.buttons_cords[number - 1][0] - 5,
                                     self.buttons_cords[number - 1][1] - 6))
                pygame.display.update()
        pygame.display.update()

    def load_images(self):
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
                button_rect = pygame.Rect(
                    self.buttons_cords[number_of_file - 1], (420, 282))
                self.buttons_rects.append((number_of_file, button_rect))
                self.surfaces[number_of_file - 1].fill('Black')
                x = (self.surface_width - new_image.get_width()) // 2
                y = (self.surface_height - new_image.get_height()) // 2
                self.surfaces[number_of_file - 1].blit(new_image, (x, y))
