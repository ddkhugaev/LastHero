from scripts.Constants import *
from scripts.Textures import *


def GetSign(n):
    if n == 0:
        return 1
    return int(n / abs(n))


class EntityHitbox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, sprite):
        super().__init__(EntityGroup)
        sf = pygame.Surface((w, h))
        pygame.draw.rect(sf, 'white', (0, 0, w, h), 1)
        sf.set_colorkey('black')
        self.image = sf
        self.rect = sf.get_rect(center=(x, y))
        self.sprite = sprite
        self.v_vert = 0
        self.in_air = True
        self.G = 0.16

    def set_coords(self, x, y):
        self.rect.center = (x, y)

    def update(self, CX, CY):
        #if self.in_air:
        self.rect.centery += self.v_vert
        self.v_vert += self.G
        if pygame.sprite.spritecollideany(self, ObstacleGroup):
            self.rect.centery -= 1
            self.in_air = False
            self.v_vert = 0
        self.rect.centerx -= CX
        self.rect.centery -= CY
        self.sprite.set_coords(self.rect.centerx,
                               self.rect.centery)


class PlayerHitbox(EntityHitbox):
    def __init__(self, *args):
        super().__init__(*args)

    def step(self, amount):
        self.sprite.image = pygame.transform.flip(player, amount < 0, False)
        self.rect.centerx += amount
        if pygame.sprite.spritecollideany(self, ObstacleGroup):
            self.rect.centerx -= amount

    def jump(self, power):
        if self.in_air:
            return
        self.in_air = True
        self.v_vert = power


class Player(pygame.sprite.Sprite):
    def __init__(self, hp, speed, jpower):
        super().__init__(EntityGroup)
        self.image = player
        self.rect = player.get_rect(center=(-400, -400))
        self.hp = hp
        self.speed = speed
        self.jumpPower = jpower
    def set_coords(self, x, y):
        self.rect.center = (x, y)

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__(ObstacleGroup)
        self.image = eval(f'block_{type}')
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, CX, CY):
        self.rect.centerx -= CX
        self.rect.centery -= CY