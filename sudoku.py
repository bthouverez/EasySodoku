import pygame
import sys

pygame.init()

# Set this to False if you don't want to see progress
PROGRESS = False

data = []
'''
data.append("""
000600400
700003600
000091080
000000000
050180003
000306045
040200060
903000000
020000100""")

data.append("""
000260701
680070090
190004500
820100040
004602900
050003028
009300074
040050036
703018000""")
'''
data.append("""
800000000
003600000
070090200
050007000
000045700
000100030
001000068
008500010
090000400
""")
'''
data.append("""
0120070560
507932080
000001000
010240050
308000402
070085010
000700000
080423701
034010028
""")
'''

# Window settings
WIDTH = 9
HEIGHT = 9
BOX_SIZE = 50

# Internal data
GRID = []
D = []
for l in data[0].split():
    GRID.append([int(i) for i in list(l)])
    D.append([int(i) for i in list(l)])


# STACK - Last In First Out
class Lifo:
    def __init__(self):
        self._data = []

    def put(self, e):
        self._data.append(e)

    def pop(self):
        if len(self._data):
            return self._data.pop()

# Return values of 3x3 block of l,c
def block(l, c):
    l = l // 3 * 3
    c = c // 3 * 3
    t = []
    for i in range(l, l + 3):
        for j in range(c, c + 3):
            t.append(GRID[i][j])
    return t


# Return values of column of l,c
def col(l, c):
    t = []
    for i in range(9):
        t.append(GRID[i][c])
    return t


# Return values of row of l,c
def row(l, c):
    return GRID[l]


def valid(n, l, c):
    return n not in row(l, c) and n not in col(l, c) and n not in block(l, c)


def draw():
    screen.fill(WHITE)
    for j in range(9):
        for i in range(9):
            cx = j*BOX_SIZE
            cy = i*BOX_SIZE
            if GRID[i][j] != 0:
                color = BLACK if D[i][j] != 0 else RED
                label = font.render(str(GRID[i][j]), 1, color)
                screen.blit(label, (cx+15, cy+5))
            r = pygame.Rect(cx, cy, BOX_SIZE, BOX_SIZE)
            pygame.draw.rect(screen, GREY, r, 1)
    for j in range(3):
        for i in range(3):
            r = pygame.Rect(i*BOX_SIZE*3, j*BOX_SIZE*3, BOX_SIZE*3, BOX_SIZE*3)
            pygame.draw.rect(screen, BLACK, r, 3)
    pygame.display.flip()
    pygame.time.delay(20)


size = WIDTH * BOX_SIZE, HEIGHT * BOX_SIZE
BLACK = (000, 000, 000)
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
ORANGE = (255, 127, 000)
RED = (255, 000, 000)

screen = pygame.display.set_mode(size)
screen.fill(WHITE)

pygame.display.set_caption('Easy Sudoku')
font = pygame.font.SysFont('monospace', 40, True)


X=Y=0
lifo = Lifo()
pop = False
draw()
pygame.time.delay(500)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    if X*9+Y < 81:
        validated = False
        if GRID[X][Y] == 0 or pop:
            pop = False
            val = GRID[X][Y]
            for i in range(val, 9):
                if valid(i + 1, X, Y):
                    lifo.put((X, Y))
                    validated = True
                    GRID[X][Y] = i + 1
                    break
            if not validated:
                GRID[X][Y] = 0
                X, Y = lifo.pop()
                pop = True
                continue
    if X * 9 + Y == 80 or PROGRESS:
        draw()

    Y += 1
    if Y == 9:
        X += 1
        Y = 0
        