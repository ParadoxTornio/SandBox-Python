import pygame
import copy
from config import WIDTH, HEIGHT, FPS, GRAVITY, ELEMENT_SELECTED
# , BLACK, WHITE, BLUE, YELLOW, RED, GREEN, TITLE
from menu import Menu
from eraser import Eraser_menu
from load_and_save import LoadAllButton, SaveAllButton
from pymunk import Space, pygame_util, Segment
from utils import custom_collision


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        pygame_util.positive_y_is_up = False
        self.space = Space()
        self.space.gravity = GRAVITY
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('images/background_2.png')
        self.table_rect = pygame.rect.Rect(0, 82, 1280, 424)
        self.screen.blit(self.background, (0, 0))

        self.clear_picture = pygame.image.load('images/musorka.png')
        self.clear_image = pygame.Surface((50, 50))
        self.clear_rect = self.clear_image.get_rect()
        self.clear_rect.x = 25
        self.clear_rect.y = 25

        self.eraser_picture = pygame.image.load('images/eraser_button.png')
        self.eraser_image = pygame.Surface((50, 50))
        self.eraser_rect = self.eraser_image.get_rect()
        self.eraser_rect.x = 100
        self.eraser_rect.y = 25

        self.selected_button_picture = pygame.image.load(
            'images/selected button.png').convert_alpha()

        self.unselected_button_picture = pygame.image.load(
            'images/unselected button.png').convert_alpha()

        self.small_eraser_surface = pygame.Surface((8, 8), pygame.SRCALPHA)
        self.small_eraser_surface.fill((255, 255, 255, 128))

        self.medium_eraser_surface = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.medium_eraser_surface.fill((255, 255, 255, 128))

        self.large_eraser_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.large_eraser_surface.fill((255, 255, 255, 128))

        self.menu = Menu(self.screen, self.space)

        self.eraser_menu = Eraser_menu(self.screen)

        self.load_all_button = LoadAllButton(
            'images/diskette.png', (1130, 25), '')

        self.save_all_button = SaveAllButton(
            'images/diskette.png', (1055, 25), '')

        self.running = True
        self.selected_element = None
        self.elements_group = pygame.sprite.Group()
        self.save_and_load_buttons_group = pygame.sprite.Group()
        self.options = pygame_util.DrawOptions(self.screen)
        self.draw_options = False

        self.segment_floor = Segment(
            self.space.static_body, (1, HEIGHT - 136), (WIDTH, HEIGHT - 136),
            11)

        self.segment_left_wall = Segment(
            self.space.static_body, (1, 0), (1, HEIGHT), 10)

        self.segment_right_wall = Segment(
            self.space.static_body, (WIDTH - 11, 0), (WIDTH - 11, HEIGHT), 10)

        self.segment_floor.friction = 1

        self.space.add(self.segment_floor)
        self.space.add(self.segment_left_wall)
        self.space.add(self.segment_right_wall)

        self.save_and_load_buttons_group.add(self.save_all_button)
        self.save_and_load_buttons_group.add(self.load_all_button)

    def new(self):
        self.run()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.update()
            self.events()
            self.draw()

    def update(self):
        pygame.display.set_caption(
            f'{self.clock.get_fps()} amount: {len(self.elements_group)}')
        self.space.step(1 / FPS)
        self.elements_group.update()

    def erase_element(self, mouse_pos):
        for sprite in self.elements_group.sprites():
            if sprite.rect.collidepoint(mouse_pos):
                sprite.kill()

    def events(self):
        for sprite_1 in self.elements_group:
            collision = pygame.sprite.spritecollide(
                sprite_1, self.elements_group, False, custom_collision)
            for sprite_2 in collision:
                sprite_1.interaction(sprite_2)
        for event in pygame.event.get():
            mouse_event = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == ELEMENT_SELECTED:
                if event.message is not None:
                    self.selected_element = event.message
                    self.eraser_menu.is_open = False
            elif (mouse_event[0] or mouse_event[2]) and \
                    self.selected_element and \
                    self.table_rect.collidepoint(mouse_pos):
                if mouse_event[0]:
                    if self.selected_element != 'eraser':
                        self.add_element()
                    else:
                        if self.eraser_menu.selected_button == \
                                self.eraser_menu.button_8x8:
                            self.erase_element(mouse_pos)
                        elif self.eraser_menu.selected_button == \
                                self.eraser_menu.button_16x16:
                            for x in range(mouse_pos[0] - 8,
                                           mouse_pos[0] + 9, 8):
                                for y in range(mouse_pos[1] - 8,
                                               mouse_pos[1] + 9, 8):
                                    self.erase_element((x, y))
                        else:
                            for x in range(mouse_pos[0] - 16,
                                           mouse_pos[0] + 17, 8):
                                for y in range(mouse_pos[1] - 16,
                                               mouse_pos[1] + 17, 8):
                                    self.erase_element((x, y))
                elif mouse_event[2]:
                    self.selected_element = None
                    self.menu.unselect_button()
                    self.eraser_menu.is_open = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and \
                        self.clear_rect.collidepoint(mouse_pos):
                    self.elements_group.empty()
                    for i in self.space.bodies:
                        self.space.remove(i)
                    for i in self.space.shapes:
                        self.space.remove(i)
                    self.space.add(self.segment_floor)
                    self.space.add(self.segment_left_wall)
                    self.space.add(self.segment_right_wall)
                if event.button == 1 and \
                        self.eraser_rect.collidepoint(mouse_pos):
                    self.selected_element = 'eraser'
                    self.menu.unselect_button()
                    self.eraser_menu.is_open = True

            self.save_and_load_buttons_group.update(event, self.elements_group)

            self.menu.handle_events(event)
            self.eraser_menu.handle_events(event)

    def draw_options(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_d]:
            self.draw_options = True

        elif key[pygame.K_s]:
            self.draw_options = False

        if self.draw_options:
            self.space.debug_draw(self.options)
            pygame.display.flip()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.elements_group.draw(self.screen)
        mouse_pos = pygame.mouse.get_pos()

        self.menu.draw()
        self.screen.blit(self.clear_picture, (25, 25))
        self.screen.blit(self.eraser_picture, (100, 25))
        self.save_and_load_buttons_group.draw(self.screen)

        if self.selected_element == 'eraser':
            self.eraser_menu.draw()
            if self.eraser_menu.selected_button == self.eraser_menu.button_8x8:
                self.screen.blit(self.small_eraser_surface,
                                 (mouse_pos[0] - 4, mouse_pos[1] - 4))
            elif self.eraser_menu.selected_button ==\
                    self.eraser_menu.button_16x16:
                self.screen.blit(self.medium_eraser_surface,
                                 (mouse_pos[0] - 8, mouse_pos[1] - 8))
            else:
                self.screen.blit(self.large_eraser_surface,
                                 (mouse_pos[0] - 16, mouse_pos[1] - 16))

        pygame.display.flip()

    def add_element(self):
        mouse_pos = pygame.mouse.get_pos()
        x_cord = mouse_pos[0] // 8 * 8
        y_cord = mouse_pos[1] // 8 * 8
        copy_element = copy.copy(self.selected_element)
        copy_element.image = self.selected_element.image.copy()
        copy_element.rect = self.selected_element.rect.copy()
        copy_element.change_position([x_cord, y_cord])
        self.elements_group.add(copy_element)


game = Game()
while game.running:
    game.new()
pygame.quit()
