import Cell
import random

class MinesweeperGame:
    def __init__(self, width, height, bomb_amount):
        self.width = width
        self.height = height
        self.bomb_amount = bomb_amount
        self.grid = self.initialize_grid()
        self.revealed_cells = 0 
        self.game_over=False
        self.win=False
        self.mines_left=bomb_amount
        self.turns=0

    def initialize_grid(self):
        grid = [[Cell.Cell() for _ in range(self.width)] for _ in range(self.height)]
        
        for _ in range(self.bomb_amount):
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if not grid[y][x].is_bomb:
                    grid[y][x].is_bomb = True
                    break
        
        for i in range(self.height):
            for j in range(self.width):
                if not grid[i][j].is_bomb:
                    grid[i][j].adjacent_bombs = self.count_bombs(grid, i, j)
        
        return grid

    def count_bombs(self, grid, x, y):
        count = 0
        coordinates = [(-1, -1), (0, -1), (1, -1),
                       (-1, 0), (1, 0),
                       (-1, 1), (0, 1), (1, 1)]
        for dx, dy in coordinates:
            nx = x + dx
            ny = y + dy
        
            if 0 <= nx < self.height and 0 <= ny < self.width:
                if grid[nx][ny].is_bomb:
                    count += 1
        return count
    
    def is_mine(self,x,y):
        return self.grid[x][y].is_bomb
    
