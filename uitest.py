from tkinter import *

top = Tk()

canvas = Canvas(top, bg="white", height=300, width=300)
canvas.create_rectangle(125,125,126,126, fill="black")
canvas.create_rectangle(100,100,105,105, fill="red", outline="red")
canvas.create_rectangle(150,150,155,155, fill="black")
canvas.create_rectangle(150,200,155,205, fill="black")
canvas.create_polygon(250,250,245,255,250,260,255,255, outline="black", fill="")
# canvas.create_polygon(50,50,48,52,50,54,52,52, outline="black", fill="white")
# canvas.create_polygon(49,51,51,49,53,51,51,53, outline="black", fill="")
# canvas.create_polygon(48,51,51,48,54,51,51,54, outline="green", fill="", width=1)
canvas.create_rectangle(48,48,54,54, outline="green", fill="", width=1)
canvas.create_rectangle(50,50,52,52, fill="red", outline="red")
data = [75,75,80,80, {'fill':'green', 'outline':'green'}]
data1 = [1,1,6,6, {'fill':'blue', 'outline':'blue'}]
data2 = [160,160,165,165, {'fill':'blue', 'outline':'blue'}]
data3 = [270,270,275,275, {'fill':'blue', 'outline':'blue'}]
canvas.create_rectangle(data)
canvas.create_rectangle(data1)
canvas.create_rectangle(data2)
canvas.create_rectangle(data3)
canvas.pack()

text = Text(top, height=1, width=50)
text.insert(INSERT, "A label")
text.pack()

top.mainloop()