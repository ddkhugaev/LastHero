from scripts.Constants import *
from scripts.Classes import *


def GenerateLevel(fname:str, playerhb:PlayerHitbox):
    cs = 320 * ZK
    with open(fname, 'r') as f:
        cells = [[el for el in r.split(';')] for r in f.read().split('\n')]
        for i in range(len(cells)):
            for j in range(len(cells[0])):
                if cells[i][j].startswith('#'):
                    Block(j * cs, i * cs, cells[i][j][1:])
                elif cells[i][j].startswith('P'):
                    playerhb.set_coords(j * cs, i * cs)


def ParseEvents_level():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            return False


def ParseKeys_level(playerhb:PlayerHitbox):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        playerhb.sprite.look_right = True
        playerhb.step(playerhb.sprite.speed)
    if keys[pygame.K_LEFT]:
        playerhb.sprite.look_right = False
        playerhb.step(-playerhb.sprite.speed)
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        playerhb.jump(-playerhb.sprite.jumpPower)


def MoveCamera_level(playerhb:PlayerHitbox):
    CX, CY = playerhb.rect.center
    CX -= SW / 2
    CY -= SH / 2
    return CX, CY


def CameraAffect_level(CX, CY):
    HitboxGroup.update(CX, CY)
    ObstacleGroup.update(CX, CY)
    EntityGroup.update(CX, CY)
    BulletGroup.update(CX, CY)
    ItemGroup.update(CX, CY)


def Draw_level(sf):
    sf.fill((30, 50, 100))
    HitboxGroup.draw(sf)
    ObstacleGroup.draw(sf)
    EntityGroup.draw(sf)
    BulletGroup.draw(sf)
    ItemGroup.draw(sf)