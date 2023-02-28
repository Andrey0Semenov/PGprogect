import pygame
from pygame import gfxdraw
import os
from random import choice, randrange

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
velocity = 2



class Brick:
    def __init__(self, x, y, w=50, h=20, color=GREEN):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self):
        pygame.draw.rect(screen, self.color, self.rect)


class Bar:
    def __init__(self, x, y, w=60, h=10):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(screen, RED, self.rect)



class Ball:
    def __init__(self, x, y, size=10):
        self.x = x
        self.y = y
        self.color = RED
        self.counter = pygame.time.get_ticks()
        self.size = size

    def update(self):
        global ball, velocity
        global ball_x, ball_y, game
        if pygame.time.get_ticks() - self.counter > velocity:
            self.counter = pygame.time.get_ticks()
            if ball_x == "left":
                ball.x -= velx
                if ball.x < 10:
                    pygame.mixer.Sound.play(s_wall)
                    ball_x = "right"
            if ball_y == 'down':
                ball.y += vel_y
            if ball_y == 'up':
                ball.y -= vel_y
                if ball.y < 50:
                    pygame.mixer.Sound.play(s_wall)
                    ball_y = 'down'
            if ball_x == "right":
                ball.x += velx
                if ball.x > 490:
                    pygame.mixer.Sound.play(s_wall)
                    ball_x = "left"

        gfxdraw.filled_circle(screen, ball.x, ball.y, self.size // 2, self.color)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)


def collision1():
    global ball, bar, ball_y, ball_x, vely, velx, mousedir, bricks
    global diff, lives, stage, score, loop, game, randomstage
    if ball.rect.colliderect(bar):
        pygame.mixer.Sound.play(hitbar)
        ball_y = "up"
        if (mousedir == "left" and ball_x == "right"):
            ball_x = "left"
        if (mousedir == "right" and ball_x == "left"):
            ball_x = "right"
    for n, brick in enumerate(bricks):
        if ball.rect.colliderect(brick):
            pygame.draw.rect(screen, (0, 0, 0), brick.rect)
            screen.blit(update_fps(color="Black"), (12, 10))
            score += 20
            screen.blit(update_fps(), (12, 10))
            pygame.mixer.Sound.play(hitbrick)
            if ball_y == "up":
                if ball.y == (brick.y + brick.h - vel_y):
                    ball_y = "down"
                else:
                    if ball_x == "left":
                        ball_x = "right"
                    else:
                        ball_x = "left"
            elif ball_y == "down":
                if ball.y <= brick.y - 1:
                    ball_y = "up"
                else:
                    if ball_x == "left":
                        ball_x = "right"
                    else:
                        ball_x = "left"
            bricks.pop(n)
            if bricks == []:
                write_highest_score()
                screen.fill((0, 0, 0))
                ball.y = 300
                ball.x = 100
                if randomstage == 1:
                    game = randrange(1, 5)
                if game == 1:
                    bricks = create_bricks1()
                if game == 2:
                    bricks = create_bricks2()
                if game == 3:
                    bricks = create_bricks3()
                if game == 4:
                    bricks = create_bricks4()
                if game == 5:
                    game = randrange(1, 5)
                    if game == 1:
                        create_bricks1()
                    if game == 2:
                        create_bricks2()
                    if game == 3:
                        create_bricks3()
                        ball.size, bar.w = 6, 30
                    if game == 4:
                        ball.size, bar.w = 6, 30
                        create_bricks4()
                show_bricks()

    if ball.y > 510:
        ball.x, ball.y = 500, 300
        lives -= 1
        pygame.mixer.Sound.play(s_out)
        if lives < 0:
            pygame.mixer.Sound.play(s_over)
            set_score()
            score = 0
            stage = 0
            ball_y = 'down'
            ball_x = 'left'
            back_to_menu()


def create_bricks1():
    blist = []
    templ = []
    for n in range(3):
        riga = [str(choice([0, 1])) for x in range(4)]
        riga2 = riga[::-1]
        riga = riga + riga2
        templ.append(riga)
    templ.append(templ[2])
    templ.append(templ[1])
    templ.append(templ[0])
    for riga in templ:
        blist.append("".join(riga))
    bricks = []
    h = 50
    w = 0
    for line in blist:
        for brick in line:
            if brick == "1":
                bricks.append(Brick(20 + w * 60, h))
            w += 1
            if w == 8:
                w = 0
                h += 30
    return bricks


def create_bricks2():
    blist = []
    for n in range(randrange(5, 16)):
        riga = [str(choice([0, 1])) for x in range(4)]
        riga2 = riga[::-1]
        riga = riga + riga2
        blist.append("".join(riga))
    bricks = []
    h = 50
    w = 0
    for line in blist:
        rndclr = randrange(100, 255), randrange(100, 255), randrange(100, 255),
        for brick in line:
            if brick == "1":
                bricks.append(Brick(50 + w * 51, h, color=rndclr))
            w += 1
            if w == 8:
                w = 0
                h += 21
    return bricks
column = 10


def create_bricks3():
    global column
    blist = []
    for n in range(randrange(10, 16)):
        riga = [str(choice([0, 1])) for x in range(column)]
        riga2 = riga[::-1]
        riga = riga + riga2
        blist.append("".join(riga))

    bricks = []
    h = 50
    w = 0
    for line in blist:
        rndclr = randrange(0, 100), randrange(50, 255), randrange(250, 255)
        for brick in line:
            if brick == "1":
                bricks.append(Brick(6 + w * 26, h, w=25, h=10, color=rndclr))
            w += 1
            if w == column * 2:
                w = 0
                h += 11
    return bricks


def create_bricks4():
    global column
    blist = []
    templ = []
    for n in range(randrange(3, 16)):
        riga = [str(choice([0, 1])) for x in range(column)]
        riga2 = riga[::-1]
        riga = riga + riga2
        templ.append(riga)
    templ.append(templ[2])
    templ.append(templ[1])
    templ.append(templ[0])
    for riga in templ:
        blist.append("".join(riga))
    bricks = []
    h = 50
    w = 0
    for line in blist:
        randomcolor = randrange(0, 255), randrange(0, 255), randrange(0, 255),
        for brick in line:
            if brick == "1":
                bricks.append(Brick(6 + w * 51, h, w=30, h=10, color=randomcolor))
            w += 1
            if w == column * 2:
                w = 0
                h += 21
    return bricks

##########################################################################################################################
def write_highest_score():  ######################  Нужно заменить текстовые файлы на базу данных
    global score, scoremax
    with open("score.txt", "w") as file:
        if scoremax < score:
            file.write(str(score))


def update_fps(color="Coral"):
    global score, scoremax
    fps = f"Макс: {scoremax}  |   Жизней: {lives}  |   Счет: {score} "
    fps_text = font.render(fps, 1, pygame.Color(color))
    return fps_text


def write(text, x, y, color="Coral", ):
    text = font.render(text, 1, pygame.Color(color))
    text_rect = text.get_rect(center=(500 // 2, y))
    screen.blit(text, text_rect)
    return text


def score_text():
    global game, randomstage
    if game == 1:
        scorefile = "score1.txt"
    if game == 2:
        scorefile = "score2.txt"
    if game == 3:
        scorefile = "score3.txt"
    if game == 4:
        scorefile = "score4.txt"
    if randomstage == 1:
        scorefile = "score5.txt"
    return scorefile


def get_score():
    global scoremax, game

    scorefile = score_text()
    if scorefile in os.listdir():
        with open(scorefile, "r") as file:
            if file.readlines() == []:
                with open(scorefile, "w") as filewrite:
                    filewrite.write("100")
                    scoremax = 100
            else:
                with open(scorefile, "r") as file:
                    scoremax = int(file.readlines()[0])
    else:
        with open(scorefile, "w") as file:
            file.write("100")
############################################################################################

def set_score():
    global score, randomstage

    scorefile = score_text()
    with open(scorefile, "r") as file:
        scoremax = int(file.readlines()[0])
    if score > scoremax:
        with open(scorefile, "w") as file:
            file.write(str(score))


def restart_common():
    global score, lives, stage
    stage = 0
    score = 0
    lives = 3
    screen.fill((0, 0, 0))
    ball.x, ball.y = 250, 300
    ball.update()
    bar.update()
    ball.size = 10
    bar.w = 60


def restart1():
    global bricks
    restart_common()
    bricks = create_bricks1()
    show_bricks()


def restart2():
    global bricks
    restart_common()
    bricks = create_bricks2()
    show_bricks()


def restart3():
    global bricks
    restart_common()
    ball.size = 6
    bar.w = 30
    bricks = create_bricks3()
    show_bricks()


def restart4():
    global bricks
    restart_common()
    ball.size = 6
    bar.w = 30
    bricks = create_bricks4()
    show_bricks()


def show_bricks():
    for brick in bricks:
        brick.update()
    screen.blit(barrier, (0, 0))
    screen.blit(barrier, (495, 0))


def back_to_menu():
    set_score()
    screen.fill((0, 0, 0))
    mainmenu()


def mainloop():
    global startx, mousedir, diff, game
    show_bricks()
    get_score()
    loop = 1
    while loop:
        pygame.draw.rect(screen, (0, 0, 0), (bar.x, bar.y, bar.w, bar.h))
        gfxdraw.filled_circle(screen, ball.x, ball.y, ball.size // 2, (0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                set_score()
                loop = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    set_score()
                    loop = 0
                if event.key == pygame.K_m:
                    back_to_menu()
            if event.type == pygame.KEYUP:
                if event.type == pygame.K_ESCAPE:
                    loop = 0
        posx = pygame.mouse.get_pos()[0]
        if pygame.mouse.get_pos()[1] > 400:
            bar.y = pygame.mouse.get_pos()[1]
        if posx > 10 and posx < 430 + 60 - bar.w:
            bar.x = posx
        diff = startx - posx
        mousedir = check_mouse_dir(diff)
        startx = posx
        ball.update()

        bar.update()
        collision1()
        pygame.display.update()
        clock.tick(240)
    pygame.quit()


def check_mouse_dir(diff):
    if diff < 0:
        mousedir = "right"
    elif diff > 0:
        mousedir = "left"
    else:
        mousedir = ""
    return mousedir


randomstage = 0


def mainmenu():
    global game, randomstage
    screen.fill((0, 0, 0))
    write("АРКАНОИД", 200, 120, color="yellow")
    write("Выберите уровень", 200, 180, color="green")
    write("1 - I уровень", 150, 210)
    write("2 - II уровень", 150, 230)
    write("3 - III уровень", 150, 250)
    write("4 - IV уровень", 150, 270)
    write("5 - V уровень", 150, 290)
    write("Выберите уровень,", 10, 450, color="gray")
    write("нажав цифру на клавиатуре", 10, 480, color="gray")
    loop = 1
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop = 0
                elif event.key == pygame.K_1:
                    game = 1
                    restart1()
                elif event.key == pygame.K_2:
                    game = 2
                    restart2()
                elif event.key == pygame.K_3:
                    game = 3
                    restart3()
                elif event.key == pygame.K_4:
                    game = 4
                    restart4()
                elif event.key == pygame.K_5:
                    randomstage = 1
                    game = randrange(1, 5)
                    if game == 1:
                        restart1()
                    if game == 2:
                        restart2()
                    if game == 3:
                        restart3()
                    if game == 4:
                        restart4()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4 or event.key == pygame.K_5:
                    screen.fill((0, 0, 0))
                    mainloop()
        pygame.display.update()
    pygame.quit()


stage = 0
lives = 3
ball_x = 'left'
ball_y = 'down'
velx = 1
vel_y = 1
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 512)
pygame.mixer.set_num_channels(32)
hitbar = pygame.mixer.Sound('sound\\kosanie.wav')
s_out = pygame.mixer.Sound('sound\\outspeech.wav')
hitbrick = pygame.mixer.Sound('sound\\hitbrick.wav')
s_over = pygame.mixer.Sound('sound\\kosanie.wav')  ################ Добавить звук проигрыша
s_wall = pygame.mixer.Sound('sound\\wall.wav')
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("ArkaGame 5.0 by pythonprogramming.altervista.org")
clock = pygame.time.Clock()
startx = 0
barrier = pygame.image.load("img\\barrier.png").convert()
pygame.mouse.set_visible(False)
mousedir = "stop"
diff = 0
score = 0
font = pygame.font.SysFont("Arial", 14)
scoremax = 0
font = pygame.font.SysFont("Arial", 24)
bar = Bar(10, 480)
ball = Ball(100, 300)
pygame.event.set_grab(True)
mainmenu()
