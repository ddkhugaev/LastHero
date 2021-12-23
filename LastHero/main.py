import pygame.display

from scripts.Constants import *
from scripts.Classes import *
from scripts.Functions import *


pygame.init()

WINDOW = pygame.display.set_mode((SW, SH))
# font
CLOCK = pygame.time.Clock()

PLAYERSPRITE = Player(3, 5, 7)
PLAYER = PlayerHitbox(0, 0, 40, 80, PLAYERSPRITE)
GenerateLevel('data/levels/test01.csv', PLAYER)

run = True
while run:
    CLOCK.tick(FPS)
    if MODE == 0:
        quit = ParseEvents_level()
        if quit is False:
            run = False
        ParseKeys_level(PLAYER)
        CX, CY = MoveCamera_level(PLAYER)
        CameraAffect_level(CX, CY)
        Draw_level(WINDOW)
    elif MODE == 1:
        pass
    pygame.display.flip()

pygame.quit()