import tkinter as tk
from tkinter import messagebox
from functools import partial
import MinesweeperGame

BACKGROUND = "#171e28"
BACKGROUNDLIGHT ="#212a33"
BUTTON = "#f4af03"
CELL="#2f3640"
class MinesweeperUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        self.root.config(bg=BACKGROUND)
        self.create_start_menu()
        self.root.mainloop()

    def create_start_menu(self):
        self.clear_root()
        self.root.geometry("500x300")

        tk.Label(self.root,bg=BACKGROUND , fg="white", text="Grid Size:(Max 15)",font=("Arial", 14)).pack(pady=20)
        self.grid_size_entry = tk.Entry(self.root,bg=BACKGROUNDLIGHT,fg="white",font=("Arial", 14))
        self.grid_size_entry.pack(pady=2)

        tk.Label(self.root,bg=BACKGROUND, fg="white",text="Number of Mines:(Max Grid size * Grid size - 1)",font=("Arial", 14)).pack(pady=20)
        self.mine_count_entry = tk.Entry(self.root,bg=BACKGROUNDLIGHT,fg="white",font=("Arial", 14))
        self.mine_count_entry.pack(pady=2)

        tk.Button(self.root, text="Start Game", bg=BUTTON,command=self.start_game,font=("Arial", 14)).pack(pady=20)

    def start_game(self):
        try:
            side_length = int(self.grid_size_entry.get())
            bomb_amount = int(self.mine_count_entry.get())
            if side_length <= 0 or bomb_amount <= 0 or bomb_amount >= side_length * side_length or side_length > 15:
                raise ValueError("Invalid grid size or number of mines.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            return
        
        self.side_length = side_length
        self.bomb_amount = bomb_amount
        self.game = MinesweeperGame.MinesweeperGame(side_length, bomb_amount)
        self.create_game_board()

    def create_game_board(self):
        self.clear_root()
        self.buttons = []
        button_size = 30  
        for i in range(self.side_length):
            row_buttons = []
            for j in range(self.side_length):
                button = tk.Button(self.root,bg=CELL,text='', width=button_size // 10, height=button_size // 20, font=("Arial", 14), command=partial(self.click, i, j))
                button.grid(row=i, column=j, padx=1, pady=1)  
                button.bind('<Button-3>', partial(self.flag, x=i, y=j))
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        self.root.update_idletasks()  
        
        
        grid_width = self.root.winfo_reqwidth()
        grid_height = self.root.winfo_reqheight()

        self.root.geometry(f"{grid_width }x{grid_height }")

    def click(self, x, y):
        cell = self.game.grid[x][y]
        button = self.buttons[x][y]

        if cell.is_revealed:
            return

        if cell.is_bomb:
            button.config(text='💣', state='disabled', bg= "red")
            self.show_game_over()
        else:
            cell.is_revealed = True
            self.game.revealed_cells += 1
            button.config(text=str(cell.adjacent_bombs), state='disabled',bg = "white")
            if cell.adjacent_bombs == 0:
                self.reveal_empty(x, y)
            self.check_win()

    def flag(self, event, x, y):
        button = self.buttons[x][y]
        cell = self.game.grid[x][y]

        if cell.is_revealed:
            return

        if cell.is_flagged:
            cell.is_flagged = False
            button.config(text='', font=("Arial", 14),bg = CELL)
        else:
            cell.is_flagged = True
            button.config(text='🚩', font=("Arial", 14), bg = "#f4af03")

    def reveal_empty(self, x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                nx, ny = x + i, y + j
                if 0 <= nx < self.side_length and 0 <= ny < self.side_length:
                    if not self.game.grid[nx][ny].is_revealed:
                        self.click(nx, ny)

    def reveal_all_bombs(self):
        for i in range(self.side_length):
            for j in range(self.side_length):
                if self.game.grid[i][j].is_bomb:
                    self.buttons[i][j].config(text='💣', state='disabled')

    def check_win(self):
        if self.game.revealed_cells == (self.side_length * self.side_length) - self.bomb_amount:
            self.show_win_message()

    def show_game_over(self):
        self.reveal_all_bombs()
        response = messagebox.askquestion("Game Over", "Game Over! Do you want to play again?")
        if response == 'yes':
            self.create_start_menu()
        else:
            self.root.quit()

    def show_win_message(self):
        response = messagebox.askquestion("Congratulations!", "You have won the game! Do you want to play again?")
        if response == 'yes':
            self.create_start_menu()
        else:
            self.root.quit()

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    MinesweeperUI()
     