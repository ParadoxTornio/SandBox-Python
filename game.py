import pygame
import copy
import pickle
from config import (
    WIDTH,
    HEIGHT,
    FPS, GRAVITY,
    ELEMENT_SELECTED,
    LOAD_GAME,
    LOAD_AREA,
    SAVE_AREA,
    BLOCK_SIZE
)
from menu import Menu
from eraser import Eraser_menu
from select_area_menu import SelectAreaMenu
from load_and_save import LoadAllButton, SaveAllButton
from pymunk import Space, pygame_util, Segment
from utils import custom_collision
from elements import FireElement, ExplodingElement, WoodElement, \
    GlassElement, LavaElement, LiquidElement, SolidElement, SteamElement
from load_menu import LoadMenu


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

        self.select_area_menu = SelectAreaMenu(self.screen)

        self.load_all_button = LoadAllButton(
            'images/diskette_load.png', (1130, 25), '')

        self.save_all_button = SaveAllButton(
            'images/diskette_save.png', (1055, 25), '')
        self.cursor_image = pygame.image.load('images/cross.png')

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

        self.save_point1 = None
        self.save_point2 = None
        self.is_save_mode = False

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

    def save_area(self, number_of_file):
        min_x = min(self.save_point1[0], self.save_point2[0])
        min_x = min_x // BLOCK_SIZE * BLOCK_SIZE
        min_y = min(self.save_point1[1], self.save_point2[1])
        min_y = min_y // BLOCK_SIZE * BLOCK_SIZE
        max_x = max(self.save_point1[0], self.save_point2[0])
        max_x = (max_x + BLOCK_SIZE - 1) // BLOCK_SIZE * BLOCK_SIZE
        max_y = max(self.save_point1[1], self.save_point2[1])
        max_y = (max_y + BLOCK_SIZE - 1) // BLOCK_SIZE * BLOCK_SIZE
        file_name = ''
        if number_of_file == '0':
            file_name = 'saves/game.save'
        else:
            file_name = f'saves/{number_of_file}_area.save'
        with open(file_name, 'wb') as file:
            data = []
            if number_of_file != '0':
                data.append(((min_x + max_x) // 2,  (min_y + max_y) // 2))

            for sprite in self.elements_group:
                if sprite.rect.x >= min_x and sprite.rect.x <= max_x and \
                        sprite.rect.y >= min_y and sprite.rect.y <= max_y:
                    data.append(((sprite.rect.x, sprite.rect.y), sprite.name))

            pickle.dump(data, file)
        self.save_point1 = None
        self.save_point2 = None
        self.is_save_mode = False
        self.select_area_menu.save_button.unselect_button()
        pygame.mouse.set_visible(True)
        self.draw()
        selected_surface = pygame.Surface((max_x - min_x, max_y - min_y))
        selected_surface.blit(self.screen, (0, 0),
                              (min_x, min_y, max_x, max_y))
        pygame.image.save(selected_surface,
                          f'images/saved_screenshots/{number_of_file}.png')

    def select_area(self):
        pygame.mouse.set_visible(False)
        self.is_save_mode = True

    def load_area(self):
        self.is_save_mode = False
        pygame.mouse.set_visible(True)
        load_menu = LoadMenu(self.screen)
        if load_menu.choosen_area_number:
            print(load_menu.choosen_area_number)

    def load_game(self, data):
        self.clear_screen()
        for coords, name in data:
            new_object = None
            if name == 'вода':
                new_object = LiquidElement('вода', 'images/water_frame.png',
                                           [0, 0], 0, 10, 100, self.space)
            elif name == 'огонь':
                new_object = FireElement(
                    'огонь', 'images/fire_frame.png', [0, 0], 1000)
            elif name == 'металл':
                new_object = SolidElement('металл', 'images/metal_frame.png',
                                          [0, 0], 10, 5, 500, True, self.space)
            elif name == 'C-4':
                new_object = ExplodingElement('C-4', 'images/C4_frame.png',
                                              [0, 0], 15, self.space)
            elif name == 'металл+':
                new_object = SolidElement('металл+',
                                          'images/metal_plus_frame.png',
                                          [0, 0], 50, 5, 1250, True,
                                          self.space)
            elif name == 'лава':
                new_object = LavaElement('лава', 'images/lava_frame.png',
                                         [0, 0], 1200, self.space)
            elif name == 'кислота':
                new_object = LiquidElement('кислота',
                                           'images/poison_frame.png',
                                           [0, 0], 30, 15, 350, self.space)
            elif name == 'кирпичи':
                new_object = SolidElement('кирпичи', 'images/bricks_frame.png',
                                          [0, 0], 10, 10, 1000, False,
                                          self.space)
            elif name == 'бетон':
                new_object = SolidElement('бетон', 'images/concrete_frame.png',
                                          [0, 0], 25, 7, 1000, False,
                                          self.space)
            elif name == 'песок':
                new_object = LiquidElement('песок', 'images/sand_frame.png',
                                           [0, 0], 0, 10, 100000, self.space)
            elif name == 'дуб':
                new_object = WoodElement('дуб', 'images/oak_frame.png',
                                         [0, 0], 5, 900, self.space)
            elif name == 'стекло':
                new_object = GlassElement('стекло', 'images/glass_frame.png',
                                          [0, 0], 5, 550, self.space)
            elif name == 'камень':
                new_object = SolidElement('камень', 'images/stone_frame.png',
                                          [0, 0], 15, 5, 1000, False,
                                          self.space)
            elif name == 'пар':
                new_object = SteamElement(
                    'пар', 'images/пар.png', coords)
            new_object.change_position(coords)
            self.elements_group.add(new_object)

    def clear_screen(self):
        self.elements_group.empty()
        for i in self.space.bodies:
            self.space.remove(i)
        for i in self.space.shapes:
            self.space.remove(i)
        self.space.add(self.segment_floor)
        self.space.add(self.segment_left_wall)
        self.space.add(self.segment_right_wall)

# TODO: сделать проверку перед тем как сохранять что-то по нажатию кнопки

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
                    self.select_area_menu.unselect_button()
                    self.is_save_mode = False
                    pygame.mouse.set_visible(True)

            elif event.type == LOAD_AREA:
                self.load_area()
                self.menu.unselect_button()
            elif event.type == SAVE_AREA:
                self.select_area()
                self.selected_element = None
                self.menu.unselect_button()

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
                    self.select_area_menu.unselect_button()
                    self.is_save_mode = False
                    pygame.mouse.set_visible(True)

            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.is_save_mode and event.button == 1:
                    if self.table_rect.collidepoint(mouse_pos):
                        self.save_point1 = mouse_pos
                    else:
                        self.save_point1 = None
                    self.save_point2 = None
                if event.button == 1 and \
                        self.clear_rect.collidepoint(mouse_pos):
                    self.clear_screen()

                if event.button == 1 and \
                        self.eraser_rect.collidepoint(mouse_pos):
                    self.selected_element = 'eraser'
                    self.menu.unselect_button()
                    self.eraser_menu.is_open = True
                    self.select_area_menu.unselect_button()
                    self.is_save_mode = False
                    pygame.mouse.set_visible(True)

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.is_save_mode and event.button == 1:
                    if self.table_rect.collidepoint(mouse_pos):
                        self.save_point2 = mouse_pos
                    else:
                        self.save_point1 = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and self.is_save_mode:
                    self.save_area('1')
                elif event.key == pygame.K_2 and self.is_save_mode:
                    self.save_area('2')
                elif event.key == pygame.K_3 and self.is_save_mode:
                    self.save_area('3')
                elif event.key == pygame.K_4 and self.is_save_mode:
                    self.save_area('4')
                elif event.key == pygame.K_5 and self.is_save_mode:
                    self.save_area('5')
                elif event.key == pygame.K_6 and self.is_save_mode:
                    self.save_area('6')
                elif event.key == pygame.K_0 and self.is_save_mode:
                    self.save_area('0')

            if event.type == LOAD_GAME:
                self.load_game(event.message)

            self.save_and_load_buttons_group.update(event, self.elements_group)

            self.menu.handle_events(event)
            self.select_area_menu.handle_events(event)
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
        self.select_area_menu.draw()

        if self.is_save_mode:
            self.screen.blit(self.cursor_image,
                             (mouse_pos[0] - 12, mouse_pos[1] - 12))
            if self.save_point1:
                if self.save_point2:
                    min_x = min(self.save_point1[0], self.save_point2[0])
                    min_y = min(self.save_point1[1], self.save_point2[1])
                    max_x = max(self.save_point1[0], self.save_point2[0])
                    max_y = max(self.save_point1[1], self.save_point2[1])
                    selected_surface = pygame.Surface(
                        (max_x - min_x, max_y - min_y), pygame.SRCALPHA)
                    selected_surface.fill((255, 255, 255, 128))
                    self.screen.blit(selected_surface, (min_x, min_y))
                else:
                    min_x = min(self.save_point1[0], mouse_pos[0])
                    min_y = min(self.save_point1[1], mouse_pos[1])
                    max_x = max(self.save_point1[0], mouse_pos[0])
                    max_y = max(self.save_point1[1], mouse_pos[1])
                    selected_surface = pygame.Surface(
                        (max_x - min_x, max_y - min_y), pygame.SRCALPHA)
                    selected_surface.fill((255, 255, 255, 128))
                    self.screen.blit(selected_surface, (min_x, min_y))

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
