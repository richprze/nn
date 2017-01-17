from tkinter import *
from random import random
from nn_classes import NeuralNet, Sweeper, Population
import inputs

class Board:
    def __init__(self):
        # setup GUI and canvas
        self.root = Tk()
        self.canvas = Canvas(self.root, bg="white", height=inputs.YSIZE, width=inputs.XSIZE)

        self.label = Label(self.root, text="Tick: 0")
        # self.text.insert(INSERT, "Tick: 0")
        self.label.pack()

        self.squares1 = []
        self.squares1.append(self.canvas.create_rectangle(50, 50, 52, 52, fill="red", outline="red"))
        self.squares1.append(self.canvas.create_rectangle(55, 55, 57, 57, fill="red", outline="red"))
        self.squares1.append(self.canvas.create_rectangle(60, 60, 62, 62, fill="red", outline="red"))
        self.squares2 = []
        self.squares2.append(self.canvas.create_rectangle(50, 100, 52, 102, fill="red", outline="red"))
        self.squares2.append(self.canvas.create_rectangle(55, 105, 57, 107, fill="red", outline="red"))
        self.squares2.append(self.canvas.create_rectangle(60, 110, 62, 112, fill="red", outline="red"))

        self.canvas.pack()
        self.times = 10 # inputs.NUMTICKS
        self.count = 0

        print("before first after call to animate")
        self.canvas.after(500, self.animate)
        self.root.mainloop()

    def animate(self):
        print("In animate")
        for square in self.squares1:
            self.canvas.move(square, 5, 5)
        for square in self.squares2:
            self.canvas.move(square, -5, 5)
        self.canvas.update()
        self.count += 1
        if self.count <= self.times:
            self.canvas.after(500, self.animate)

Board()
