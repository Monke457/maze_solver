from graphics import Window
from maze import Maze


def main():
    win = Window(800, 600)
    maze = Maze(40, 40, 13, 18, 40, 40, win)
    maze._break_entrance_and_exit()
    maze._break_walls_r(0, 1)
    maze._reset_visited()
    maze.solve()
    win.wait_for_close()


main()
