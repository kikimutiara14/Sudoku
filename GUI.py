# GUI.py
import pygame
from solver import solve, valid
from generator import generate
import time
pygame.font.init()


class Grid:
    def __init__(self, difficulty):
        board = generate(difficulty)
        self.rows = 9
        self.cols = 9
        self.cubes = [[Cube(board[i][j], i, j, 540, 540) for j in range(9)] for i in range(9)]
        self.width = 540
        self.height = 540
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 560))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw(win)


def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat

def game_intro():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Main Menu")
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        win.fill((255,255,255))
        fnt = pygame.font.SysFont("comicsans", 40)

        text = fnt.render("Select Difficulty", 1, (0,0,0))
        win.blit(text, (155, 155))

        text = fnt.render("Easy", 1, (0,0,0))
        pygame.draw.rect(win, (0, 255, 0), (540/2 - 50, 200, 100, 40))
        win.blit(text, (235, 205))

        text = fnt.render("Normal", 1, (0,0,0))
        pygame.draw.rect(win, (255, 255, 0), (540/2 - 50, 250, 100, 40))
        win.blit(text, (220, 255))

        text = fnt.render("Hard", 1, (0,0,0))
        pygame.draw.rect(win, (255, 0, 0), (540/2 - 50, 300, 100, 40))
        win.blit(text, (235, 305))
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] < 320 and pos[0] > 220 and pos[1] < 240 and pos[1] > 200:
                    intro = False
                    return 'easy'
                elif pos[0] < 320 and pos[0] > 220 and pos[1] < 290 and pos[1] > 250:
                    intro = False
                    return 'normal'
                elif pos[0] < 320 and pos[0] > 220 and pos[1] < 340 and pos[1] > 300:
                    intro = False
                    return 'hard'


def main(difficulty):
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(difficulty)
    key = None
    run = True
    start = time.time()
    strikes = 0
    board.select(0, 0)
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    key = None
                if event.key == pygame.K_DOWN and board.selected[0] < 8:
                    board.select(board.selected[0] + 1, board.selected[1])
                    key = None
                if event.key == pygame.K_UP and board.selected[0] > 0:
                    board.select(board.selected[0] - 1, board.selected[1])
                    key = None
                if event.key == pygame.K_RIGHT and board.selected[1] < 8:
                    board.select(board.selected[0], board.selected[1] + 1)
                    key = None
                if event.key == pygame.K_LEFT and board.selected[1] > 0:
                    board.select(board.selected[0], board.selected[1] - 1)
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                            if strikes >= 3:
                                run = False
                        key = None

                        if board.is_finished():
                            print("Game over")
                            run = False
                if event.key == pygame.K_a:
                    for num in range(1, 10):
                        board.place(num)
                if event.key == pygame.K_SPACE:
                    for i in range(9):
                        for j in range(9):
                            board.select(i, j)
                            for num in range(1, 10):
                                board.place(num)
                                

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()

difficulty = game_intro()
main(difficulty)
pygame.quit()