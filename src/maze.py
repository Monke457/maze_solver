from graphics import Cell, Point
import time
import random

directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]


class Maze():
    _cells = []

    def __init__(self,
                 x1, y1,
                 num_rows, num_cols,
                 cell_size_x, cell_size_y,
                 win=None, seed=None):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win

        if seed is not None:
            seed = random.seed(seed)
        self.__seed = seed

        self.__create_cells()

    def __create_cells(self):
        for col in range(self.__num_cols):
            if len(self._cells)-1 < col:
                self._cells.append([])

            for row in range(self.__num_rows):
                if len(self._cells[col])-1 >= row:
                    continue
                x = self.__x1 + col * self.__cell_size_x
                y = self.__y1 + row * self.__cell_size_y
                p1 = Point(x, y)
                p2 = Point(x + self.__cell_size_x, y + self.__cell_size_y)
                cell = Cell(p1, p2, self.__win)
                self._cells[col].append(cell)

        if self.__win is None:
            return

        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        self._cells[i][j].draw()
        self.__animate()

    def __animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_left_wall = False
        self._cells[-1][-1].has_right_wall = False
        self.__draw_cell(0, 0)
        self.__draw_cell(-1, -1)

    def _break_walls_r(self, i, j):
        self._cells[i][j]._visited = True
        while True:
            to_visit = []
            for d in directions:
                x = i + d[0]
                y = j + d[1]
                if (
                    x < 0
                    or y < 0
                    or x >= len(self._cells)
                    or y >= len(self._cells[x])
                    or self._cells[x][y]._visited
                ):
                    continue
                to_visit.append((x, y))
            if len(to_visit) == 0:
                self.__draw_cell(i, j)
                return

            (x, y) = to_visit[random.randrange(0, len(to_visit))]

            if x == i:
                if y > j:
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[x][y].has_top_wall = False
                else:
                    self._cells[i][j].has_top_wall = False
                    self._cells[x][y].has_bottom_wall = False
            else:
                if x > i:
                    self._cells[i][j].has_right_wall = False
                    self._cells[x][y].has_left_wall = False
                else:
                    self._cells[i][j].has_left_wall = False
                    self._cells[x][y].has_right_wall = False

            self._break_walls_r(x, y)

    def _reset_visited(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._cells[i][j]._visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self.__animate()
        self._cells[i][j]._visited = True

        if i == len(self._cells)-1 and j == len(self._cells[i])-1:
            return True

        for d in directions:
            x = i + d[0]
            y = j + d[1]
            if (
                x < 0
                or y < 0
                or x >= len(self._cells)
                or y >= len(self._cells[x])
                or self._cells[x][y]._visited
                or self.__wall_between(i, j, x, y)
            ):
                continue
            self._cells[i][j].draw_move(self._cells[x][y])
            if self._solve_r(x, y):
                return True
            self._cells[i][j].draw_move(self._cells[x][y], undo=True)
        return False

    def __wall_between(self, x1, y1, x2, y2):
        if x2 == x1:
            if y2 > y1:
                return (self._cells[x1][y1].has_bottom_wall
                        or self._cells[x2][y2].has_top_wall)
            else:
                return (self._cells[x1][y1].has_top_wall
                        or self._cells[x2][y2].has_bottom_wall)
        else:
            if x2 > x1:
                return (self._cells[x1][y1].has_right_wall
                        or self._cells[x2][y2].has_left_wall)
            else:
                return (self._cells[x1][y1].has_left_wall
                        or self._cells[x2][y2].has_right_wall)
