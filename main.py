from tkinter import *
import tkinter.font as font
import pyglet
import os
from grid_generator import *

tiles = []
size_x = 9
size_y = 9

is_active = False
time = -1
mines_number = 10
frame3 = []

def is_win():
    global is_active, mines_number

    if not is_active:
        return

    points = 0
    tiles_used = 0

    for y in range(size_y):
        for x in range(size_x):
            if tiles[y][x]["state"] == "disabled":
                tiles_used += 1

            if tiles[y][x]["image"] != "" and tiles[y][x]["state"] == "disabled" and grid[y][x] == -1:
                points += 1
            elif tiles[y][x]["image"] != "" and tiles[y][x]["state"] == "disabled":
                points -= 1
    
    if points == mines_number and tiles_used == size_y * size_x:
        is_active = False
        new_game_btn.config(image = cool_python_img)
        for y in range(size_y):
            for x in range(size_x):
                tiles[y][x].config(state = "disabled")

def you_lost():
    global is_active, mines_number

    is_active = False
    new_game_btn.config(image = dead_python_img)
    for y in range(size_y):
        for x in range(size_x):
            if grid[y][x] == -1 and tiles[y][x]["image"] == "":
                tiles[y][x].config(relief=FLAT, image=mine_img, height = 20, width = 18)
            elif grid[y][x] > -1 and tiles[y][x]["image"] != "":
                tiles[y][x].config(relief=RAISED, image=flag_without_bomb_img, height = 20, width = 18)
            tiles[y][x].config(state = "disabled")

def flags_num():
    flags = 0
    
    if len(tiles) <= 0:
        return mines_number

    for y in range(size_y):
        for x in range(size_x):
            if tiles[y][x]["image"] != "" and tiles[y][x]["state"] == "disabled":
                flags += 1

    
    return mines_number - flags

def add_flag(y, x):
    if tiles[y][x]["image"] == "" and tiles[y][x]["state"] != "disabled" and is_active and flags_num() <= 999:
        tiles[y][x].config(image = flag_img, state="disabled", height = 20, width = 18)
    elif tiles[y][x]["text"] == "" and is_active:
        tiles[y][x].config(image = "", state="normal", height = 1, width = 2)

    flags_left_label.config(text=flags_num())

def check_tile(row_number, button_number):
    global is_active, grid, tiles, size_x, size_y
    color = "white"

    text = StringVar()
    text.set(str(grid[row_number][button_number]))


    if text == "1":
        color = "#21607F"
    elif text == "2":
        color = "#467C41"
    elif text == "3":
        color = "#E04D39"
    elif text == "4":
        color = "#733333"
    elif text == "5":
        color = "#390000"

    if not is_active:
        is_active = True
        timer()

    if grid[row_number][button_number] == -1 and tiles[row_number][button_number]["image"] == "":
        you_lost()
    elif grid[row_number][button_number] != 0 and tiles[row_number][button_number]["image"] == "":
        tiles[row_number][button_number].config(relief=FLAT, state="disabled", fg = color, font = ("Courier", 8, "bold"),
                                                text="", textvariable=text)
    elif tiles[row_number][button_number]["image"] == "":
        tiles[row_number][button_number].config(relief=FLAT, state="disabled", text=" ")
        for y in range(row_number - 1, row_number + 2):
            for x in range(button_number - 1, button_number + 2):
                if y >= 0 and x >= 0 and x <= size_x - 1 and y <= size_y - 1:
                    if tiles[y][x]["text"] != " ":
                        check_tile(y, x)    

def timer():
    global time, is_active
    if time == 999:
        you_lost

    is_win()
    time += 1
    timer_label.config(text=time)
    if is_active:
        root.after(1000, timer)

def on_hover(event):
    global is_active

    if is_active:
        new_game_btn.config(image = surprised_python_img)

def on_leave(event):
    global is_active

    if is_active:
        new_game_btn.config(image = python_img)

