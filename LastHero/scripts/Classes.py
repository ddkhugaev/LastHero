import math

import pygame.sprite

from scripts.Textures import *


def GetSign(n):
    if n == 0:
        return 1
    return int(n / abs(n))


def getXY(cx, cy, degree, distance):
    nx = cx + distance * math.sin(math.radians(degree))
    ny = cy + distance * math.cos(math.radians(degree))
    return (nx, ny)


class BottomHitbox(pygame.sprite.Sprite):
    def __init__(self, w):
        super().__init__(HitboxGroup)
        sf = pygame.Surface((w, 1))
        pygame.draw.rect(sf, 'red', (0, 0, w, 1), 1)
        sf.set_colorkey('black')
        self.image = sf
        self.rect = sf.get_rect(center=(0, 0))
        self.x = 0
        self.y = 0

    def set_coords(self, x, y):
        self.x, self.y = x, y


class HelperHitbox(pygame.sprite.Sprite):
    def __init__(self, w, h):
        super().__init__(HitboxGroup)
        sf = pygame.Surface((w, h))
        pygame.draw.rect(sf, 'green', (0, 0, w, h), 1)
        sf.set_colorkey('black')
        self.image = sf
        self.rect = sf.get_rect(center=(0, 0))
        self.x = 0
        self.y = 0

    def set_coords(self, x, y):
        self.x, self.y = x, y


