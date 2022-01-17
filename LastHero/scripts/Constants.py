import pygame
import random


SW, SH = 1000, 600
FPS = 60
ZK = 0.25

MODE = 0
# 0 is for level
# 1 is for main menu
# IDK what else

BDecoGroup = pygame.sprite.Group()
TextGroup = pygame.sprite.Group()
ObstacleGroup = pygame.sprite.Group()
EntityGroup = pygame.sprite.Group()
BulletGroup = pygame.sprite.Group()
FBGroup = pygame.sprite.Group()
HitboxGroup = pygame.sprite.Group()
SpecialGroup = pygame.sprite.Group()

CurrentLevel = [0]

SCORE = [0, 0]
PARTICLES = []