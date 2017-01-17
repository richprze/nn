from tkinter import *
from random import random
from nn_classes import NeuralNet, Sweeper, Population
import math
import inputs

class Board:
    def __init__(self):
        self.times = 10 # inputs.NUMTICKS
        self.count = 0
        # setup GUI and canvas
        self.root = Tk()
        self.canvas = Canvas(self.root, bg="white", height=inputs.YSIZE, width=inputs.XSIZE)

        self.label = Label(self.root, text="Tick: 0")
        # self.text.insert(INSERT, "Tick: 0")
        self.label.pack()

        # setup initial mines positions and draw
        self.mines = []
        self.mines_positions = []
        for i in range(0, inputs.NUMMINES):
            pos, data = self.place_mine()
            self.mines.append(self.canvas.create_rectangle(data))
            self.mines_positions.append(pos)

        # TEST - place sweepers
        self.sweepers = []
        for i in range(0,10):
            x = round(random() * inputs.XSIZE)
            y = round(random() * inputs.YSIZE)
            self.sweepers.append({'pos': [x,y], 'elem': self.place_sweeper([x,y])})
        print(len(self.sweepers))

        self.canvas.pack()
        print("before first after call to animate")
        self.canvas.after(500, self.move_mines_random_1)
        self.root.mainloop()

    def move_mines_random_1(self):
        self.count += 1
        print("in mines")
        for mine in self.mines:
            x = -5 if random() < .5 else 5
            y = -5 if random() < .5 else 5
            self.canvas.move(mine, x, y)
        self.label.configure(text="Tick: {}".format(self.count))
        self.canvas.move(self.sweepers[0]['elem'], 10, 10)
        self.canvas.update()
        if self.count < self.times:
            self.canvas.after(500, self.move_mines_random_1)

    def place_mine(self):
        x = round(random() * inputs.XSIZE)
        y = round(random() * inputs.YSIZE)
        data = [x-1, y-1, x+1, y+1, {'fill': 'red', 'outline': 'red'}]
        return [x, y], data

    def place_sweeper(self, pos):
        # size is 6 x 6 square
        x1 = pos[0] - 3
        y1 = pos[1] - 3
        x2 = pos[0] + 3
        y2 = pos[1] + 3
        return self.canvas.create_rectangle(x1, y1, x2, y2, fill="", outline="green", width=1)

    def move_sweeper(self, tracks, rotation):
        # takes left and right track velocities / forces (outputs from NN) and moves the sweeper
        left = tracks[0]
        right = tracks[1]

        # calculate rotational force
        rot_delta = left - right

        # Force ~ to direction; limit to 1 radian turning radius / 57 degrees
        rot_delta = min(inputs.MAXTURNRATE, max(-inputs.MAXTURNRATE, rot_delta))

        # update sweeper's facing direction
        rotation += rot_delta

        # calculate direction unit vector
        look = [math.sin(rotation), math.cos(rotation)] # x,y

        # calculate absolute speed
        speed = left + right

        # new position
        pos = [x * speed for x in look]

        # account for window and wrap around
        # if x is negative, have it come in from the right
        if pos[0] < 0: pos[0] = inputs.XSIZE + pos[0]
        # if x is greater than window size, have it come in the left
        elif pos[0] > inputs.XSIZE: pos[0] = pos[0] - inputs.XSIZE

        # if y is negative, have it come up from bottom
        if pos[1] < 0: pos[1] = inputs.YSIZE + pos[1]
        # if y is > window size, have it come down from top
        elif pos[1] > inputs.YSIZE: pos[1] = pos[1] - inputs.YSIZE

        return pos

# Board()
board = Board()


# sweeper class:
# has function that moves sweeper:
    # -> sets new pos coords
    # -> then redraws it in new position? OR move it by delta...

# vector maths
def vec_dist(vec1, vec2):
    return math.sqrt((vec1[0]-vec2[0])**2 + (vec1[1]-vec2[1])**2)

def vec_diff(sweeper, mine):
    # should be [mine] - [sweeper] to get vec direction from sweeper to mine
    return [mine[0]-sweeper[0],mine[1]-sweeper[1]]