class EntityHitbox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, sprite):
        super().__init__(HitboxGroup)
        sf = pygame.Surface((w, h))
        pygame.draw.rect(sf, 'white', (0, 0, w, h), 1)
        sf.set_colorkey('black')
        self.h, self.w = h, w
        self.x, self.y = x, y
        self.image = sf
        self.rect = sf.get_rect(center=(x, y))
        self.sprite = sprite
        self.bottomhb = BottomHitbox(w - 2)
        self.tophb = BottomHitbox(w - 2)
        self.v_vert = 0
        self.is_alive = True
        self.G = 0.16

    def set_coords(self, x, y):
        self.x, self.y = x, y

    def damage(self, dmg):
        if not self.is_alive:
            return
        if not self.sprite.hurttimer:
            self.sprite.hp = min(self.sprite.hp - dmg, self.sprite.maxhp)
            self.sprite.hurttimer = 60
            for _ in range(5):
                xs = random.randint(-5, 5)
                ys = random.randint(-5, 0)
                a = random.randint(0, 5) * 0.1
                PARTICLES.append(Particle(self.x, self.y,
                                          'circle', (255, 255, 255), 10,
                                          [[20, {'yspeed': a, 'size': -0.5,
                                                 'blue': -12.75}]], xs=xs, ys=ys))
        if self.sprite.hp <= 0:
            self.is_alive = False
            self.image = pygame.Surface((0, 0))

    def update(self, *args):
        if self.sprite.hurttimer > 0:
            self.sprite.hurttimer -= 1
        if not pygame.sprite.spritecollideany(self.bottomhb, ObstacleGroup):
            self.y += self.v_vert
            #self.rect.y += self.v_vert
            #self.bottomhb.rect.y += self.v_vert
            self.v_vert += self.G
        if pygame.sprite.spritecollideany(self, ObstacleGroup):
            self.y -= 1
            self.v_vert = 0
        if pygame.sprite.spritecollideany(self.tophb, ObstacleGroup) and \
                pygame.sprite.spritecollideany(self, ObstacleGroup):
            self.v_vert = max(self.v_vert, 3)  # -self.v_vert) #()
        self.sprite.set_coords(self.x, self.y)
        self.bottomhb.set_coords(self.x + 1,
                                 self.y + self.h // 2)
        self.tophb.set_coords(self.x + 1,
                              self.y - self.h // 2 - 2)


class PlayerHitbox(EntityHitbox):
    def __init__(self, *args):
        super().__init__(*args)
        self.is_attack = False
        self.left = False
        self.aroundhb = HelperHitbox(240, 240)
        self.weaponhb = HelperHitbox(60, 80)
        self.cdv = 0

    def step(self, amount):
        if not self.is_alive:
            return

        if self.is_attack:
            self.sprite.image = pygame.transform.flip(player_attack, self.left, False)
        else:
            self.sprite.image = pygame.transform.flip(player, self.left, False)

        self.x += amount
        self.rect.x += amount
        if pygame.sprite.spritecollideany(self, ObstacleGroup):
            self.x -= amount
        self.rect.x -= amount

    def jump(self, power):
        if not (pygame.sprite.spritecollideany(self.bottomhb, ObstacleGroup) and self.is_alive):
            return
        self.v_vert = power
        self.y += power

    def descend(self):
        if pygame.sprite.spritecollideany(self.bottomhb, ObstacleGroup) or not self.is_alive:
            return
        self.v_vert = max(self.v_vert, 0)

    def attack(self):
        if not self.is_alive:
            return
        if not self.cdv:
            self.is_attack = True
            self.sprite.image = pygame.transform.flip(player_attack, self.left, False)
            self.cdv = 60

    def damage(self, dmg):
        super().damage(dmg)
        if not self.alive():
            self.sprite.image = player_die

    def update(self, guisf, *args):
        super().update(*args)
        pygame.draw.rect(guisf, 'black', (0, 0, 20 * self.sprite.maxhp, 20))
        pygame.draw.rect(guisf, 'red', (0, 0,
                                        20 * self.sprite.hp * (self.sprite.hp > 0),
                                        20))
        if self.cdv:
            self.cdv -= 1
        if self.cdv == 30:
            self.is_attack = False
            self.sprite.image = pygame.transform.flip(player, self.left, False)

        self.aroundhb.set_coords(self.x, self.y)
        self.weaponhb.set_coords(self.x + 50 * ((not self.left) - (self.left)),
                                 self.y)

        for fb in FBGroup:
            if pygame.sprite.collide_rect(fb, self.aroundhb) and \
                    pygame.sprite.spritecollideany(self, FBGroup):
                fb.image.set_alpha(100)
            else:
                fb.image.set_alpha(255)

        if not self.is_alive:
            self.sprite.image = player_die


class EnemyHitbox(EntityHitbox):
    def __init__(self, x, y, w, h, sprite, type, timership):
        super().__init__(x, y, w, h, sprite)
        self.type = type
        self.timership = timership
        self.i = 0

    def update(self, guisf, *args):
        super().update(*args)
        if not self.is_alive:
            return
        if self.type == 0:
            self.x += self.sprite.speed * self.timership[self.i][2]
            if pygame.sprite.spritecollideany(self, ObstacleGroup) and \
                    not pygame.sprite.spritecollideany(self.bottomhb, ObstacleGroup):
                self.x -= self.sprite.speed

            self.timership[self.i][1] -= 1
            if self.timership[self.i][1] == 0:
                self.timership[self.i][1] = self.timership[self.i][0]
                self.i = (self.i + 1) % len(self.timership)
                if self.timership[self.i][2]:
                    self.sprite.speed = -self.sprite.speed
                    self.sprite.image = pygame.transform.flip(self.sprite.image, True, False)
        pygame.draw.rect(guisf, 'black', (self.rect.centerx - 20, self.rect.centery - 50,
                                          40, 5))
        pygame.draw.rect(guisf, 'red', (self.rect.centerx - 20, self.rect.centery - 50,
                                        40 * self.sprite.hp / self.sprite.maxhp * (self.sprite.hp > 0),
                                        5))


class Player(pygame.sprite.Sprite):
    def __init__(self, hp, speed, jpower):
        super().__init__(EntityGroup)
        self.image = player
        self.rect = player.get_rect(center=(0, 0))
        self.maxhp = hp
        self.hp = hp
        self.speed = speed
        self.jumpPower = jpower
        self.hurttimer = 0
        self.x = 0
        self.y = 0

    def set_coords(self, x, y):
        self.x, self.y = x, y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, hp, speed, pic):
        super().__init__(EntityGroup)
        self.image = pic
        self.rect = pic.get_rect(center=(0, 0))
        self.x = 0
        self.y = 0
        self.maxhp = hp
        self.hp = hp
        self.speed = speed
        self.hurttimer = 0

    def set_coords(self, x, y):
        self.x, self.y = x, y


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__(ObstacleGroup)
        self.image = pygame.transform.rotozoom(
            pygame.image.load(f'./data/textures/block_{type}.png'), 0, ZK)
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y

    def update(self, *args):
        pass


class FakeBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__(FBGroup)
        self.image = pygame.transform.rotozoom(
            pygame.image.load(f'./data/textures/block_{type}.png'), 0, ZK)
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y

    def update(self, *args):
        pass


class Text(pygame.sprite.Sprite):
    def __init__(self, x, y, font:pygame.font.Font, text:str, color:tuple=(255, 255, 255)):
        super().__init__(TextGroup)
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y

    def update(self, *args):
        pass


class Finish(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(SpecialGroup)
        self.image = finish
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y

    def update(self, *args):
        pass


class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y, val):
        super().__init__(SpecialGroup)
        self.image = chest if not (val - 1) else coin
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.val = val
        self.closed = True

    def update(self, *args):
        pass


class BDecoration(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__(BDecoGroup)
        self.image = pygame.transform.rotozoom(
            pygame.image.load(f'./data/textures/{name}.png'), 0, ZK)
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y

    def update(self, *args):
        pass


class Particle:
    def __init__(self, x, y, type:str, c:tuple or list, s,
                 timership, xs=0, ys=0, d:int=0, w=0):
        self.x = x
        self.y = y
        self.type = type
        self.c = list(c)
        self.s = s
        self.timership = timership
        self.xs = xs
        self.ys = ys
        self.w = w
        self.d = d

    def change(self, tvalue:dict):
        for el in tvalue:
            if el == 'red':
                self.c[0] += tvalue[el]
            elif el == 'green':
                self.c[1] += tvalue[el]
            elif el == 'blue':
                self.c[2] += tvalue[el]
            elif el == 'degree':
                self.d += tvalue[el]
            elif el == 'xspeed':
                self.xs += tvalue[el]
            elif el == 'yspeed':
                self.ys += tvalue[el]
            elif el == 'size':
                self.s += tvalue[el]
            elif el == 'width':
                self.w += tvalue[el]

    def draw(self, sf, CX, CY):
        if self.type == 'circle':
            pygame.draw.circle(sf, tuple(self.c),
                               (self.x - CX, self.y - CY),
                               self.s, round(self.w))
        elif self.type == 'square':
            pygame.draw.rect(sf, tuple(self.c),
                             (self.x - CX - self.s,
                              self.y - CY - self.s,
                              self.s * 2, self.s * 2))
        elif self.type == 'line':
            pos = getXY(self.x - CX, self.y - CY, self.d, self.s)
            pygame.draw.line(sf, tuple(self.c),
                             (self.x - CX, self.y - CY),
                             pos, round(self.w))
        elif self.type == 'pic':
            pass

    def time(self, delete:list, n:int):
        self.timership[0][0] -= 1
        self.change(self.timership[0][1])
        self.x += self.xs
        self.y += self.ys
        if self.timership[0][0] <= 0:
            del self.timership[0]
        if not self.timership:
            delete.append(n)


# circle, square, line, pic
#[[60, {r: 1}], [30, {...}], [...]]
