import pygame

from scripts.Constants import *
from scripts.Classes import *


def GenerateLevel(fname:str, plist, elist):
    cs = 320 * ZK
    HitboxGroup.empty()
    ObstacleGroup.empty()
    EntityGroup.empty()
    BulletGroup.empty()
    ItemGroup.empty()
    del plist[:]
    del elist[:]
    plist.append(PlayerHitbox(0, 0, 40, 78, Player(3, 5, 8)))
    with open(fname, 'r') as f:
        cells = [[el for el in r.split(';')] for r in f.read().split('\n')]
        for i in range(len(cells)):
            for j in range(len(cells[0])):
                if cells[i][j].startswith('#'):
                    Block(j * cs, i * cs, cells[i][j][1:])
                elif cells[i][j].startswith('$'):
                    FakeBlock(j * cs, i * cs, cells[i][j][1:])
                elif cells[i][j].startswith('P'):
                    plist[0].set_coords(j * cs, i * cs)
                elif cells[i][j].startswith('E'):
                    data = cells[i][j].split('&')[1:]
                    pic, flip = data[2].split()
                    es = Enemy(*map(int, data[1].split()),
                               pygame.transform.flip(eval(pic), bool(flip), False))
                    if int(data[0]) == 0:
                        go, idle = map(int, data[4].split())
                        elist.append(EnemyHitbox(j * cs, i * cs, *map(int, data[3].split()),
                                                 es, int(data[0]),
                                                 [[go, go, True], [idle, idle, False]]))


def ParseEvents_level(plist, elist, cLevel):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            return False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r and e.mod & pygame.KMOD_CTRL:
                GenerateLevel(cLevel, plist, elist)
                return plist[0]


def ParseKeys_level(plist):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        plist[0].left = False
        plist[0].step(plist[0].sprite.speed)
    if keys[pygame.K_LEFT]:
        plist[0].left = True
        plist[0].step(-plist[0].sprite.speed)
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        plist[0].jump(-plist[0].sprite.jumpPower)
    if keys[pygame.K_f]:
        plist[0].attack()
    if keys[pygame.K_p]:
        #print(playerhb.in_air)
        plist[0].damage(1)


def EnemyCycle(elist, plist):
    delete = []
    for i, enemy in enumerate(elist):
        if pygame.sprite.collide_rect(plist[0], enemy):
            if plist[0].is_attack:
                elist[i].damage(1)
            else:
                plist[0].damage(1)
        if not elist[i].is_alive:
            delete.append(i)
    for i in sorted(delete, reverse=True):
        del elist[i]


def ParticleCycle(window, cx, cy):
    delete = []
    for i in range(len(PARTICLES)):
        PARTICLES[i].time(delete, i)
        PARTICLES[i].draw(window, cx, cy)

    for i in reversed(delete):
        del PARTICLES[i]


def MoveCamera_level(plist):
    CX, CY = plist[0].x, plist[0].y
    CX -= SW / 2
    CY -= SH / 2
    return CX, CY


def ObjectUpdate_level(*args):
    HitboxGroup.update(*args)
    ObstacleGroup.update(*args)
    EntityGroup.update(*args)
    BulletGroup.update(*args)
    ItemGroup.update(*args)
    FBGroup.update(*args)


def CameraAffect_level(CX, CY):
    for obj in HitboxGroup:
        obj.rect.center = obj.x - CX, obj.y - CY
    for obj in ObstacleGroup:
        obj.rect.center = obj.x - CX, obj.y - CY
    for obj in EntityGroup:
        obj.rect.center = obj.x - CX, obj.y - CY
    for obj in BulletGroup:
        obj.rect.center = obj.x - CX, obj.y - CY
    for obj in ItemGroup:
        obj.rect.center = obj.x - CX, obj.y - CY
    for obj in FBGroup:
        obj.rect.center = obj.x - CX, obj.y - CY


def Draw_level(mainsf, gui_sf):
    mainsf.fill((60, 100, 200))
    ObstacleGroup.draw(mainsf)
    EntityGroup.draw(mainsf)
    BulletGroup.draw(mainsf)
    ItemGroup.draw(mainsf)
    FBGroup.draw(mainsf)
    HitboxGroup.draw(mainsf)
    mainsf.blit(gui_sf, (0, 0, 1, 1))