from tkinter import *
import tkinter as tk
import math
import time

size = 600
speed = 250
playing = True
top = tk.Tk()
top.title = "Placeholder"
box = tk.PhotoImage("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")
cells = []

class Grid(Frame):  # Create grid of cells
    def __init__(self, root):
        Frame.__init__(self, root)
        for row in range(round(math.sqrt(size))):
            cells.append([])
            for column in range(round(math.sqrt(size))):
                item = tk.Button(self, text="", image=box, height=15, width=15, borderwidth=0, bg='white', activebackground='white')
                item.grid(row=row, column=column)
                cells[len(cells)-1].append(item)
                item.configure(command=lambda x=[row, column]: self.gridItemClick(x[0], x[1]))
        nextIttr()

    def gridItemClick(self, x, y):  # Toggle button state on clicked
        print(x, y)
        if isAlive(cells[x][y]):
            cells[x][y].configure(bg="white")
            cells[x][y].configure(activebackground="white")
        else:
            cells[x][y].configure(bg="gray")
            cells[x][y].configure(activebackground="gray")


class Controls(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        play = tk.Button(self, text="Play", borderwidth=0, bg="white", fg="black", command=self.playClick).grid(row=0, column=0)
        pause = tk.Button(self, text="Pause", borderwidth=0, bg="white", fg="black", command=self.pauseClick).grid(row=0, column=1)
        reset = tk.Button(self, text="Reset", borderwidth=0, bg="white", fg="black", command=self.resetClick).grid(row=0, column=2)

    def playClick(self):
        global playing
        playing = True
        nextIttr()
    def pauseClick(self):
        global playing
        playing = False
    def resetClick(self):
        global playing
        for row in cells:
            for item in row:
                item.configure(bg="white")
                item.configure(activebackground="white")
        playing = False


def nextIttr():  # Called once per iteration
    deathIntents = []
    birthIntents = []
    for row in cells:
        for item in row:
            neighbors = checkNeighbors(cells.index(row), row.index(item))
            if isAlive(item):  # Adds living cells to kill list
                if neighbors < 2 or neighbors > 3:
                    deathIntents.append(item)
            else:
                if neighbors == 3:  # Adds dead cells to birth list
                    birthIntents.append(item)

    for item in deathIntents:
        item.configure(bg="white")
        item.configure(activebackground="white")
    for item in birthIntents:
        item.configure(bg="gray")
        item.configure(activebackground="gray")

    if playing:
        top.after(speed, nextIttr)

def isAlive(cell):  # Returns current state of cell
    if cell.cget("bg") == "white":
        return False
    else:
        return True

def checkNeighbors(x, y):  # Returns number of living cells surrounding x, y
    count = 0
    possibilities = [
        [0, 1],
        [0, -1],
        [1, 0],
        [1, 1],
        [1, -1],
        [-1, 0],
        [-1, 1],
        [-1, -1]
    ]
    for i in possibilities:
        try:
            if isAlive(cells[x+i[0]][y+i[1]]):
                count += 1
        except IndexError:
            count = 0

    return count

grid = Grid(top)
grid.pack(side="top", fill="both")
controls = Controls(top)
controls.pack(side="bottom", fill="x", expand=True)
tk.call('wm', 'Iconphoto', top._w, tk.PhotoImage('icon.png'))
top.mainloop()
