"""Invader Two, electric boogaloo."""

import sys
import random
import time
import pygame


def gen_row(width, height, xcoor, ycoor, array):
    """Generates a row."""
    offset = 0
    pos = 10
    while pos > 0:
        rect = pygame.Rect(xcoor + offset, ycoor, width, height)
        array.append(rect)
        offset += 24
        pos -= 1
    return array


pygame.init()
pygame.font.init()
pygame.mixer.init()
# Screen Stuff
RESOLUTION = (1366, 768)
SCREEN = pygame.display.set_mode(RESOLUTION)
BACKGROUND = pygame.image.load("./Images/SpaceBackground.jpg")
BACKGROUND = pygame.transform.scale(BACKGROUND, RESOLUTION)
FONT = pygame.font.SysFont("ibmplexserif", 20)
STARTPAGE = pygame.image.load("./Images/gamestart.png")
ENDPAGE = pygame.image.load("./Images/gameover.jpg")
STARTPAGE = pygame.transform.scale(STARTPAGE, RESOLUTION)
ENDPAGE = pygame.transform.scale(ENDPAGE, RESOLUTION)
# Player
PLAYERIMG = pygame.image.load("./Images/spaceship.png")
P_WIDTH, P_HEIGHT = 32, 32
PX, PY = (RESOLUTION[0] // 2), (RESOLUTION[1] - 100)
PX_CHA = 0
# This is the coordinates that need to be used for bullets.
PLAYER = pygame.Rect(PX, PY, P_WIDTH, P_HEIGHT)
LIVES = 5
SCORE = 0
# ALIEN
ALIENIMG = pygame.image.load("./Images/ufo.png")
A_WIDTH, A_HEIGHT = 24, 24
ALIENS = []
AY = 0
SHOOTCHANCE = 1000
for i in range(5):
    ALIENS = gen_row(A_HEIGHT, A_WIDTH, A_WIDTH, AY, ALIENS)
    AY += A_WIDTH
# Bullet
BULLETIMG = pygame.image.load("./Images/bullet.png")
B_WIDTH, B_HEIGHT = 16, 16
BY = 100
BULLETS = []
A_BULLETS = []
DX = 1
# SoundFX ¬ Bfxr
EXPLOSION = pygame.mixer.Sound("./Sounds/explosion.wav")
INVADERDEATH = pygame.mixer.Sound("./Sounds/invaderkilled.wav")
SHOT = pygame.mixer.Sound("./Sounds/shoot.wav")
MUSIC = pygame.mixer.music.load(
    "./Sounds/space-invaders-space-invaders-youtubemp3free.org.mp3"
)
pygame.mixer.music.play(-1)

MENU_RUNNING = True
while MENU_RUNNING is True:
    SCREEN.blit(STARTPAGE, (0, 0))
    MENU_RUNNING = False
    pygame.display.update()
    pygame.display.flip()
    time.sleep(3)


GAME_RUNNING = True
while GAME_RUNNING is True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if PX < RESOLUTION[0] - 10:
                    PX_CHA = 2
            elif event.key == pygame.K_LEFT:
                if PX > 10:
                    PX_CHA = -2
            elif event.key == pygame.K_SPACE:
                # If bullets is less than three, create bullet.
                if len(BULLETS) < 3:
                    BULLET = pygame.Rect(
                        (PLAYER.x + P_WIDTH // 4),
                        (PLAYER.y - P_HEIGHT // 2),
                        B_WIDTH,
                        B_HEIGHT,
                    )
                    BULLETS.append(BULLET)
                    SHOT.play()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PX_CHA = 0
    SCREEN.blit(BACKGROUND, (0, 0))
    # Alien Movement
    for i in range(len(ALIENS)):
        invader = ALIENS[i]
        invader.move_ip(DX, 0)
        if invader.x + A_WIDTH >= RESOLUTION[0] or invader.x == 0:
            DX = DX * -1
            for k in range(len(ALIENS)):
                ALIENS[k].move_ip(0, A_HEIGHT)
        elif invader.y >= PLAYER.y:
            GAME_RUNNING = False
        SCREEN.blit(ALIENIMG, ALIENS[i])
    # Player Movement
    SCREEN.blit(PLAYERIMG, PLAYER)
    LIVESSURFACE = FONT.render(f"LIVES:{LIVES}", True, (255, 255, 255))
    SCORESURFACE = FONT.render(f"SCORE:{SCORE}", True, (255, 255, 255))
    SCREEN.blit(SCORESURFACE, (0, RESOLUTION[1] - 100))
    SCREEN.blit(LIVESSURFACE, (RESOLUTION[0] - 100, RESOLUTION[1] - 100))
    PLAYER.move_ip(PX_CHA, 0)
    if PLAYER.x + P_WIDTH >= RESOLUTION[0]:
        PX_CHA = 0
    elif PLAYER.x <= 0:
        PX_CHA = 0
    # Bullet Movement from player.
    for bullet in BULLETS:
        if bullet.y <= 0:
            BULLETS.remove(bullet)
        else:
            bullet.y -= 3
            SCREEN.blit(BULLETIMG, bullet)
    # Bullet Movement for alien.
    SHOOT = random.randint(0, SHOOTCHANCE)
    if SHOOT == 0:
        alien = ALIENS[random.randint(0, len(ALIENS) - 1)]
        A_BULLET = pygame.Rect(
            alien.x + A_WIDTH // 4, alien.y - P_HEIGHT // 2, B_WIDTH, B_HEIGHT
        )
        A_BULLETS.append(A_BULLET)
        SHOT.play()
    for bullet in A_BULLETS:
        if bullet.y >= RESOLUTION[1]:
            A_BULLETS.remove(bullet)
        else:
            bullet.y += 3
            SCREEN.blit(BULLETIMG, bullet)
    # Bullet Collision for alien
    for alien in ALIENS:
        for bulletz in BULLETS:
            if alien.colliderect(bulletz):
                INVADERDEATH.play()
                ALIENS.remove(alien)
                BULLETS.remove(bulletz)
                SCORE += 10
    # Bullet Collision for player
    for bullets in A_BULLETS:
        if PLAYER.colliderect(bullets):
            A_BULLETS.remove(bullets)
            LIVES -= 1
    if LIVES == 0:
        EXPLOSION.play()
        GAME_RUNNING = False
    elif len(ALIENS) == 0:
        AY = 0
        for i in range(5):
            ALIENS = gen_row(A_HEIGHT, A_WIDTH, A_WIDTH, AY, ALIENS)
            AY += A_WIDTH
        DX += 1
        SHOOTCHANCE -= 100
    pygame.display.update()
    pygame.display.flip()
GAME_OVER = True
while GAME_OVER is True:
    SCREEN.blit(ENDPAGE, (0, 0))
    GAME_OVER = False
    with open("./HighScore.txt", "w") as HIGH_S:
        HIGH_S.write(str(SCORE))

    with open("./HighScore.txt", "r") as HIGH_S:
        for line in HIGH_S:
            if SCORE > int(line):
                with open("./HighScore.txt", "w") as HIGH_S:
                    HIGH_S.write(str(SCORE))
            HIGHSCORESURFACE = FONT.render(f"HIGHSCORE:{line}", True, (255, 255, 255))
            SCREEN.blit(HIGHSCORESURFACE, (20, 20))
    pygame.display.update()
    pygame.display.flip()
    time.sleep(3)
sys.exit()
