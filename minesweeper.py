import tkinter as tk
from tkinter import messagebox
from functools import partial
import random

def count_bombs(grid, x, y):
    size = len(grid)
    count = 0
    coordinates = [(-1, -1), (0, -1), (1, -1),
                   (-1, 0), (1, 0),
                   (-1, 1), (0, 1), (1, 1)]
    for dx, dy in coordinates:
        nx = x + dx
        ny = y + dy
    
        if 0 <= nx < size and 0 <= ny < size:
            if grid[nx][ny] == '*':
                count += 1
    return count

def initialize_grid(side_length, bomb_amount):
    grid = []
    for _ in range(side_length):
        row = ['_'] * side_length
        grid.append(row)
    
    for _ in range(bomb_amount):
        while True:
            x = random.randint(0, side_length - 1)
            y = random.randint(0, side_length - 1)
            if grid[x][y] != '*':
                grid[x][y] = '*'
                break
        
    for i in range(side_length):
        for j in range(side_length):
            if grid[i][j] != '*':
                grid[i][j] = str(count_bombs(grid, i, j))
    
    return grid

def click(x, y):
    value = grid[x][y]
    button = buttons[x][y]
    if value == '*':
        button.config(text='💣', state='disabled')
        messagebox.showinfo("Virus.exe started successfully", "Game Over!")
        for row in buttons:
            for btn in row:
                btn.config(state='disabled')
    else:
        button.config(text=value, state='disabled')
        if value == '0':
            reveal_empty(x, y)

def flag(event, x, y):
    button = buttons[x][y]
    if button['text'] == '🚩':
        button.config(text='', font=large_font)
    else:
        button.config(text='🚩', font=large_font)

def reveal_empty(x, y):
    for i in range(-1, 2):
        for j in range(-1, 2):
            nx, ny = x + i, y + j
            if 0 <= nx < side_length and 0 <= ny < side_length and buttons[nx][ny]['state'] == 'normal':
                click(nx, ny)

# Initialize the grid
side_length = 10
bomb_amount = 10
grid = initialize_grid(side_length, bomb_amount)

# Create GUI
root = tk.Tk()
root.title("Minesweeper")

# Define larger font
large_font = ("Arial", 20)

buttons = []
for i in range(side_length):
    row_buttons = []
    for j in range(side_length):
        button = tk.Button(root, text='', width=4, height=2, font=large_font, command=partial(click, i, j))
        button.grid(row=i, column=j)
        button.bind('<Button-3>', partial(flag, x=i, y=j))  # Bind right-click to flag
        row_buttons.append(button)
    buttons.append(row_buttons)

root.mainloop()


     
         