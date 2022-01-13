import pygame.display

from scripts.Constants import *
from scripts.Classes import *
from scripts.Functions import *


pygame.init()
pygame.display.set_caption('Last Hero')

WINDOW = pygame.display.set_mode((SW, SH))
# font
CLOCK = pygame.time.Clock()


PLAYER = []
ENEMIES = []
GenerateLevel('data/levels/Tutorial.csv', PLAYER, ENEMIES)

run = True
while run:
    CLOCK.tick(FPS)
    if MODE == 0:
        GUI_SF = pygame.Surface((SW, SH))
        GUI_SF.fill('gold')
        GUI_SF.set_colorkey('gold')

        CX, CY = MoveCamera_level(PLAYER)
        ObjectUpdate_level(GUI_SF)
        CameraAffect_level(CX, CY)

        res = ParseEvents_level(PLAYER, ENEMIES, 'data/levels/Tutorial.csv')
        if res is False:
            run = False
        elif res is PlayerHitbox:
            PLAYER = res
        ParseKeys_level(PLAYER)
        EnemyCycle(ENEMIES, PLAYER)
        Draw_level(WINDOW, GUI_SF)
        ParticleCycle(WINDOW, CX, CY)
        #print(PLAYER[0].rect.center, (PLAYER[0].x, PLAYER[0].y), PLAYER[0].x - CX, PLAYER[0].y - CY)
    elif MODE == 1:
        pass
    pygame.display.flip()

pygame.quit()