import Cell
import random
class MinesweeperGame:
    def __init__(self, side_length, bomb_amount):
        self.side_length = side_length
        self.bomb_amount = bomb_amount
        self.grid = self.initialize_grid()
        self.revealed_cells = 0  

    def initialize_grid(self):
        grid = [[Cell.Cell() for _ in range(self.side_length)] for _ in range(self.side_length)]
        
        for _ in range(self.bomb_amount):
            while True:
                x = random.randint(0, self.side_length - 1)
                y = random.randint(0, self.side_length - 1)
                if not grid[x][y].is_bomb:
                    grid[x][y].is_bomb = True
                    break
        
        for i in range(self.side_length):
            for j in range(self.side_length):
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
        
            if 0 <= nx < self.side_length and 0 <= ny < self.side_length:
                if grid[nx][ny].is_bomb:
                    count += 1
        return count