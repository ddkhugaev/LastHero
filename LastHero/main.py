from scripts.Constants import *
from scripts.Classes import *
from scripts.Functions import *


pygame.init()
pygame.display.set_caption('Last Hero')

WINDOW = pygame.display.set_mode((SW, SH))
FONT = pygame.font.Font(None, 20)
CLOCK = pygame.time.Clock()


start_screen(WINDOW, CLOCK)
PLAYER = []
ENEMIES = []
GenerateLevel(f'data/levels/{levels[CurrentLevel]}.csv', PLAYER, ENEMIES, FONT)

menu_sprites = pygame.sprite.Group()
sprite_menu = pygame.sprite.Sprite()
sprite_menu.image = load_image("./data/textures/background2.png")
sprite_menu.rect = sprite_menu.image.get_rect()
menu_sprites.add(sprite_menu)

run = True
while run:
    CLOCK.tick(FPS)
    if MODE == 0:
        GUI_SF = pygame.Surface((SW, SH))
        GUI_SF.fill('gold')
        GUI_SF.set_colorkey('gold')

        ObjectUpdate_level(GUI_SF)
        SpecialsInteract(PLAYER, ENEMIES, FONT)
        CX, CY = MoveCamera_level(PLAYER)
        CameraAffect_level(CX, CY)

        res = ParseEvents_level(PLAYER, ENEMIES, 'data/levels/Tutorial.csv')
        if res is False:
            run = False
        elif res is PlayerHitbox:
            PLAYER = res
        ParseKeys_level(PLAYER)
        EnemyCycle(ENEMIES, PLAYER)
        Draw_level(WINDOW, GUI_SF, menu_sprites)
        ParticleCycle(WINDOW, CX, CY)
        #print(PLAYER[0].rect.center, (PLAYER[0].x, PLAYER[0].y), PLAYER[0].x - CX, PLAYER[0].y - CY)
    elif MODE == 1:
        pass
    pygame.display.flip()

pygame.quit()