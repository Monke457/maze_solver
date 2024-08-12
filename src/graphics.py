from tkinter import Tk, BOTH, Canvas


class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Sovler")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(
                self.__root, bg="black", width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False

    def draw_line(self, line, fill_color="white"):
        line.draw(self.__canvas, fill_color)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("Window closed...")

    def close(self):
        self.__running = False


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line():
    def __init__(self, p1, p2):
        self.__p1 = p1
        self.__p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(
                self.__p1.x, self.__p1.y,
                self.__p2.x, self.__p2.y,
                fill=fill_color, width=2)


class Cell():
    def __init__(self, p1, p2, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = p1.x
        self.__y1 = p1.y
        self.__x2 = p2.x
        self.__y2 = p2.y
        self.__win = win
        self._visited = False

    def draw(self):
        if self.__win is None:
            return

        p1 = Point(self.__x1, self.__y1)
        p2 = Point(self.__x1, self.__y2)
        if self.has_left_wall:
            self.__win.draw_line(Line(p1, p2))
        else:
            self.__win.draw_line(Line(p1, p2), "black")

        p1 = Point(self.__x2, self.__y1)
        p2 = Point(self.__x2, self.__y2)
        if self.has_right_wall:
            self.__win.draw_line(Line(p1, p2))
        else:
            self.__win.draw_line(Line(p1, p2), "black")

        p1 = Point(self.__x1, self.__y1)
        p2 = Point(self.__x2, self.__y1)
        if self.has_top_wall:
            self.__win.draw_line(Line(p1, p2))
        else:
            self.__win.draw_line(Line(p1, p2), "black")

        p1 = Point(self.__x1, self.__y2)
        p2 = Point(self.__x2, self.__y2)
        if self.has_bottom_wall:
            self.__win.draw_line(Line(p1, p2))
        else:
            self.__win.draw_line(Line(p1, p2), "black")

    def draw_move(self, to_cell, undo=False):
        if self.__win is None:
            return

        x1 = (self.__x1 + self.__x2) // 2
        x2 = (to_cell.__x1 + to_cell.__x2) // 2
        y1 = (self.__y1 + self.__y2) // 2
        y2 = (to_cell.__y1 + to_cell.__y2) // 2

        p1 = Point(x1, y1)
        p2 = Point(x2, y2)

        fill = "red"
        if undo:
            fill = "grey"
        self.__win.draw_line(Line(p1, p2), fill)
