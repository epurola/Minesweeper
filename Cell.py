class Cell:
    def __init__(self, is_bomb=False):
        self.is_bomb = is_bomb
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_bombs = 0