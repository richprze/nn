from tkinter import *
from random import random
import math
import inputs
import time

class Board(object):
    def __init__(self, parent):
        self.root = parent
        self.canvas = Canvas(self.root, bg="white", height=inputs.YSIZE, width=inputs.XSIZE)
        self.label = Label(self.root, text="Tick: 0")
        self.label.pack()
        self.canvas.pack()

    def update(self):
        self.canvas.update()

    def place_object(self, obj, pos):
        if obj == 'sweeper':
            pad = inputs.SWEEPERSIZE
            data = {"fill": "", "outline": "green", "width": 1}
        else:
            pad = inputs.MINESIZE
            data = {"fill": "red", "outline": "red"}

        return self.canvas.create_rectangle(obj_tuple(pos, pad), data)

    def add_mine(self):
        self.canvas.create_rectangle(150,150,152,152, fill="blue", outline="blue")
        self.canvas.update()

def obj_tuple(pos, pad):
    return (pos[0] - pad, pos[1] - pad, pos[0] + pad, pos[1] + pad)

def move_mines():
    for mine in mines:
        x = -5 if random() < .5 else 5
        y = -5 if random() < .5 else 5
        board.canvas.move(mine['id'], x, y)
        mine['pos'] = [mine['pos'][0] + x, mine['pos'][1] + y]
        # mine['pos'] = [x+y for x,y in zip(min['pos'], [x,y])]

# vector maths
def vec_dist(vec1, vec2):
    return math.sqrt((vec1[0]-vec2[0])**2 + (vec1[1]-vec2[1])**2)

def vec_diff(sweeper, mine):
    # should be [mine] - [sweeper] to get vec direction from sweeper to mine
    return [mine[0]-sweeper[0],mine[1]-sweeper[1]]


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
    look = [math.sin(rotation), math.cos(rotation)]  # x,y

    # calculate absolute speed
    speed = left + right

    # vector to new position
    to_new_pos = [x * speed for x in look]

    # new position (sum the two vectors)
    pos = [x + y for x, y in zip(pos, to_new_pos)]

    # account for window and wrap around
    # if x is negative, have it come in from the right
    if pos[0] < 0:
        pos[0] = inputs.XSIZE + pos[0]
    # if x is greater than window size, have it come in the left
    elif pos[0] > inputs.XSIZE:
        pos[0] = pos[0] - inputs.XSIZE

    # if y is negative, have it come up from bottom
    if pos[1] < 0:
        pos[1] = inputs.YSIZE + pos[1]
    # if y is > window size, have it come down from top
    elif pos[1] > inputs.YSIZE:
        pos[1] = pos[1] - inputs.YSIZE

    return pos


print(__name__)

# setup GUI and canvas
root = Tk()
board = Board(root)

times = 10  # inputs.NUMTICKS

# initialize mines
mines = []
for i in range(0, inputs.NUMMINES):
    x = round(random() * inputs.XSIZE)
    y = round(random() * inputs.YSIZE)
    mines.append({'pos': [x, y], 'id': board.place_object('mine', [x, y])})
# initialize sweepers
sweeper1 = board.place_object('sweeper', [25,25])
sweeper2 = {'pos': [30,30], 'id': board.place_object('sweeper', [30,30])}
board.update()
root.after(5000, board.add_mine)
last_update = time.time()

for i in range(0,times):
    # get next positions
    move_mines()
    board.canvas.move(sweeper1, 5, 5)
    sweeper2['pos'][0] += 5
    sweeper2['pos'][1] += 10
    board.canvas.coords(sweeper2['id'], obj_tuple(sweeper2['pos'], inputs.SWEEPERSIZE))
    # update label
    board.label.configure(text="Tick: {}".format(i+1))
    # wait for 1 / FPS seconds to pass
    delta = time.time() - last_update
    print("{}s elapsed.".format(delta))
    time.sleep(max(0,1/inputs.FPS - delta))
    # update board
    board.update()

    last_update = time.time()

root.mainloop()
