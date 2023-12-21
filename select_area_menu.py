import pygame
from buttons import Button

from config import LOAD_AREA, SAVE_AREA
# WIDTH, HEIGHT, FPS, BLACK, WHITE, BLUE, YELLOW, RED, GREEN, TITLE


class SaveAreaButton(Button):
    def __init__(self, image_path, position, text):
        super().__init__(image_path, position, text)
        self.selected_picture = pygame.image.load(
            'images/big selected button.png').convert_alpha()
        self.image = pygame.surface.Surface((100, 50))
        self.image.blit(self.picture, (0, 0))
        self.rect.width = 100
        self.rect.height = 50

    def click_action(self):
        pygame.event.post(
            pygame.event.Event(SAVE_AREA, message=''))


class LoadAreaButton(Button):
    def __init__(self, image_path, position, text):
        super().__init__(image_path, position, text)
        self.selected_picture = pygame.image.load(
            'images/load button.png').convert_alpha()
        self.image = pygame.surface.Surface((100, 50))
        self.image.blit(self.picture, (0, 0))
        self.rect.width = 100
        self.rect.height = 50

    def click_action(self):
        pygame.event.post(
            pygame.event.Event(LOAD_AREA, message=''))


class SelectAreaMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background_image = pygame.image.load(
            'images/select buttons background.png')
        self.save_button = SaveAreaButton('images/save button.png',
                                          (752, 14), 'save')
        self.load_button = LoadAreaButton('images/load button.png',
                                          (902, 14), 'load')
        self.select_buttons_group = pygame.sprite.Group()
        self.select_buttons_group.add(self.save_button)
        self.select_buttons_group.add(self.load_button)

    def draw(self):
        self.screen.blit(self.background_image, (749, 0))
        self.select_buttons_group.draw(self.screen)

    def unselect_button(self):
        self.save_button.unselect_button()

    def handle_events(self, event):
        self.select_buttons_group.update(event)
