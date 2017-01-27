from tkinter import *
from random import random
from nn_classes import Population, Sweeper, obj_tuple
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

    def create_mines(self):
        settings.mines = []
        for i in range(0, inputs.NUMMINES):
            x = round(random() * inputs.XSIZE)
            y = round(random() * inputs.YSIZE)
            settings.mines.append({'pos': [x, y], 'id': self.place_object('mine', [x, y])})

    def reset(self):
        self.canvas.delete('all')
        self.canvas.update()



print(__name__)

# setup GUI and canvas
settings.root = Tk()
settings.board = Board(settings.root)

times = 200  # inputs.NUMTICKS
gens = 20 # # of generations to evolve; 1 = no evolution

settings.board.create_mines()

population = Population()

print(population.sweepers[0].brain.get_num_weights())
weights = population.sweepers[0].brain.get_weights()
print(weights)
weights[0] = weights[1]
population.sweepers[0].brain.update_weights(weights)
print(population.sweepers[0].brain.get_weights())

last_update = time.time()
for k in range(0,gens):
    print("Starting generation: {}".format(population.generation))
    for l in range(0,times):
        # move sweepers to next positions
        for sweeper in population.sweepers:
            sweeper.move_sweeper()
            sweeper.handle_mines()
        # update fitness and label
        population.total_fitness = settings.num_mines_found
        settings.board.label.configure(text="Tick: {} | Mines: {}".format(l+1, settings.num_mines_found))
        # wait for 1 / FPS seconds to pass
        delta = time.time() - last_update
        time.sleep(max(0,1/inputs.FPS - delta))
        # update board
        settings.board.update()

        last_update = time.time()

    # EVOLVE + UPDATE pop
    population.evolve()

    population.reset()
    settings.board.reset()
    time.sleep(2)
    settings.board.create_mines()

    # place new sweepers
    for sweeper in population.sweepers:
        sweeper.place()

    print(population.sweepers)

    settings.board.update()

    for stat in settings.stats:
        print(stat)


settings.root.mainloop()
