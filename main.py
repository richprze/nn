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
        for i in range(0, inputs.NUMMINES):
            x = round(random() * inputs.XSIZE)
            y = round(random() * inputs.YSIZE)
            self.mines.append({'pos': [x,y], 'elem': self.place_object('mine', [x,y])})

        # TEST - place sweepers
        self.sweepers = []
        for i in range(0,10):
            x = round(random() * inputs.XSIZE)
            y = round(random() * inputs.YSIZE)
            self.sweepers.append({'pos': [x,y], 'elem': self.place_object('sweeper', [x,y])})
        print(len(self.sweepers))

        self.canvas.pack()
        print("before first after call to animate")
        self.canvas.after(500, self.move_mines_random_1)
        # self.root.mainloop()

    def move_mines_random_1(self):
        self.count += 1
        print("in mines")

        print("mine 0 and 1 positions:")
        print("mine 0 - x: {}, y: {}".format(self.mines[0]['pos'][0], self.mines[0]['pos'][1]))
        print("mine 1 - x: {}, y: {}".format(self.mines[1]['pos'][0], self.mines[1]['pos'][1]))

        for mine in self.mines:
            x = -5 if random() < .5 else 5
            y = -5 if random() < .5 else 5
            self.canvas.move(mine['elem'], x, y)
            mine['pos'] = [mine['pos'][0] + x, mine['pos'][1] + y]
            # mine['pos'] = [x+y for x,y in zip(min['pos'], [x,y])]

        print("mine 0 and 1 positions after move")
        print("mine 0 - x: {}, y: {}".format(self.mines[0]['pos'][0], self.mines[0]['pos'][1]))
        print("mine 1 - x: {}, y: {}".format(self.mines[1]['pos'][0], self.mines[1]['pos'][1]))

        self.label.configure(text="Tick: {}".format(self.count))
        self.canvas.move(self.sweepers[0]['elem'], 10, 10)
        print("the sweepers[0] data:")
        print(self.sweepers[0])
        self.canvas.update()
        if self.count < self.times:
            self.canvas.after(500, self.move_mines_random_1)

    def place_object(self, obj, pos):
        if obj == 'sweeper': 
            pad = 3
            data = {"fill": "", "outline": "green", "width": 1}
        else: 
            pad = 1
            data = {"fill": "red", "outline": "red"}

        x1 = pos[0] - pad
        y1 = pos[1] - pad
        x2 = pos[0] + pad
        y2 = pos[1] + pad
        return self.canvas.create_rectangle(x1, y1, x2, y2, data)

    def move_sweeper(self, tracks, rotation, pos):
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

        # vector to new position
        to_new_pos = [x * speed for x in look]

        # new position (sum the two vectors)
        pos = [x+y for x,y in zip(pos, to_new_pos)]

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
