"""
Sonnenschein
"""

import pygame
import random
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0


class Character:
    Size = 100

    def __init__(self, gfx_path: str):
        self.gfx_path = gfx_path
        self.gfx = pygame.image.load(gfx_path)
        w, h = self.gfx.get_width(), self.gfx.get_height()
        long_side = max(w, h)
        self.gfx = pygame.transform.smoothscale(self.gfx, (self.Size * w / long_side, self.Size * h / long_side))
        # Add alpha channel to gfx
        self.gfx = self.gfx.convert_alpha()
        # Make white (up to threshold) to transparent
        for x in range(self.gfx.get_width()):
            for y in range(self.gfx.get_height()):
                color = self.gfx.get_at((x, y))
                if color[0] > 200 and color[1] > 200 and color[2] > 200:
                    color = (255, 255, 255, 0)
                self.gfx.set_at((x, y), color)

    def draw(self):
        pos = get_random_position()
        screen.blit(self.gfx, pos - pygame.Vector2(self.gfx.get_width() / 2, self.gfx.get_height() / 2))


class Area:
    def __init__(self, name: str, pos: pygame.Vector2, size: pygame.Vector2, color: str):
        self.name = name
        self.pos = pos
        self.size = size
        self.color = color

    def draw(self):
        # fill rect
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos, self.size))


players = [
    Character("assets/zebra.jpeg"),
    Character("assets/tiger.jpeg"),
    Character("assets/giraffe2.jpeg"),
    Character("assets/pferd1.jpeg"),
]
areas = [
    Area("sky", pygame.Vector2(0, 0), pygame.Vector2(screen.get_width(), screen.get_height() / 2), "skyblue"),
    Area(
        "ground",
        pygame.Vector2(0, screen.get_height() / 2),
        pygame.Vector2(screen.get_width(), screen.get_height() / 2),
        "white",
    ),
]


def get_random_position():
    x = random.randint(0, screen.get_width())
    y = random.randint(0, screen.get_height())
    return pygame.Vector2(x, y)


class Snow:
    def __init__(self, *, num: int = 100):
        self.positions = [get_random_position() for _ in range(num)]
        self.size = 5
        self.color = "white"

    def draw(self):
        for pos in self.positions:
            pygame.draw.circle(screen, self.color, pos, self.size)

    def update(self):
        for i in range(len(self.positions)):
            self.positions[i].y += 1
            if self.positions[i].y > screen.get_height():
                self.positions[i].x = random.randint(0, screen.get_width())
                self.positions[i].y = 0


snow = Snow()


class Sun:
    def __init__(self):
        self.pos = pygame.Vector2(screen.get_width() * 0.8, screen.get_height() * 0.2)
        self.size = 50
        self.color = "yellow"

    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, self.size)
        # Stripes
        n = 12
        for i in range(n):
            angle = i / n * 2 * math.pi
            pygame.draw.line(
                screen,
                "yellow",
                self.pos,
                self.pos + pygame.Vector2(math.cos(angle), math.sin(angle)) * self.size * 2,
                width=5,
            )


sun = Sun()


font = pygame.font.Font(None, 36)

for area in areas:
    area.draw()
sun.draw()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    add_char = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            add_char = True

    snow.update()

    # fill the screen with a color to wipe away anything from last frame
    # screen.fill("white")

    if add_char:
        i = random.randint(0, len(players) - 1)
        players[i].draw()

    snow.draw()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
