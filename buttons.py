import pygame
from config import ELEMENT_SELECTED
# WIDTH, HEIGHT, FPS, BLACK, WHITE, BLUE, YELLOW, RED, GREEN, TITLE


class Button(pygame.sprite.Sprite):
    def __init__(self, image_path, position, text,
                 element_object=None):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.text = text
        self.picture = pygame.image.load(image_path)
        self.selected_picture = pygame.image.load(
            'images/selected button.png').convert_alpha()
        self.image = pygame.Surface((50, 65))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.is_visible = False
        self.image.blit(self.picture, (0, 0))
        sys_font = pygame.font.Font('PixeloidMono-d94EV.ttf', 11)
        text_surface = sys_font.render(self.text, True, (194, 23, 29))
        text_rect = text_surface.get_rect()
        text_rect.x = 0
        text_rect.y = 50
        self.element_object = element_object
        self.image.blit(text_surface, text_rect)

    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(mouse_pos):
                self.image.blit(self.selected_picture, (0, 0))
                self.click_action()
                return True
        return False

    def unselect_button(self):
        self.image.blit(self.picture, (0, 0))

    def select_button(self):
        self.image.blit(self.selected_picture, (0, 0))

    def click_action(self):
        pygame.event.post(
            pygame.event.Event(ELEMENT_SELECTED, message=self.element_object))


class MenuButton(Button):
    def __init__(self, image_path, position, text, menu_object):
        super().__init__(image_path, position, text)
        self.menu_object = menu_object
        self.image = pygame.Surface((50, 50))
        self.esc_picture = pygame.image.load('images/esc_button.png')
        self.elements_picture = pygame.image.load('images/button_0.png')
        self.is_open = False
        self.image.blit(self.elements_picture, (0, 0))

    def click_action(self):
        if self.is_open:
            self.is_open = False
            self.image.blit(self.elements_picture, (0, 0))
            self.menu_object.hide_menu()
        else:
            self.is_open = True
            self.image.blit(self.esc_picture, (0, 0))
            self.menu_object.show_menu()