def new_game(btn):
    global grid, tiles, size_y, size_x, mines_number, frame3, is_active, time
    grid = generate(size_y, size_x, mines_number)
    is_active = False
    time = -1
    print(grid)

    if btn:
        new_game_btn.config(image = python_img)
        for i in range(size_y):
            for j in range(size_x):
                tiles[i][j].config(image = "", height = 1, width = 2, cursor="hand2",
                                relief=RAISED, state="normal", text = "", textvariable="",
                                command=lambda y = i, x = j: check_tile(y, x))
                tiles[i][j].config(borderwidth=5)
    else:
        for i in range(size_y):
            tiles.append([])
            frame3.append(Frame(frame2))
            frame3[i].pack(side=TOP, fill=X)
            for j in range(size_x):
                tiles[i].append(Button(frame3[i], image = "", height = 1, width = 2, cursor="hand2",
                                    command=lambda y = i, x = j: check_tile(y, x)))
                tiles[i][j].config(borderwidth=5)
                tiles[i][j].pack(side=LEFT, anchor=W)
                tiles[i][j].bind("<Button-3>", lambda event, y = i, x = j: add_flag(y, x))
                tiles[i][j].bind("<Enter>", on_hover)
                tiles[i][j].bind("<Leave>", on_leave)

def set_lvl(new_size_x, new_size_y, new_mines_number):
    global size_x, size_y, mines_number, frame3, tiles
    
    for i in range(size_y):
        frame3[i].destroy()
    frame3 = []
    tiles = []

    size_x = new_size_x
    size_y = new_size_y
    mines_number = new_mines_number

    new_game(False)

root = Tk()
root.title("Another Minesweeper Clone")
root.iconbitmap("resources/favicon.ico")
root.resizable(False, False)

pyglet.font.add_file('resources/digital-7.ttf')
flag_img = PhotoImage(file = "resources/flag.png")
flag_without_bomb_img = PhotoImage(file = "resources/flag_without_bomb.png")
mine_img = PhotoImage(file = "resources/mine.png")
normal_python_img = PhotoImage(file = "resources/zywywonsz.png")
python_img = normal_python_img.subsample(2, 2)
cool_python_img = PhotoImage(file = "resources/szczesliwywonsz.png")
cool_python_img = cool_python_img.subsample(2, 2)
dead_python_img = PhotoImage(file = "resources/martwywonsz.png")
dead_python_img = dead_python_img.subsample(2, 2)
surprised_python_img = PhotoImage(file = "resources/zdziwionywonsz.png")
surprised_python_img = surprised_python_img.subsample(2, 2)

menubar = Menu(root)

frame1=Frame(root)
frame1.config(relief=SUNKEN, borderwidth=10, padx=10, pady=5)
frame1.pack(side=TOP, fill=X)

frame2=Frame(root)
frame2.config(relief=SUNKEN, borderwidth=10)
frame2.pack(side=TOP, fill=X)

settingsmenu = Menu(menubar, tearoff=0)
settingsmenu.add_command(label="Beginner", command=lambda: set_lvl(9, 9, 10))
settingsmenu.add_command(label="Advanced", command=lambda: set_lvl(16, 16, 40))
settingsmenu.add_command(label="Master", command=lambda: set_lvl(30, 16, 99))
settingsmenu.add_separator()
settingsmenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Game", menu=settingsmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=print(""))
helpmenu.add_command(label="About", command=print(""))
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

flags_left_label = Label(frame1, width=3, height=1, font=("digital-7", 38), text=str(flags_num()), bg="black", fg="red")
flags_left_label.pack(side=LEFT)

timer_label = Label(frame1, width=3, height=1, font=("digital-7", 38), text="000", bg="black", fg="red")
timer_label.pack(side=RIGHT)

new_game_btn = Button(frame1, image=python_img, cursor="hand2", command=lambda: new_game(True))
new_game_btn.config(borderwidth=7)
new_game_btn.pack(side=TOP)

new_game(False)
root.mainloop()
