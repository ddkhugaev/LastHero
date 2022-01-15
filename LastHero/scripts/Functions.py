import pygame
import os
import sys

from scripts.Constants import *
from scripts.Classes import *


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def start_screen(window, clock):
    menu_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image("./data/textures/menu2.png")
    sprite.rect = sprite.image.get_rect()
    menu_sprites.add(sprite)
    menu_sprites.draw(window)

    intro_text = ["Нажмите пробел"]

    font = pygame.font.Font(None, 30)
    text_coord = 500
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 395
        text_coord += intro_rect.height
        window.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def GenerateLevel(fname:str, plist, elist, font):
    cs = 320 * ZK
    HitboxGroup.empty()
    BDecoGroup.empty()
    ObstacleGroup.empty()
    EntityGroup.empty()
    BulletGroup.empty()
    SpecialGroup.empty()
    del plist[:]
    del elist[:]
    plist.append(PlayerHitbox(0, 0, 40, 78, Player(3, 5, 8)))
    with open(fname, 'r', encoding='utf-8') as f:
        cells = [[el for el in r.split(';')] for r in f.read().split('\n')]
        for i in range(len(cells)):
            for j in range(len(cells[0])):
                for el in cells[i][j].split('//'):
                    if el.startswith('#'):
                        Block(j * cs, i * cs, el[1:])
                    elif el.startswith('$'):
                        FakeBlock(j * cs, i * cs, el[1:])
                    elif el.startswith('P'):
                        plist[0].set_coords(j * cs, i * cs)
                    elif el.startswith('E'):
                        data = el.split('&')[1:]
                        pic, flip = data[2].split()
                        es = Enemy(*map(int, data[1].split()),
                                   pygame.transform.flip(eval(pic), bool(flip), False))
                        if int(data[0]) == 0:
                            go, idle = map(int, data[4].split())
                            elist.append(EnemyHitbox(j * cs, i * cs, *map(int, data[3].split()),
                                                     es, int(data[0]),
                                                     [[go, go, True], [idle, idle, False]]))
                    elif el.startswith('T'):
                        Text(j * cs, i * cs, font, el[1:])
                    elif el == 'F':
                        Finish(j * cs, i * cs)


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
    mouse_btn = pygame.mouse.get_pressed()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        plist[0].left = False
        plist[0].step(plist[0].sprite.speed)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        plist[0].left = True
        plist[0].step(-plist[0].sprite.speed)
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        plist[0].jump(-plist[0].sprite.jumpPower)
    if keys[pygame.K_f]  or mouse_btn[0] is True:
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
    BDecoGroup.update(*args)
    ObstacleGroup.update(*args)
    EntityGroup.update(*args)
    BulletGroup.update(*args)
    SpecialGroup.update(*args)
    FBGroup.update(*args)


def SpecialsInteract(plist, elist, font):
    global CurrentLevel
    for obj in SpecialGroup:
        if type(obj) == Finish:
            if pygame.sprite.collide_mask(plist[0], obj):
                CurrentLevel += 1
                GenerateLevel(f'data/levels/{levels[CurrentLevel]}.csv', plist, elist, font)


def CameraAffect_level(CX, CY):
    for obj in HitboxGroup:
        obj.rect.center = obj.x - CX, obj.y - CY
    for obj in ObstacleGroup:
        obj.rect.center = obj.x - CX, obj.y - CY
    for obj in BDecoGroup:
        obj.rect.center = obj.x - CX, obj.y - CY
    for obj in EntityGroup:
        obj.rect.center = obj.x - CX, obj.y - CY
    for obj in BulletGroup:
        obj.rect.center = obj.x - CX, obj.y - CY
    for obj in SpecialGroup:
        obj.rect.center = obj.x - CX, obj.y - CY
    for obj in FBGroup:
        obj.rect.center = obj.x - CX, obj.y - CY


def Draw_level(mainsf, gui_sf, menu_sp):
    menu_sp.draw(mainsf)

    BDecoGroup.draw(mainsf)
    ObstacleGroup.draw(mainsf)
    EntityGroup.draw(mainsf)
    BulletGroup.draw(mainsf)
    SpecialGroup.draw(mainsf)
    FBGroup.draw(mainsf)
    HitboxGroup.draw(mainsf)
    mainsf.blit(gui_sf, (0, 0, 1, 1))