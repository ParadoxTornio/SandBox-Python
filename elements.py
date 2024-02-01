from config import BLOCK_SIZE, BURN_ELEMENT
# WIDTH, HEIGHT, FPS, BLACK, WHITE, BLUE, YELLOW, RED, GREEN, TITLE
import pygame
from pymunk import Body, Circle, Segment, Poly
# import random
import time


class Element(pygame.sprite.Sprite):
    def __init__(self, name, image_path, pos):
        pygame.sprite.Sprite.__init__(self)
        # self.image = image
        self.image_path = image_path
        self.picture = pygame.image.load(self.image_path)
        self.image = pygame.Surface((8, 8))
        self.image.blit(self.picture, (0, 0))
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.name = name

    def draw_element(self):
        pass

    def change_position(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def __copy__(self):
        new_instance = self.__class__(self.name, self.image_path, self.pos)
        return new_instance


class SteamElement(Element):
    def __init__(self, name, image_path, pos):
        super().__init__(name, image_path, pos)
        self.time_on_screen = None

    def change_position(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        self.rect.y -= 2
        if not self.time_on_screen:
            self.time_on_screen = time.perf_counter()
        elif time.perf_counter() - self.time_on_screen >= 2.5:
            pygame.sprite.Sprite.kill(self)

    def interaction(self, sprite_2):
        pass


class SolidElement(Element):
    def __init__(self, name, image_path, pos, solidity,
                 fragility, temperature_resistance, is_melting, space):
        super().__init__(name, image_path, pos)
        self.space = space
        self.solidity = solidity
        self.fragility = fragility
        self.temperature_resistance = temperature_resistance
        self.is_melting = is_melting
        self.is_killed = False

    def change_position(self, pos):
        pos = (pos[0] // 8 * 8, pos[1] // 8 * 8)
        super().change_position(pos)

        self.metal_block = Segment(
            self.space.static_body,
            (pos[0] + BLOCK_SIZE // 2, pos[1] + BLOCK_SIZE // 2 - 1),
            (pos[0] + BLOCK_SIZE // 2, pos[1] + BLOCK_SIZE // 2 + 1),
            BLOCK_SIZE // 2 - 1)
        self.space.add(self.metal_block)

    def __copy__(self):
        new_instance = self.__class__(
            self.name, self.image_path, self.pos,
            self.solidity, self.fragility,
            self.temperature_resistance, self.is_melting, self.space)
        return new_instance

    def kill(self):
        if not self.is_killed:
            self.space.remove(self.metal_block)
            super().kill()
            self.is_killed = True

    def interaction(self, sprite_2):
        if self.groups() == sprite_2.groups() and \
                self.name == sprite_2.name:
            sprite_2.kill()
        if not isinstance(sprite_2, SolidElement):
            if isinstance(sprite_2, LiquidElement):
                if self.solidity < sprite_2.ph:
                    try:
                        self.groups()[0].add(SteamElement('пар', 'images/пар.png', [self.rect.x, self.rect.y]))  # noqa
                    except IndexError or AssertionError:
                        pass
                    self.kill()
            elif isinstance(sprite_2, FireElement):
                if self.is_melting:
                    if self.temperature_resistance <= sprite_2.temperature:
                        self.kill()


class FireElement(Element):
    def __init__(self, name, image_path, pos, temperature):
        super().__init__(name, image_path, pos)
        self.temperature = temperature
        self.time_on_screen = None

    def __copy__(self):
        new_instance = self.__class__(
            self.name, self.image_path, self.pos, self.temperature)
        return new_instance

    def update(self):
        if not self.time_on_screen:
            self.time_on_screen = time.perf_counter()
        elif time.perf_counter() - self.time_on_screen >= 1:
            pygame.sprite.Sprite.kill(self)

    def interaction(self, sprite_2):
        if self.groups() == sprite_2.groups() and \
                self.name == sprite_2.name:
            sprite_2.kill()
        if isinstance(sprite_2, LiquidElement):
            if self.temperature >= sprite_2.evaporation_temperature:
                try:
                    sprite_2.groups()[0].add(SteamElement('пар', 'images/пар.png', [self.rect.x, self.rect.y]))  # noqa
                except IndexError:
                    pass
                sprite_2.kill()
                self.kill()


class LiquidElement(Element):
    def __init__(self, name, image_path, pos, ph,
                 liquidity, evaporation_temperature, space):
        super().__init__(name, image_path, pos)
        self.image = pygame.Surface((16, 16))
        self.image.blit(self.picture, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        self.ph = ph
        self.liquidity = liquidity
        self.evaporation_temperature = evaporation_temperature
        self.space = space
        water_body = Body(10, 100)
        water_body.position = pos
        self.water_shape = Circle(water_body, 5, (0, 0))
        self.water_shape.friction = 0
        space.add(water_body, self.water_shape)

    def update(self):
        self.rect.x = self.water_shape.body.position[0] - 8
        self.rect.y = self.water_shape.body.position[1] - 8

    def change_position(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.water_shape.body.position = pos[0] + 8, pos[1] + 8

    def __copy__(self):
        new_instance = self.__class__(self.name, self.image_path, self.pos,
                                      self.ph, self.liquidity,
                                      self.evaporation_temperature, self.space)
        return new_instance

    def kill(self):
        self.space.remove(self.water_shape)
        super().kill()

    def interaction(self, sprite_2):
        pass


class SandElement(Element):
    def __init__(self, name, image_path, pos, space):
        super().__init__(name, image_path, pos)
        self.image = pygame.Surface((16, 16))
        self.image.blit(self.picture, (0, 0))
        self.rect = self.image.get_rect()
        self.space = space
        self.body = Body(200, 1000)
        self.shape = Poly.create_box(self.body, (12, 12))
        self.shape.friction = 0.9
        self.shape.elasticity = 0.05
        self.space.add(self.body, self.shape)
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def update(self):
        self.rect.x = self.shape.body.position[0] - 8
        self.rect.y = self.shape.body.position[1] - 8

    def change_position(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.shape.body.position = pos[0] + 8, pos[1] + 8

    def __copy__(self):
        new_instance = self.__class__(
            self.name, self.image_path, self.pos, self.space)
        return new_instance

    def kill(self):
        self.space.remove(self.shape)
        super().kill()

    def interaction(self, sprite_2):
        pass


class ExplodingElement(Element):
    def __init__(self, name, image_path, pos, explosion_power, space):
        super().__init__(name, image_path, pos)
        self.explosion_power = explosion_power
        self.space = space
        self.is_killed = False
        self.is_blown_up = False
        self.time_after_exp = None
        self.explosion_images = []
        self.anim_number = None
        for i in range(1, 10):
            self.explosion_images.append(
                pygame.image.load(f'images/Explosion/Explosion{i}.png'))

    def __copy__(self):
        new_instance = self.__class__(
            self.name, self.image_path, self.pos,
            self.explosion_power, self.space)
        return new_instance

    def update(self):
        if self.time_after_exp:
            if time.perf_counter() - self.time_after_exp >= 0.5:
                self.kill()
                self.time_after_exp = None
            elif time.perf_counter() - \
                    self.time_after_exp >= 0.06 * (self.anim_number + 1):
                self.anim_number += 1
                self.image = pygame.Surface(
                    (self.rect.width, self.rect.height), pygame.SRCALPHA)
                self.image.blit(
                    self.explosion_images[self.anim_number], (0, 0))

    def explode(self):
        center = self.rect.center
        self.rect.width = 192
        self.rect.height = 192
        self.rect.center = center
        self.image = pygame.Surface((self.rect.width, self.rect.height),
                                    pygame.SRCALPHA)
        self.image.blit(self.explosion_images[0], (0, 0))
        self.time_after_exp = time.perf_counter()
        self.anim_number = 0
        # self.image.fill((255, 255, 255, 128))

    def kill(self):
        if not self.is_killed:
            self.space.remove(self.exploding_block)
            super().kill()
            self.is_killed = True

    def change_position(self, pos):
        pos = (pos[0] // 8 * 8, pos[1] // 8 * 8)
        super().change_position(pos)

        self.exploding_block = Segment(
            self.space.static_body,
            (pos[0] + BLOCK_SIZE // 2, pos[1] + BLOCK_SIZE // 2 - 1),
            (pos[0] + BLOCK_SIZE // 2, pos[1] + BLOCK_SIZE // 2 + 1),
            BLOCK_SIZE // 2 - 1)
        self.space.add(self.exploding_block)

    def interaction(self, sprite_2):
        if self.groups() == sprite_2.groups() and \
                self.name == sprite_2.name:
            if not self.is_blown_up and not sprite_2.is_blown_up:
                sprite_2.kill()
        if isinstance(sprite_2, FireElement):
            if not self.is_blown_up:
                self.explode()
                self.is_blown_up = True
        if isinstance(sprite_2, ExplodingElement):
            if self.is_blown_up:
                if not sprite_2.is_blown_up:
                    sprite_2.explode()
                    sprite_2.is_blown_up = True
        if isinstance(sprite_2, SandElement):
            if self.is_blown_up:
                sprite_2.kill()
        if isinstance(sprite_2, SolidElement):
            if self.explosion_power >= sprite_2.solidity:
                sprite_2.kill()
        if isinstance(sprite_2, WoodElement):
            if self.explosion_power > sprite_2.solidity:
                sprite_2.kill()
        if isinstance(sprite_2, GlassElement):
            if self.explosion_power >= sprite_2.solidity:
                sprite_2.kill()
        if isinstance(sprite_2, LiquidElement):
            if sprite_2.ph > 0:
                try:
                    self.groups()[0].add(SteamElement('пар', 'images/пар.png', [self.rect.x, self.rect.y]))  # noqa
                except IndexError or AssertionError:
                    pass


class WoodElement(Element):
    def __init__(self, name, image_path, pos,
                 solidity, temperature_resistance, space):
        super().__init__(name, image_path, pos)
        self.solidity = solidity
        self.space = space
        self.temperature_resistance = temperature_resistance
        self.time_on_screen = None
        self.is_killed = False
        self.is_burning = False

    def change_position(self, pos):
        super().change_position(pos)
        self.pos = pos
        self.wood_block = Segment(
            self.space.static_body,
            (pos[0] + BLOCK_SIZE // 2, pos[1] + BLOCK_SIZE // 2 - 1),
            (pos[0] + BLOCK_SIZE // 2, pos[1] + BLOCK_SIZE // 2 + 1),
            BLOCK_SIZE // 2 - 1)
        self.space.add(self.wood_block)

    def kill(self):
        if not self.is_killed:
            self.space.remove(self.wood_block)
            super().kill()
            self.is_killed = True

    def __copy__(self):
        new_instance = self.__class__(self.name, self.image_path,
                                      self.pos, self.solidity,
                                      self.temperature_resistance, self.space)
        return new_instance

    def update(self):
        if self.is_burning:
            if not self.time_on_screen:
                self.time_on_screen = time.perf_counter()
            elif time.perf_counter() - self.time_on_screen >= 0.9:
                self.burn_around()
                self.kill()

    def burn_around(self):
        pygame.event.post(
            pygame.event.Event(
                BURN_ELEMENT, message=(self.pos[0], self.pos[1] - 8)))
        pygame.event.post(
            pygame.event.Event(
                BURN_ELEMENT, message=(self.pos[0], self.pos[1] + 8)))
        pygame.event.post(
            pygame.event.Event(
                BURN_ELEMENT, message=(self.pos[0] - 8, self.pos[1])))
        pygame.event.post(
            pygame.event.Event(
                BURN_ELEMENT, message=(self.pos[0] + 8, self.pos[1])))

    def interaction(self, sprite_2):
        if self.groups() == sprite_2.groups() and \
                self.name == sprite_2.name:
            sprite_2.kill()
        if isinstance(sprite_2, FireElement):
            if self.temperature_resistance < sprite_2.temperature:
                if not self.is_burning:
                    self.is_burning = True
        elif isinstance(sprite_2, LiquidElement):
            if self.solidity < sprite_2.ph:
                self.kill()


class GlassElement(Element):
    def __init__(self, name, image_path, pos,
                 solidity, temperature_resistance, space):
        super().__init__(name, image_path, pos)
        self.solidity = solidity
        self.space = space
        self.temperature_resistance = temperature_resistance

    def change_position(self, pos):
        super().change_position(pos)
        self.glass_block = Segment(
            self.space.static_body,
            (pos[0] + BLOCK_SIZE // 2, pos[1] + BLOCK_SIZE // 2 - 1),
            (pos[0] + BLOCK_SIZE // 2, pos[1] + BLOCK_SIZE // 2 + 1),
            BLOCK_SIZE // 2 - 1)
        self.space.add(self.glass_block)

    def kill(self):
        self.space.remove(self.glass_block)
        super().kill()

    def __copy__(self):
        new_instance = self.__class__(self.name, self.image_path,
                                      self.pos, self.solidity,
                                      self.temperature_resistance, self.space)
        return new_instance

    def interaction(self, sprite_2):
        if self.groups() == sprite_2.groups() and \
                self.name == sprite_2.name:
            sprite_2.kill()
        if isinstance(sprite_2, FireElement):
            if sprite_2.temperature >= self.temperature_resistance:
                self.kill()
        if isinstance(sprite_2, LiquidElement):
            if sprite_2.ph >= self.solidity * 10:
                self.kill()


class LavaElement(Element):
    def __init__(self, name, image_path, pos, temperature, space):
        super().__init__(name, image_path, pos)
        self.temperature = temperature
        self.space = space
        self.is_killed = False
        self.image = pygame.Surface((16, 16))
        self.image.blit(self.picture, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        lava_body = Body(10, 100)
        lava_body.position = pos
        self.lava_shape = Circle(lava_body, 5, (0, 0))
        self.lava_shape.friction = 0
        space.add(lava_body, self.lava_shape)

    def update(self):
        self.rect.x = self.lava_shape.body.position[0] - 8
        self.rect.y = self.lava_shape.body.position[1] - 8

    def __copy__(self):
        new_instance = self.__class__(
            self.name, self.image_path, self.pos, self.temperature, self.space)
        return new_instance

    def change_position(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.lava_shape.body.position = pos[0] + 8, pos[1] + 8

    def kill(self):
        if not self.is_killed:
            self.space.remove(self.lava_shape)
            super().kill()
            self.is_killed = True

    def interaction(self, sprite_2):
        if isinstance(sprite_2, LiquidElement):
            try:
                if self.rect.y > sprite_2.rect.y:
                    cords = [self.rect.x, self.rect.y]
                else:
                    cords = [sprite_2.rect.x, sprite_2.rect.y]
                self.steam_element = SteamElement(
                    'пар', 'images/пар.png', cords)
                self.solid_element1 = SolidElement('камень',
                                                   'images/stone_frame.png',
                                                   [0, 0], 15, 5, 1000, False,
                                                   self.space)
                self.solid_element2 = SolidElement('камень',
                                                   'images/stone_frame.png',
                                                   [0, 0], 15, 5, 1000, False,
                                                   self.space)
                self.solid_element3 = SolidElement('камень',
                                                   'images/stone_frame.png',
                                                   [0, 0], 15, 5, 1000, False,
                                                   self.space)
                self.solid_element4 = SolidElement('камень',
                                                   'images/stone_frame.png',
                                                   [0, 0], 15, 5, 1000, False,
                                                   self.space)
                cords[0] = cords[0] // BLOCK_SIZE * BLOCK_SIZE
                cords[1] = cords[1] // BLOCK_SIZE * BLOCK_SIZE
                self.solid_element1.change_position(cords)
                self.solid_element2.change_position(
                    (cords[0] + 8, cords[1]))
                self.solid_element3.change_position(
                    (cords[0], cords[1] + 8))
                self.solid_element4.change_position(
                    (cords[0] + 8, cords[1] + 8))
                self.groups()[0].add(self.steam_element)
                self.groups()[0].add(self.solid_element1)
                self.groups()[0].add(self.solid_element2)
                self.groups()[0].add(self.solid_element3)
                self.groups()[0].add(self.solid_element4)

            except IndexError:
                pass
            sprite_2.kill()
            self.kill()
        if isinstance(sprite_2, SolidElement):
            if self.temperature >= sprite_2.temperature_resistance:
                sprite_2.kill()
        if isinstance(sprite_2, WoodElement):
            if self.temperature >= sprite_2.temperature_resistance:
                sprite_2.kill()
        if isinstance(sprite_2, GlassElement):
            if self.temperature >= sprite_2.temperature_resistance:
                sprite_2.kill()
