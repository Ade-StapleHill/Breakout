import pygame, math, random
from pygame.locals import *

screen = pygame.display.set_mode((400, 600))

dbg_flag = True     ## set True for DBG print
def dbg_print(str):
    global dbg_flag

    if dbg_flag:
        print(f"DBG: {str}")



#https://gamedev.stackexchange.com/questions/61705/pygame-colliderect-but-how-do-they-collide

def on_collide(paddle, ball, nregions=3):
    # we collided, so which side? Args are the `Rect`s of paddle and ball.
    # Divide width of paddle into nregions, default 3, and return index 
    #
    print("paddle.centery=%d, ball.centery=%d " % (paddle.centery, ball.centery))
    if paddle.centery < ball.centery:
        dbg_print("paddle bottom")
    elif paddle.centery > ball.centery:
        dbg_print("paddle top")

    if paddle.centerx < ball.centerx:
        dbg_print("paddle right")
    elif paddle.centerx > ball.centerx:
        dbg_print("paddle left")

    ball_offset = ball.centerx - paddle.x
    region_width = int(paddle.width / nregions)
    region = int(ball_offset / region_width)
    if region < 0: region = 0 ## left edge clipped the ball
    if region >= nregions : region = nregions - 1  ## right edge clipped ball
    dbg_print(f"region={region}, ball_offset={ball_offset}, nregions={nregions}, paddle.width={paddle.width}")

    return region

# Making the bat


class Bat:
    def __init__(self):
        self.x = screen.get_width() / 2
        self.y = screen.get_height() - 20
        self.drawn = None

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.x > 40:
            self.x -= 7
        if pressed_keys[K_RIGHT] and self.x < 360:
            self.x += 7

    def draw(self):
        self.drawn = pygame.draw.line(screen, (0, 0, 0), (self.x - 30, self.y),
                         (self.x + 30, self.y), 6)


# Defining the ball


class Ball:
    def __init__(self):
        self.direction = math.pi + math.pi / 3 * random.random()
        self.speed = 4
        self.move_vector()
        self.x = screen.get_width() / 2
        self.y = screen.get_height() - 60
        self.r = 10
        self.colour = (0, 0, 0)
        self.drawn = None
        self.hit = False

    def move_vector(self):
        self.dx = math.sin(self.direction) * self.speed
        self.dy = math.cos(self.direction) * self.speed

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        self.drawn = pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)),
                           self.r, 0)

    def bounce(self, blocks, score):

        # Bouncing off the sides

        if (self.x <= 20 and self.dx < 0) or (self.x >= screen.get_width() - 20
                                              and self.dx > 0):
            self.dx *= -1
        if self.y <= 10:
            self.dy *= -1

        # Bounce off the bat
        spin_arr = (-10, -5, 0, 0, 0, 5, 10)
        if bat.drawn.colliderect(self.drawn) and not self.hit:
            self.hit = True   ## avoid multiple collision as ball travels accross

            if (bat.drawn.centery > self.drawn.centery):
                # collide top of bat
                region = on_collide(bat.drawn, self.drawn, len(spin_arr))
                self.dy *= -1   ## change vertical direction

                spin_angle = spin_arr[region]
                if spin_angle:
                    self.direction = math.atan2(self.dy, self.dx) + math.radians(spin_angle)
                    self.move_vector()

                dbg_print(f"{spin_angle= }, {self.direction= }") 
        else:
            self.hit = False    ## reset to detect new collision

        # Bounce off the blocks

        for block in blocks:
            if pygame.Rect(block.x, block.y, 50, 20).colliderect(
                    self.x - 10, self.y - 10, 20, 20):
                self.dy *= -1
                blocks.remove(block)
                score += 10
                if score % 50 == 0:
                    self.dy *= 1.25
                    self.dx *= 1.25
        return blocks, score

        for block in blocks:
            if Block.colour == (255, 0, 0):
                if pygame.Rect(block.x, block.y, 50, 20).colliderect(
                        self.x - 10, self.y - 10, 20, 20):
                    score += 40


# Defining the blocks


class Block:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour

    def draw(self):
        pygame.draw.rect(screen, self.colour, Rect(self.x, self.y, 50, 20), 0)


# Defining what to do when the game finishes


def gameOver():
    pygame.draw.rect(
        screen, (255, 255, 255),
        Rect(10, 10,
             screen.get_width() - 20,
             screen.get_height() - 20), 0)

    txt = font.render("Score", True, (0, 0, 0))
    screen.blit(txt, (int(screen.get_width() / 2 - txt.get_width() / 2), 50))
    txt = font.render(str(score), True, (0, 0, 0))
    screen.blit(txt, (int(screen.get_width() / 2 - txt.get_width() / 2), 70))
    txt = font.render("Press 'r' to retry", True, (0, 0, 0))
    screen.blit(txt, (int(screen.get_width() / 2 - txt.get_width() / 2), 90))

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_r:
                    return
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit


# Initialize pygame

pygame.init()

# Setting up the screen and characters

pygame.display.set_caption("Breakout")
clock = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 30)
bat = Bat()
blocks = []

# Block colours

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
TEAL = (0, 255, 255)
colours = [RED, BLUE, GREEN, PURPLE, YELLOW, TEAL]
i = 0

# Building blocks

for y in range(50, 350, 50):
    for x in range(25, 360, 60):
        blocks.append(Block(x, y, colours[i]))
    i += 1

# Setting up score and text

txt = font.render("Press space to start", True, (255, 255, 255))
screen.blit(txt, (int(screen.get_width() * 0.25), int(screen.get_height() * 0.2)))
pygame.display.update()
wait = True

while wait:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                wait = False

# Other character setup and screen fill

ball = Ball()
screen.fill((0, 0, 0))

# Game Loop

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            raise SystemExit

    # Border

    pygame.draw.rect(
        screen, (255, 255, 255),
        Rect(10, 10,
             screen.get_width() - 20,
             screen.get_height() - 20), 0)

    # Draw the blocks

    for block in blocks:
        block.draw()

    # Move the bat and ball

    bat.move()
    bat.draw()
    ball.move()
    ball.draw()

    # Bounce the ball if required

    blocks, score = ball.bounce(blocks, score)

    if len(blocks) == 0 or ball.y > screen.get_height() - 10:
        gameOver()
        blocks = []
        bat = Bat()
        ball = Ball()
        i = 0
        score = 0
        for y in range(50, 350, 50):
            for x in range(25, 360, 60):
                blocks.append(Block(x, y, colours[i]))
            i += 1

    # Update the display

    pygame.display.update()

    clock.tick(60)
