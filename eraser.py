import pygame
from buttons import Button
# from config import
# WIDTH, HEIGHT, FPS, BLACK, WHITE, BLUE, YELLOW, RED, GREEN, TITLE


class Eraser_menu:
    def __init__(self, screen):
        self.screen = screen
        self.is_open = False
        self.background_image = pygame.image.load(
            'images/eraser buttons background.png')
        self.button_8x8 = Button('images/button8x8.png', (181, 8),
                                 'small')
        self.button_16x16 = Button('images/button16x16.png', (256, 8),
                                   'medium')
        self.button_32x32 = Button('images/button32x32.png', (331, 8),
                                   'large')
        self.selected_button = self.button_8x8
        self.button_8x8.select_button()
        self.eraser_buttons_group = pygame.sprite.Group()
        self.eraser_buttons_group.add(self.button_8x8)
        self.eraser_buttons_group.add(self.button_16x16)
        self.eraser_buttons_group.add(self.button_32x32)

    def draw(self):
        if self.is_open:
            self.screen.blit(self.background_image, (155, 0))
            self.eraser_buttons_group.draw(self.screen)

    def unselect_button(self):
        if self.selected_button:
            self.selected_button.unselect_button()
            self.selected_button = None

    def handle_events(self, event):
        for button in self.eraser_buttons_group:
            # button.update(event)
            if button.update(event) and self.selected_button != button:
                if self.selected_button:
                    self.selected_button.unselect_button()
                self.selected_button = button
