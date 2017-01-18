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
        # self.text.insert(INSERT, "Tick: 0")
        self.label.pack()
        self.canvas.pack()

    def update(self):
        self.canvas.update()

    def place_object(self, obj, pos):
        if obj == 'sweeper':
            pad = 3
            data = {"fill": "", "outline": "green", "width": 1}
        else:
            pad = 1
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


# setup GUI and canvas
root = Tk()
board = Board(root)

times = 10  # inputs.NUMTICKS
count = 0

# initialize mines
mines = []
for i in range(0, inputs.NUMMINES):
    x = round(random() * inputs.XSIZE)
    y = round(random() * inputs.YSIZE)
    mines.append({'pos': [x, y], 'id': board.place_object('mine', [x, y])})
sweeper1 = board.place_object('sweeper', [25,25])
sweeper2 = {'pos': [30,30], 'id': board.place_object('sweeper', [30,30])}
board.update()
root.after(5000, board.add_mine)
last_update = time.time()

while count < times:
    count += 1
    # get next positions
    move_mines()
    board.canvas.move(sweeper1, 5, 5)
    sweeper2['pos'][0] += 5
    sweeper2['pos'][1] += 10
    board.canvas.coords(sweeper2['id'], obj_tuple(sweeper2['pos'], 3))
    # update label
    board.label.configure(text="Tick: {}".format(count))
    # wait for 1 / FPS seconds to pass
    delta = time.time() - last_update
    print("{}s elapsed.".format(delta))
    time.sleep(max(0,1/inputs.FPS - delta))
    # update board
    board.update()

    last_update = time.time()

root.mainloop()