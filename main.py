import pygame, json, copy, random, box
from pygame.locals import *


CLR_BG = (234, 212, 252)
CLR_BLACK = (0, 0, 0)
CLR_RED = (255, 0, 0)
CLR_BLUE = (0, 0, 255)
CLR_YELLOW = (200, 200, 0)
FONT_SIZE = 16
NODE_SIZE = 7
MODE_NONE = 0
MODE_DRAG = 1
MODE_NODE = 2
MODE_SELECTION = 3
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

MARGIN = 15
GRID_SIZE = 9
SQUARE_SIZE = 50
FONT_SIZE = 30


def create_grid(to_remove):

    def unUsedInRow(grid, i, num):
        return num not in grid[i]

    def unUsedInCol(grid, j, num):
        for i in range(9):
            if grid[i][j] == num:
                return False
        return True

    def checkIfSafe(grid, i, j, num):
        return unUsedInRow(grid, i, num) and unUsedInCol(grid, j, num) and unUsedInBox(grid, i - i % 3, j - j % 3, num)

    def unUsedInBox(grid, rowStart, colStart, num):
        for i in range(3):
            for j in range(3):
                if grid[rowStart + i][colStart + j] == num:
                    return False
        return True

    def fillBox(grid, row, col):
        for i in range(3):
            for j in range(3):
                while True:

                    # Generate a random number between 1 and 9
                    num = random.randint(1, 9)
                    if unUsedInBox(grid, row, col, num):
                        break
                grid[row + i][col + j] = num

    def fillDiagonal(grid):
        for i in range(0, 9, 3):

            # Fill each 3x3 subgrid diagonally
            fillBox(grid, i, i)

    def fillRemaining(grid, i, j):
        if i == 9:
            return True
        if j == 9:
            return fillRemaining(grid, i + 1, 0)
        if grid[i][j] != 0:
            return fillRemaining(grid, i, j + 1)
        for num in range(1, 10):
            if checkIfSafe(grid, i, j, num):
                grid[i][j] = num
                if fillRemaining(grid, i, j + 1):
                    return True
                grid[i][j] = 0

        return False

    def removeKDigits(grid, k):
        while k > 0:
            cellId = random.randint(0, 80)
            i = cellId // 9
            j = cellId % 9
            if grid[i][j] != 0:
                grid[i][j] = 0
                k -= 1

    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]  # [[0] * GRID_SIZE] * GRID_SIZE
    fillDiagonal(grid)
    fillRemaining(grid, 0, 0)
    removeKDigits(grid, to_remove)
    return grid


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Sudoku")
pygame.font.init()
fnt = pygame.font.SysFont("Courier New Bold", FONT_SIZE)
grid = create_grid(20)
mx, my = -1, -1
keys = {}

running = True

while running:
    for event in pygame.event.get():
        # print(event.type)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif (0 <= mx < GRID_SIZE) and (0 <= my < GRID_SIZE):
                keystate = pygame.key.get_pressed()
                for k in range(pygame.K_1, pygame.K_9 + 1):
                    if keystate[k]:
                        k -= pygame.K_0
                        # print(mx, my)
                        grid[my][mx] = -k
                        break
        elif event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEMOTION:
            mouse = list(pygame.mouse.get_pos())
            mx, my = (mouse[0] - MARGIN) // SQUARE_SIZE, (mouse[1] - MARGIN) // SQUARE_SIZE
            # print(x, y)
            # if (0 <= mouse[0] < GRID_SIZE) and (0 <= mouse[1] < GRID_SIZE):

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (0 <= mx < GRID_SIZE) and (0 <= my < GRID_SIZE):
                if grid[my][mx] < 0:
                    grid[my][mx] = 0
                # if keystate[pygame.K_LEFT]:            self.rot += self.rot_speed
    # bg
    screen.fill(CLR_BG)

    for x in range(GRID_SIZE + 1):
        thickness = 3 if (x % 3) == 0 else 1
        pygame.draw.line(screen, CLR_BLACK, [MARGIN, MARGIN + x * SQUARE_SIZE], [MARGIN + GRID_SIZE * SQUARE_SIZE, MARGIN + x * SQUARE_SIZE], thickness)
        pygame.draw.line(screen, CLR_BLACK, [MARGIN + x * SQUARE_SIZE, MARGIN], [MARGIN + x * SQUARE_SIZE, MARGIN + GRID_SIZE * SQUARE_SIZE], thickness)

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] != 0:
                text_surface = fnt.render(str(abs(grid[y][x])), True, CLR_BLACK if grid[y][x] > 0 else CLR_RED)
                r = text_surface.get_rect()
                screen.blit(text_surface, (MARGIN + x * SQUARE_SIZE + (SQUARE_SIZE - r[2]) // 2, MARGIN + y * SQUARE_SIZE + (SQUARE_SIZE - r[3]) // 2))

    pygame.display.flip()
    clock.tick(10)
