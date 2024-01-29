import pickle
import pygame
# from game import
from buttons import Button
from config import LOAD_GAME


class SaveAllButton(Button):
    def __init__(self, image_path, position, text, element_object=None):
        super().__init__(image_path, position, text, element_object)
        self.start_time = 0
        self.selected_picture = pygame.image.load('images/diskette_save_2.png')
        self.image = pygame.Surface((50, 50))
        self.image.blit(self.picture, (0, 0))
        self.is_pressed = False

    def click_action(self, list_of_sprites):
        print(0)
        with open('saves/game.save', 'wb') as file:
            data = []

            for sprite in list_of_sprites:
                data.append(((sprite.rect.x, sprite.rect.y), sprite.name))

            pickle.dump(data, file)

    def update(self, event, list_of_sprites):
        if self.is_pressed:
            if pygame.time.get_ticks() - self.start_time >= 2000:
                self.image.blit(self.picture, (0, 0))
                self.is_pressed = False
        else:
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.rect.collidepoint(mouse_pos):
                    self.image.blit(self.selected_picture, (0, 0))
                    self.is_pressed = True
                    self.start_time = pygame.time.get_ticks()
                    self.click_action(list_of_sprites)


class LoadAllButton(SaveAllButton):
    def __init__(self, image_path, position, text, element_object=None):
        super().__init__(image_path, position, text, element_object)
        self.selected_picture = pygame.image.load('images/diskette_load_2.png')

    def click_action(self, list_of_sprites):
        try:
            with open('saves/game.save', 'rb') as file:
                data = pickle.load(file)
                pygame.event.post(
                    pygame.event.Event(LOAD_GAME, message=data))
        except Exception:
            pass
