from tkinter import *
from random import random
from nn_classes import NeuralNet, Sweeper, Population, obj_tuple
import time
import inputs
import settings

class Board(object):
    def __init__(self, parent):
        self.root = parent
        self.canvas = Canvas(self.root, bg="white", height=inputs.YSIZE, width=inputs.XSIZE)
        self.label = Label(self.root, text="Tick: 0 | Mines: 0")
        self.label.pack()
        self.canvas.pack()

    def update(self):
        self.canvas.update()

    def place_object(self, obj, pos):
        if obj == 'sweeper':
            pad = inputs.SWEEPERSIZE
            data = {"fill": "", "outline": "green", "width": 1}
        elif obj == 'new mine':
            pad = inputs.MINESIZE
            data = {"fill": "red", "outline": "red"}
        else:
            pad = inputs.MINESIZE
            data = {"fill": "#F5A9A9", "outline": "#F5A9A9"}

        return self.canvas.create_rectangle(obj_tuple(pos, pad), data)

    def draw_line(self, start, end):
        return self.canvas.create_line(start[0], start[1], end[0], end[1], fill="#D6D6D6")

    def add_mine(self):
        self.canvas.create_rectangle(150,150,152,152, fill="blue", outline="blue")
        self.canvas.update()

def move_mines():
    for mine in mines:
        x = -5 if random() < .5 else 5
        y = -5 if random() < .5 else 5
        settings.board.canvas.move(mine['id'], x, y)
        mine['pos'] = [mine['pos'][0] + x, mine['pos'][1] + y]
        # mine['pos'] = [x+y for x,y in zip(min['pos'], [x,y])]


print(__name__)

# setup GUI and canvas
settings.root = Tk()
settings.board = Board(settings.root)

times = 100  # inputs.NUMTICKS
gens = 1 # # of generations to evolve; 1 = no evolution

# initialize mines
for i in range(0, inputs.NUMMINES):
    x = round(random() * inputs.XSIZE)
    y = round(random() * inputs.YSIZE)
    settings.mines.append({'pos': [x, y], 'id': settings.board.place_object('mine', [x, y])})

population = Population()

last_update = time.time()
for k in range(0,gens):
    for l in range(0,times):
        # move sweepers to next positions
        for sweeper in population.sweepers:
            sweeper.move_sweeper()
            sweeper.handle_mines()
        # update label
        settings.board.label.configure(text="Tick: {} | Mines: {}".format(l+1, settings.num_mines_found))
        # wait for 1 / FPS seconds to pass
        delta = time.time() - last_update
        print("{}s elapsed.".format(delta))
        time.sleep(max(0,1/inputs.FPS - delta))
        # update board
        settings.board.update()

        last_update = time.time()

    # EVOLVE + UPDATE pop

    # RESET board + REDRAW


settings.root.mainloop()
