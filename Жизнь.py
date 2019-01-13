import pygame
import copy


screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.left = 10
        self.top = 10
        self.cell_size = 30


    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.board[j][i] == 1:
                    pygame.draw.rect(screen, pygame.Color("Green"), (self.left + i * self.cell_size,
                                                                     self.top + j * self.cell_size,
                                                                     self.cell_size, self.cell_size), 0)
                pygame.draw.rect(screen, pygame.Color("White"), (self.left + i * self.cell_size,
                                                                 self.top + j * self.cell_size,
                                                                 self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[0] <= self.left + (self.width) * self.cell_size \
                and self.top <= mouse_pos[1] <= self.top + (self.height) * self.cell_size:
            return (mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.top) // self.cell_size
        else:
            return None

    def on_click(self, cell_coords):
        x, y = cell_coords
        self.board[y][x] = not self.board[y][x]

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        print(cell)
        if cell:
            self.on_click(cell)


class Life(Board):
    def __init__(self, width, height):
        super(Life, self).__init__(width, height)

    def next_move(self):
        currentTurn = copy.deepcopy(self.board)
        coords = [(-1, 1), (-1, 0), (-1, -1), (0, -1),
                       (0, 1), (1, -1), (1, 0), (1, 1)]
        nextTurn = []
        for i in range(len(currentTurn)):
            row = []
            for j in range(len(currentTurn[i])):
                life = 0
                for x, y in coords:
                    if currentTurn[(i + x) % len(currentTurn[i])][(j + y) % len(currentTurn)] == 1:
                        life += 1

                if currentTurn[i][j] == 0:
                    if life == 3:
                        row.append(1)
                    else:
                        row.append(0)
                else:
                    if life == 2 or life == 3:
                        row.append(1)
                    else:
                        row.append(0)
            nextTurn.append(row)
        self.board = copy.deepcopy(nextTurn)


pygame.init()
life = Life(45, 45)
life.set_view(0, 0, 20)
running = True
MYEVENTTYPE = 30
start = False
speed = 500
pygame.time.set_timer(MYEVENTTYPE, speed)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MYEVENTTYPE and start:
            life.next_move()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not start:
                if event.button == 3:
                    life.get_click(event.pos)

            if event.button == 1:
                start = True

            if event.button == 4:
                if speed - 20 > 0:
                    speed -= 20
                    pygame.time.set_timer(MYEVENTTYPE, speed)

            if event.button == 5:
                if speed + 20 <= 1000:
                    speed += 20
                    pygame.time.set_timer(MYEVENTTYPE, speed)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = not start
    screen.fill((0, 0, 0))
    life.render()
    pygame.display.flip()