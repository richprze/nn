from tkinter import *
from random import random
import math
import inputs
import time


root = Tk()
canvas = Canvas(root, bg="white", height=500, width=500)
canvas.pack()

left = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
right = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
scale = 100
fills = {0: "black",
         .1: "red", 
         .2: "green", 
         .3: "blue", 
         .4: "cyan",
         .5: "yellow", 
         .6: "magenta",
         .7: "black",
         .8: "red", 
         .9: "green", 
         1: "blue"}

for l in left:
    fill = fills[l]
    for r in right:
        length = (l+r)*scale
        angle = (l-r)*math.pi/2
        x = math.sin(angle) * length
        y = math.cos(angle) * length
        print("x: {}, y: {}".format(x,y))
        canvas.create_line(250,250,250-x, 250-y, fill="#D3D3D3")
        canvas.create_oval(250-x-2,250-y-2,250-x+2, 250-y+2, fill=fill, outline=fill)

canvas.update()

root.mainloop()
