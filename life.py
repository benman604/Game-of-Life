from tkinter import *
import math
import webbrowser
import random
size = 600
speed = 250
currentcount = 0
playing = False
top = Tk()
top.geometry("460x500")
box = PhotoImage("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")
cells = []
activeColor = "gray"
inactiveColor = "white"

class Grid(Frame):  # Create grid of cells
    def __init__(self, root):
        Frame.__init__(self, root)
        for row in range(round(math.sqrt(size))):
            cells.append([])
            for column in range(round(math.sqrt(size))):
                item = Button(self, text="", image=box, height=15, width=15, borderwidth=0, bg='white', activebackground='white')
                item.grid(row=row, column=column, padx=1, pady=1)
                cells[len(cells)-1].append(item)
                item.configure(command=lambda x=[row, column]: self.gridItemClick(x[0], x[1]))
        nextIttr()

    def gridItemClick(self, x, y):  # Toggle button state on clicked
        print(x, y)
        if isAlive(cells[x][y]):
            cells[x][y].configure(bg=inactiveColor)
            cells[x][y].configure(activebackground=inactiveColor)
        else:
            cells[x][y].configure(bg=activeColor)
            cells[x][y].configure(activebackground=activeColor)


class Controls(Frame):
    def __init__(self, root):
        global currentcount
        Frame.__init__(self, root)

        self.state = StringVar()
        self.state.set("Play")
        self.play = Button(self, textvariable=self.state, borderwidth=0, bg=inactiveColor, fg="black", command=self.playClick).grid(row=0, column=0)

        self.count = StringVar()
        self.count.set("0")
        self.counter = Button(self, textvariable=self.count, borderwidth=0, fg="black").grid(row=0, column=1)

        Button(self, text="Clear", borderwidth=0, bg=inactiveColor, fg="black", command=self.resetClick).grid(row=0, column=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def playClick(self):
        global playing
        global play
        playing = not playing
        if playing:
            nextIttr()
            self.state.set("Pause")
        else:
            self.state.set("Play")

    def resetClick(self):
        global playing
        global currentcount
        currentcount = 0
        for row in cells:
            for item in row:
                item.configure(bg=inactiveColor)
                item.configure(activebackground=inactiveColor)
        playing = False
        self.state.set("Play")

controls = Controls(top)

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
        item.configure(bg=inactiveColor)
        item.configure(activebackground=inactiveColor)
    for item in birthIntents:
        item.configure(bg=activeColor)
        item.configure(activebackground=activeColor)

    global currentcount
    global controls
    currentcount += 1
    controls.count.set(str(currentcount))

    if playing:
        top.after(speed, nextIttr)

def isAlive(cell):  # Returns current state of cell
    if cell.cget("bg") == inactiveColor:
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
controls.pack(side="bottom", fill="x", expand=True)

def setspeed(newspeed):
    global speed
    speed = newspeed
def showAbout():
    webbrowser.open("https://github.com/benman604/Game-of-Life", new=1)
def fillRandom():
    global playing
    global currentcount
    playing = False
    for row in cells:
        for cell in row:
            r = random.randint(0, 1)
            if r == 0:
                cell.configure(bg=inactiveColor)
                cell.configure(activebackground=inactiveColor)
            else:
                cell.configure(bg=activeColor)
                cell.configure(activebackground=activeColor)
                controls.state.set("Play")
                currentcount = 0

menu = Menu(top)

speedmenu = Menu(menu, tearoff=0)
speedmenu.add_command(label="0.25", command=lambda: setspeed(1000))
speedmenu.add_command(label="0.5", command=lambda: setspeed(750))
speedmenu.add_command(label="1", command=lambda: setspeed(500))
speedmenu.add_command(label="1.25", command=lambda: setspeed(250))
speedmenu.add_command(label="1.75", command=lambda: setspeed(100))
speedmenu.add_command(label="2", command=lambda: setspeed(50))
menu.add_cascade(label="Speed", menu=speedmenu)
menu.add_command(label="Fill Random", command=fillRandom)
menu.add_command(label="About", command=showAbout)

icon = PhotoImage(file="icon.png")
top.iconphoto(False, icon)

top.config(menu=menu)
top.title('Game of Life')
top.mainloop()
