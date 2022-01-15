from scripts.Constants import *

player = pygame.transform.rotozoom(pygame.image.load('./data/textures/player_idle.png'), 0, ZK)
player_attack = pygame.transform.rotozoom(pygame.image.load('./data/textures/player_idle_attack.png'), 0, ZK)
player_die = pygame.transform.rotozoom(pygame.image.load('./data/textures/playerstatue.png'), 0, ZK)
finish = pygame.transform.rotozoom(pygame.image.load('./data/textures/level_end.png'), 0, ZK)
slug = pygame.transform.rotozoom(pygame.image.load('./data/textures/slug.png'), 0, ZK)
spider = pygame.transform.rotozoom(pygame.image.load('./data/textures/spider.png'), 0, ZK)

levels = ['Tutorial'] + [f'Level{n + 1}' for n in range(3)]