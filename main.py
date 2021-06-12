import pygame
from queue import PriorityQueue

pygame.init()
width = 700
height = 760
rows = 50
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("A* Path Finding Visualizer")
pygame.display.set_icon(pygame.image.load("./images/img.png"))

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 168, 0)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)
active = [1, 0, 0]
font = pygame.font.SysFont(None, 17)


class Node:
    def __init__(self, row, col, width, tot_row):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbour = []
        self.width = width
        self.tot_row = tot_row

    def getPos(self):
        return self.row, self.col

    def isClosed(self):
        return self.color == RED

    def isOpen(self):
        return self.color == GREEN

    def isStart(self):
        return self.color == ORANGE

    def isEnd(self):
        return self.color == BLUE

    def isBarrier(self):
        return self.color == BLACK

    def reset(self):
        self.color = WHITE

    def makeClosed(self):
        self.color = RED

    def makeOpen(self):
        self.color = GREEN

    def makeStart(self):
        self.color = ORANGE

    def makeEnd(self):
        self.color = BLUE

    def makeBarrier(self):
        self.color = BLACK

    def makePath(self):
        self.color = PURPLE

    def draw(self, window):
        pygame.draw.rect(
            window, self.color, (self.x, self.y, self.width, self.width))

    def updateNeighbour(self, grid):
        self.neighbour = []
        if self.row < self.tot_row - 1 and not grid[self.row + 1][self.col].isBarrier():
            self.neighbour.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].isBarrier():
            self.neighbour.append(grid[self.row - 1][self.col])

        if self.col < self.tot_row - 1 and not grid[self.row][self.col + 1].isBarrier():
            self.neighbour.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].isBarrier():
            self.neighbour.append(grid[self.row][self.col - 1])

    def __lt__(self):
        return False


def h(p1, p2):
    ind = active.index(1)
    if ind == 0:
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    elif ind == 1:
        return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
    else:
        dx = abs(p1[0] - p2[0])
        dy = abs(p1[1] - p2[1])
        return (dx + dy) + (2**0.5 + 2 + 1) * min(dx, dy)


def AStarAlgo(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    gScore = {node: float("inf") for r in grid for node in r}
    gScore[start] = 0
    fScore = {node: float("inf") for r in grid for node in r}
    fScore[start] = h(start.getPos(), end.getPos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            while current in came_from:
                current = came_from[current]
                current.makePath()
                draw()
            return True

        for neighbour in current.neighbour:
            temp_gScore = gScore[current] + 1
            if temp_gScore < gScore[neighbour]:
                came_from[neighbour] = current
                gScore[neighbour] = temp_gScore
                fScore[neighbour] = temp_gScore + \
                    h(neighbour.getPos(), end.getPos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((fScore[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.makeOpen()

        draw()
        if current != start:
            current.makeClosed()
    return False


def getGrid(row, width):
    grid = []
    gap = width // row
    for i in range(row):
        grid.append([])
        for j in range(row):
            node = Node(i, j, gap, row)
            grid[i].append(node)
    return grid


def drawRadioButton(win, width):
    for i in range(len(active)):
        if active[i] == 1:
            pygame.draw.circle(win, BLUE, (540, width + 12 + (19 * i)), 7, 2)
            pygame.draw.circle(win, BLUE, (540, width + 12 + (19 * i)), 3)
        else:
            pygame.draw.circle(win, BLACK, (540, width + 12 + (19 * i)), 7, 2)


def changeActive(win, width, ind):
    global active
    active = [0, 0, 0]
    active[ind] = 1
    drawRadioButton(win, width)


def drawGrid(win, row, width):
    gap = width // row
    for i in range(row + 1):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))


def writeText(win, msg, color, pos):
    text = font.render(msg, True, color)
    win.blit(text, pos)


def drawCellText(win, color, pos, msg):
    text = font.render(msg, True, BLACK)
    win.blit(text, (pos[0] + pos[2] + 3, pos[1] + 2))
    pygame.draw.rect(win, color, pos)


def draw(win, grid, row, width):
    win.fill(WHITE)
    writeText(win, "SPACE - Start visualization", "Red",
              (10, width + 5))
    writeText(win, "C - clear Screen", "Red", (10, width + 18))
    writeText(win, "Left Click - Add start/end/barrier",
              "Red", (10, width + 31))
    writeText(win, "Right Click - Remove start/end/barrier",
              "Red", (10, width + 44))

    drawCellText(win, ORANGE, (250, width + 5, width //
                               row - 1, width // row - 1), "-Start Node")
    drawCellText(win, BLUE, (250, width + (width // row) + 10, width //
                             row - 1, width // row - 1), "-End Node")
    drawCellText(win, BLACK, (250, width + (2 * (width // row)) + 15, width //
                              row - 1, width // row - 1), "-Barrier")

    drawCellText(win, PURPLE, (390, width + 5, width //
                               row - 1, width // row - 1), "-Path")
    drawCellText(win, RED, (390, width + (width // row) + 10, width //
                            row - 1, width // row - 1), "-Closed Node")
    drawCellText(win, GREEN, (390, width + (2 * (width // row)) + 15, width //
                              row - 1, width // row - 1), "-Open Node")
    drawRadioButton(win, width)
    writeText(win, "Use Manhattan Distance", "Black", (555, width + 6))
    writeText(win, "Use Diagonal Distance", "Black", (555, width + 25))
    writeText(win, "Use Euclidean Distance", "Black", (555, width + 44))

    for r in grid:
        for node in r:
            node.draw(win)

    drawGrid(win, row, width)
    pygame.display.update()


def getClickedPos(pos, row, width):
    gap = width // row
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def main(win, row, width):
    grid = getGrid(row, width)
    start = None
    end = None
    running = True
    started = False

    while running:
        draw(win, grid, row, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[1] < width:
                    rows, col = getClickedPos(pos, row, width)
                    node = grid[rows][col]
                    if not start and node != end:
                        start = node
                        start.makeStart()

                    if not end and node != start:
                        end = node
                        end.makeEnd()

                    if node != start and node != end:
                        node.makeBarrier()
                x, y = pos
                if x in range(536, 545):
                    if y in range(width + 7, width + 15):
                        changeActive(win, width, 0)
                    if y in range(width + 27, width + 34):
                        changeActive(win, width, 1)
                    if y in range(width + 47, width + 55):
                        changeActive(win, width, 2)

            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                if pos[1] < width:
                    rows, col = getClickedPos(pos, row, width)
                    node = grid[rows][col]
                    node.reset()
                    if node == start:
                        start = None
                    if node == end:
                        end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    grid = getGrid(row, width)
                    start = None
                    end = None

                if event.key == pygame.K_SPACE and start and end:
                    started = True

                    for r in grid:
                        for n in r:
                            n.updateNeighbour(grid)

                    AStarAlgo(lambda: draw(win, grid, row, width),
                              grid, start, end)
                    started = False
                    start.makeStart()
                    end.makeEnd()
    pygame.quit()


main(window, rows, width)
