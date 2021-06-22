import pygame
from pygame.locals import *
from algorithm import *
from config import *
import random
import sys

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
font = pygame.font.Font('FreeSansBold.ttf', 50)
pygame.display.set_caption("MineSweeper")



class Cell:
    def __init__(self):
        self.mine = False
        self.clicked = False
        self.flag = False
        self.num = None
        self.rect = None

    def click(self):
        self.clicked = True

    def set_mine(self):
        self.mine = True

    def set_flag(self):
        self.flag = True



class GetSurrounding:
    def __init__(self, game):
        self.game = game

    def get_above_point(self, pos):
        return self.game[pos[0]-1][pos[1]]

    def get_under_point(self, pos):
        return self.game[pos[0]+1][pos[1]]

    def get_left_point(self, pos):
        return self.game[pos[0]][pos[1]-1]

    def get_right_point(self, pos):
        return self.game[pos[0]][pos[1]+1]

    def get_above_left_point(self, pos):
        return self.game[pos[0]-1][pos[1]-1]

    def get_above_right_point(self, pos):
        return self.game[pos[0]-1][pos[1]+1]

    def get_under_left_point(self, pos):
        return self.game[pos[0]+1][pos[1]-1]

    def get_under_right_point(self, pos):
        return self.game[pos[0]+1][pos[1]+1]


    def get_surrounding_points(self, pos):
        # top left corner
        if pos == (0,0):
            points = [self.get_right_point(pos), self.get_under_right_point(pos), self.get_under_point(pos)]
        # top right corner
        elif pos == (0, len(self.game[0])-1):
            points = [self.get_left_point(pos), self.get_under_point(pos), self.get_under_left_point(pos)]
        # bottom left corner
        elif pos == (len(self.game)-1, 0):
            points = [self.get_above_point(pos), self.get_above_right_point(pos), self.get_right_point(pos)]
        # bottom right corner
        elif pos == (len(self.game)-1, len(self.game[0])-1):
            points = [self.get_left_point(pos), self.get_above_left_point(pos), self.get_above_point(pos)]
        # first row
        elif pos[0] == 0:
            points = [self.get_left_point(pos), self.get_right_point(pos), self.get_under_left_point(pos), self.get_under_point(pos), self.get_under_right_point(pos)]
        # last row
        elif pos[0] == len(self.game)-1:
            points = [self.get_left_point(pos), self.get_right_point(pos), self.get_above_left_point(pos), self.get_above_point(pos), self.get_above_right_point(pos)]
        # first column
        elif pos[1] == 0:
            points = [self.get_above_point(pos), self.get_above_right_point(pos), self.get_right_point(pos), self.get_under_right_point(pos), self.get_under_point(pos)]
        # last column
        elif pos[1] == len(self.game[0])-1:
            points = [self.get_above_point(pos), self.get_under_point(pos), self.get_above_left_point(pos), self.get_under_left_point(pos), self.get_left_point(pos)]
        # any other point
        else:
            points = [self.get_above_point(pos), self.get_under_point(pos), self.get_left_point(pos), self.get_right_point(pos), self.get_above_left_point(pos),
             self.get_above_right_point(pos), self.get_under_left_point(pos), self.get_under_right_point(pos)]
        return points


    def fill_point(self, pos):
        if self.game[pos[0]][pos[1]].mine:
            return "*"

        count = 0
        mines = self.get_surrounding_points(pos)
        for point in mines:
            if point.mine:
                count += 1
        return count



def generate_game(n):
    matrix = []
    for c in range(n):
        c = []
        for r in range(n):
            c.append(Cell())
        matrix.append(c)
    count = 0
    while count < 15:
        row = random.randint(0,11)
        col = random.randint(0,11)
        if not matrix[row][col].mine:
            matrix[row][col].set_mine()
            count += 1
    return matrix



def draw_board(board, content):
    screen.fill(BLACK)
    for y, row in enumerate(board):
        for ix, cell in enumerate(row):
            rect = pygame.Rect((MARGIN + WIDTH) * ix + MARGIN, (MARGIN + HEIGHT) * y + MARGIN, WIDTH, HEIGHT)
            cell.rect = rect
            pygame.draw.rect(screen, GRAY, rect)
            if cell.clicked:
                num = content.fill_point((y, ix))
                cell.num = num
                text = font.render(str(num), True, BLACK)
                screen.blit(text, rect)
                if num == 0:
                    for point in content.get_surrounding_points((y, ix)):
                        point.click()
            else:
                pygame.draw.rect(screen, GRAY, rect)



game = generate_game(SIZE)
content = GetSurrounding(game)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for row in game:
                for cell in row:
                    if cell.rect.collidepoint(pos):
                        cell.click()

    draw_board(game, content)
        
    pygame.display.flip()
