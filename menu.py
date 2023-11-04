import pygame
from config import WIDTH
# , HEIGHT, FPS, BLACK, WHITE, BLUE, YELLOW, RED, GREEN, TITLE
from elements import SolidElement, LiquidElement, FireElement, \
    ExplodingElement, WoodElement, GlassElement, LavaElement

ELEMENT_SELECTED = pygame.USEREVENT + 1


class Button(pygame.sprite.Sprite):
    def __init__(self, image_path, position, text, element_object=None):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.text = text
        self.picture = pygame.image.load(image_path)
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
                self.click_action()

    def click_action(self):
        pygame.event.post(
            pygame.event.Event(ELEMENT_SELECTED, message=self.element_object))


class MenuButton(Button):
    def __init__(self, image_path, position, text, menu_object):
        super().__init__(image_path, position, text)
        self.menu_object = menu_object
        self.esc_picture = pygame.image.load('esc_button.png')
        self.is_open = False

    def click_action(self):
        if self.is_open:
            self.is_open = False
            self.menu_object.hide_menu()
        else:
            self.is_open = True
            self.image.blit(self.esc_picture, (0, 0))
            self.menu_object.show_menu()


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.elements_button = MenuButton(
            'button_0.png', (WIDTH - 75, 25), '', self)
        self.background_image = pygame.image.load('background.png')
        self.menu_buttons_group = pygame.sprite.Group()
        self.menu_buttons_group.add(self.elements_button)  # noqa
        self.draw()
        self.create_buttons()

    def show_menu(self):
        self.menu_buttons_group.draw(self.screen)

    def hide_menu(self):
        self.menu_buttons_group.clear(self.screen, self.background_image)

    def create_buttons(self):
        water_button = Button(
            'water.png', (100, 525), 'вода',
            LiquidElement('вода', 'water_frame.png', [0, 0], 0, 10, 100))
        fire_button = Button(
            'fire.png', (175, 525), 'огонь',
            FireElement('огонь', 'fire_frame.png', [0, 0], 1000))
        metal_button = Button(
            'metal.png', (250, 525), 'металл',
            SolidElement('металл', 'metal_frame.png',
                         [0, 0], 10, 5, 500, True))
        c4_button = Button(
            'C4.png', (925, 525), 'С-4',
            ExplodingElement('C-4', 'C4_frame.png', [0, 0], 15, False))
        gunpowder_button = Button(
            'gunpowder.png', (1000, 525), 'порох',
            ExplodingElement('порох', 'gunpowder_frame.png', [0, 0], 15, True))
        buf_metal_button = Button(
            'buffed_metal.png', (325, 525), 'металл+',
            SolidElement('металл+', 'metal_plus_frame.png',
                         [0, 0], 50, 5, 1250, True))
        lava_button = Button(
            'lava.png', (700, 525), 'лава',
            LavaElement('лава', 'lava_frame.png', [0, 0], 1200))
        poison_button = Button(
            'poison.png', (775, 525), 'кислота',
            LiquidElement('кислота', 'poison_frame.png', [0, 0], 30, 15, 350))
        bricks_button = Button(
            'bricks.png', (550, 525), 'кирпичи',
            SolidElement('кирпичи', 'bricks_frame.png',
                         [0, 0], 10, 10, 1000, False))
        concrete_button = Button(
            'concrete.png', (400, 525), 'бетон',
            SolidElement('бетон', 'concrete_frame.png',
                         [0, 0], 25, 7, 1000, False))
        sand_button = Button(
            'sand.png', (625, 525), 'песок',
            LiquidElement('песок', 'sand_frame.png', [0, 0], 0, 10, 0))
        oak_button = Button(
            'oak.png', (1075, 525), 'дуб',
            WoodElement('дуб', 'oak_frame.png', [0, 0], 5, 900))
        glass_button = Button(
            'glass.png', (475, 525), 'стекло',
            GlassElement('стекло', 'glass_frame.png', [0, 0], 5, 550))
        stone_button = Button(
            'stone.png', (850, 525), 'камень',
            SolidElement('камень', 'stone_frame.png',
                         [0, 0], 15, 5, 1000, False))
        self.menu_buttons_group.add(water_button)  # noqa
        self.menu_buttons_group.add(fire_button)  # noqa
        self.menu_buttons_group.add(metal_button)  # noqa
        self.menu_buttons_group.add(buf_metal_button)  # noqa
        self.menu_buttons_group.add(concrete_button)  # noqa
        self.menu_buttons_group.add(glass_button)  # noqa
        self.menu_buttons_group.add(bricks_button)  # noqa
        self.menu_buttons_group.add(sand_button)  # noqa
        self.menu_buttons_group.add(lava_button)  # noqa
        self.menu_buttons_group.add(poison_button)  # noqa
        self.menu_buttons_group.add(stone_button)  # noqa
        self.menu_buttons_group.add(c4_button)  # noqa
        self.menu_buttons_group.add(gunpowder_button)  # noqa
        self.menu_buttons_group.add(oak_button)  # noqa

    def draw(self):
        if self.elements_button.is_open:
            self.menu_buttons_group.draw(self.screen)

    def handle_events(self, event):
        for button in self.menu_buttons_group:
            button.update(event)
