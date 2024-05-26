from datetime import date,datetime
import customtkinter as ctk
from tkinter import  messagebox
from functools import partial
import MinesweeperGame
from game_database import GameDatabase

BACKGROUND = "#171e28"  # Darkblue
BACKGROUNDLIGHT = "#212a33"  # Gray/blue
BUTTON = "#f4af03"  # Yellowish
CELL = "#2f3640"  # Darkblue

class MinesweeperUI:

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        ctk.deactivate_automatic_dpi_awareness()
        self.root = ctk.CTk()
        self.root.title("\U0001F4A3 Minesweeper")
        self.root.config(bg=BACKGROUND)
        self.game_records = []  # List to store game records
        self.db = GameDatabase()
        self.create_start_menu()
        self.root.mainloop()
        
    def create_start_menu(self):
        self.clear_root()
        
        self.root.geometry("500x400")
        ctk.CTkLabel(master=self.root, bg_color=BACKGROUND, text="Traditional Game 16x30", text_color="white", font=("Arial", 20)).pack(pady=30)

        ctk.CTkButton(self.root, text="Start Game", fg_color=BUTTON, text_color="black", command=self.start_original_game, font=("Arial", 14)).pack()
        ctk.CTkButton(self.root, text="Custom Game", fg_color=BUTTON, text_color="black", command=self.launch_custom_game_settings, font=("Arial", 14)).pack(pady=50)
        ctk.CTkButton(self.root, text="Game Records", fg_color=BUTTON, text_color="black", command=self.show_game_records, font=("Arial", 14)).pack(pady=10)
        
    def update_mine_count_max(self):
        width = int(self.grid_width_entry.get())
        height = int(self.grid_height_entry.get())
        max_mines = width * height -1
        self.mine_count_entry.configure(to=max_mines, number_of_steps=max_mines - 1)
        self.mine_count_entry.set(max_mines)
        self.update_grid_mines_label(self.mine_count_entry.get()) 
          
    def update_grid_width_label(self,value):
        self.my_label.configure(text=str(int(value)))
        #Dynamically updates the max minecount label
        self.update_mine_count_max()
        mines = self.mine_count_entry.get()
        self.mine_count_entry.set(mines)
        self.update_grid_mines_label(mines)
     
    def update_grid_mines_label(self,value):
        self.my_label_mines.configure(text=str(int(value)))
     
    def update_grid_height_label(self,value):
        int(value)
        self.height.configure(text=str(int(value)))
        #Dynamically updates the max minecount label
        self.update_mine_count_max()
        mines = self.mine_count_entry.get()
        self.mine_count_entry.set(mines)
        self.update_grid_mines_label(mines)
     
        
    def launch_custom_game_settings(self):
        self.clear_root()
        settings_frame = ctk.CTkFrame(master=self.root, fg_color=BACKGROUNDLIGHT)
        settings_frame.pack(pady=20, padx=20, fill="both", expand=True)
        # Grid width slider
        self.grid_width_entry = ctk.CTkSlider(master=settings_frame, from_=2, to=30, number_of_steps=29, bg_color=BACKGROUNDLIGHT, command = self.update_grid_width_label)
        self.my_label = ctk.CTkLabel(master=settings_frame, text="Width"  , text_color="white", font=("Arial", 14))
        self.my_label.place(x=10,y=10)
        self.my_label.pack(pady=10)
        self.grid_width_entry.pack(pady=2)
        self.grid_width_entry.set(10)
        # Grid height slider
        self.grid_height_entry = ctk.CTkSlider(master=settings_frame, from_=2, to=23, number_of_steps=22, bg_color=BACKGROUNDLIGHT,command= self.update_grid_height_label)
        self.height=ctk.CTkLabel(master=settings_frame,  text="Height", text_color="white", font=("Arial", 14))
        self.height.pack(pady=10)
        self.grid_height_entry.pack(pady=2)
        self.grid_height_entry.set(10)
        # Number of mines slider
        self.mine_count_entry = ctk.CTkSlider(master=settings_frame, from_=1, to=400, number_of_steps=399, bg_color=BACKGROUNDLIGHT,command = self.update_grid_mines_label)
        self.my_label_mines=ctk.CTkLabel(master=settings_frame,  text="Mines", text_color="white", font=("Arial", 14))
        self.my_label_mines.pack(pady=10)
        self.mine_count_entry.pack(pady=2)
        self.mine_count_entry.set(40)
        # Button to start the custom game
        ctk.CTkButton(master=settings_frame, text="Start Custom Game", fg_color=BUTTON, text_color="black", command=self.start_game, font=("Arial", 14)).pack(pady=10)
        # Back button to return to the main menu
        self.back = ctk.CTkButton(master=settings_frame, text="Back", text_color="white", command=self.create_start_menu, font=("Arial", 14))
        self.back.pack(pady=10)


    def start_game(self):
        try:
            width = int(self.grid_width_entry.get())
            height = int(self.grid_height_entry.get())
            bomb_amount = int(self.mine_count_entry.get())
            if width <= 0 or height <= 0 or bomb_amount <= 0 or bomb_amount >= width * height or width > 30 or height > 30:
                raise ValueError("Invalid grid size or number of mines.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            return

        self.width = width
        self.height = height
        self.bomb_amount = bomb_amount
        self.game = MinesweeperGame.MinesweeperGame(width, height, bomb_amount)
        self.create_game_board()
        
    def start_original_game(self):
        self.width = 30
        self.height = 16
        bomb_amount = 99
        self.bomb_amount = bomb_amount
        self.game = MinesweeperGame.MinesweeperGame(self.width, self.height, bomb_amount)
        self.create_original_game_board()
        
    def create_original_game_board(self):
     self.clear_root()
    
     game_frame = ctk.CTkFrame(master=self.root, fg_color=BACKGROUNDLIGHT)
     game_frame.grid(row=0, column=0, padx=20, pady=20)
    
     self.buttons = []
     button_size = 30
    
     self.root.grid_rowconfigure(0, weight=1)
     self.root.grid_columnconfigure(0, weight=1)

    # Create the button elements on the board
     for i in range(self.height):
         row_buttons = []
         for j in range(self.width):
            button = ctk.CTkButton(master=game_frame, fg_color=CELL, text='', width=button_size, height=button_size, font=("Arial", 14), command=partial(self.click, i, j))
            button.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")
            button.bind('<Button-3>', partial(self.flag, x=i, y=j))
            row_buttons.append(button)
         self.buttons.append(row_buttons)

     self.root.update_idletasks()

     grid_width = self.width * (button_size + 2)
     grid_height = self.height * (button_size + 2)
     self.timer_label = ctk.CTkLabel(master=self.root, text="Time: 00:00:00", text_color="white", font=("Arial", 14), bg_color=BACKGROUNDLIGHT)
     self.timer_label.grid(row=1, column=0, padx=2, pady=2)
     self.root.geometry(f"{int(grid_width + 40)}x{int(grid_height + 80)}")
    
     self.start_time = datetime.now()
     self.update_timer()


    def create_game_board(self):
        self.clear_root()
        game_frame = ctk.CTkFrame(master=self.root, fg_color=BACKGROUNDLIGHT)
        game_frame.grid(row=0, column=0, padx=20, pady=20)
        
        self.buttons = []
        if self.grid_height_entry.get() < 15 and self.grid_width_entry.get() < 15:
         button_size = 500 / self.grid_height_entry.get()
        else:
            button_size = 30
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        for i in range(int(self.grid_height_entry.get())):
            self.row_buttons = []
            for j in range(int(self.grid_width_entry.get())):
                button = ctk.CTkButton(master=game_frame, fg_color=CELL, text='', width=button_size, height=button_size, font=("Arial", 14), command=partial(self.click, i, j))
                button.grid(row=i, column=j, padx=1, pady=1)
                button.bind('<Button-3>', partial(self.flag, x=i, y=j))
                self.row_buttons.append(button)
            self.buttons.append(self.row_buttons)
        self.root.update_idletasks()

        grid_width = self.grid_width_entry.get()* (button_size +20)
        grid_height = self.grid_height_entry.get() * (button_size +2)
        self.timer_label = ctk.CTkLabel(master=self.root, text="Time: 00:00:00",text_color="white", font=("Arial", 14), bg_color=BACKGROUNDLIGHT)
        self.timer_label.grid(row=0, column=1,padx=2, pady=2)
        self.root.geometry(f"{int(grid_width)}x{int(grid_height)}")
        
        self.start_time = datetime.now()
        self.update_timer()

        
    def update_timer(self):
     if self.game.game_over:
        return

     now = datetime.now()
     elapsed_time = now - self.start_time
     self.formatted_time = str(elapsed_time).split('.')[0]  
     self.timer_label.configure(text=f"Time: {self.formatted_time}")
     self.timer_label.after(1000, self.update_timer)


    def click(self, x, y):
        cell = self.game.grid[x][y]
        button = self.buttons[x][y]

        if cell.is_revealed:
            return
        if cell.is_flagged:
            return
        if cell.is_bomb:
            button.configure(text='💣', state='disabled', fg_color="red")
            self.show_game_over()
            self.game_over()
        else:
            cell.is_revealed = True
            self.game.revealed_cells += 1
            button.configure(text=str(cell.adjacent_bombs), state='disabled', fg_color="white")
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
        button.configure(text='', font=("Arial", 14), fg_color=CELL)
        if self.game.is_mine(x, y):
            self.game.mines_left += 1  
     else:
        cell.is_flagged = True
        button.configure(text='', font=("Arial", 14), fg_color=BUTTON)
        if self.game.is_mine(x, y):
           self.game.mines_left -= 1  


    def reveal_empty(self, x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                nx, ny = x + i, y + j
                if 0 <= nx < self.height and 0 <= ny < self.width:
                    if not self.game.grid[nx][ny].is_revealed:
                        self.click(nx, ny)

    def reveal_all_bombs(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.game.grid[i][j].is_bomb:
                    self.buttons[i][j].configure(text='💣', state='disabled')
                    self.game.game_over=True

    def check_win(self):
        if self.game.revealed_cells == (self.width * self.height) - self.bomb_amount:
            self.show_win_message()
            self.game.win = True
            if not self.game.game_over:
             self.game_over()

    def show_game_over(self):
        self.reveal_all_bombs()
        self.clear_root()
    
        win_frame = ctk.CTkFrame(master=self.root, fg_color=BACKGROUND)
        win_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
        elapsed_time = datetime.now() - self.start_time
        formatted_time = str(elapsed_time).split('.')[0]
        
        ctk.CTkLabel(master=win_frame, bg_color=BACKGROUND, text="Game Over!", text_color="white", font=("Arial", 16)).pack(pady=10)
        ctk.CTkLabel(master=win_frame, bg_color=BACKGROUND, text=f"Time wasted {formatted_time}.", text_color="white", font=("Arial", 14)).pack(pady=10)
    
        ctk.CTkButton(master=win_frame, text="Play Again", fg_color=BUTTON, text_color="black", command=self.create_start_menu, font=("Arial", 14)).pack(pady=10)
        ctk.CTkButton(master=win_frame, text="Quit", fg_color=BUTTON, text_color="black", command=self.root.quit, font=("Arial", 14)).pack(pady=10)

    def show_win_message(self):
        self.clear_root()
        win_frame = ctk.CTkFrame(master=self.root, fg_color=BACKGROUND,)
        win_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
        elapsed_time = datetime.now() - self.start_time
        formatted_time = str(elapsed_time).split('.')[0]

        ctk.CTkLabel(master=win_frame, bg_color=BACKGROUND, text="Congratulations!", text_color="white", font=("Arial", 16)).pack(pady=10)
        ctk.CTkLabel(master=win_frame, bg_color=BACKGROUND, text=f"You have won the game in {formatted_time}.", text_color="white", font=("Arial", 14)).pack(pady=10)
    
        ctk.CTkButton(master=win_frame, text="Play Again", fg_color=BUTTON, text_color="black", command=self.create_start_menu, font=("Arial", 14)).pack(pady=10)
        ctk.CTkButton(master=win_frame, text="Quit", fg_color=BUTTON, text_color="black", command=self.root.quit, font=("Arial", 14)).pack(pady=10)


    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def game_over(self):
        self.game.game_over=True
        duration=self.formatted_time
        outcome = "Win" if self.game.win else "Loss"
        mines_left = self.game.mines_left
        self.db.add_record(duration ,outcome, mines_left)
        
    def show_game_records(self):
     self.clear_root()

     records_frame = ctk.CTkScrollableFrame(self.root, fg_color=BACKGROUNDLIGHT)
     records_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    
     best_time_frame = ctk.CTkFrame(self.root, fg_color=BACKGROUND)
     best_time_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

     records = self.db.get_all_records()

     if not records:
        ctk.CTkLabel(records_frame, text="No records found", text_color="white", font=("Arial", 14)).pack(pady=10)
     else:
        for record in records:
            record_id, date, time_of_day, duration, outcome, mines_left = record
            formatted_record = f"\nGAME: {record_id}\n Date: {date}\n Time: {time_of_day}\n Duration: {duration}\n Outcome: {outcome}\n Mines Left: {mines_left}"
            ctk.CTkLabel(records_frame, text=formatted_record, text_color="white", font=("Arial", 12), anchor="center").pack(pady=1)

    # Display the best time on the left side
     best_time = self.db.get_best_time()
     wins = self.db.get_win_amount()
     loss =self.db.get_loss_amount()
     games= self.db.get_matches_amount()
     winrate = self.db.get_win_rate()
     time_wasted = self.db.get_time_wasted()
     if best_time:
        ctk.CTkLabel(best_time_frame, text=f"Best Time: {best_time}", text_color="white", font=("Arial", 14)).pack(pady=10)
        ctk.CTkLabel(best_time_frame, text=f"Games Played: {games}", text_color="white", font=("Arial", 14)).pack(pady=10)
        ctk.CTkLabel(best_time_frame, text=f"Wins: {wins}", text_color="white", font=("Arial", 14)).pack(pady=10)
        ctk.CTkLabel(best_time_frame, text=f"Losses: {loss}", text_color="white", font=("Arial", 14)).pack(pady=10)
        ctk.CTkLabel(best_time_frame, text=f"Win rate: {winrate} %", text_color="white", font=("Arial", 14)).pack(pady=10)
        ctk.CTkLabel(best_time_frame, text=f"Time Wasted: {time_wasted}", text_color="white", font=("Arial", 14)).pack(pady=10)
        

    # Add back button at the bottom
     ctk.CTkButton(self.root, text="Back", text_color="white", command=self.create_start_menu, font=("Arial", 14)).grid(row=1, column=0, columnspan=2, pady=10, sticky="s")
           
   


if __name__ == "__main__":
    MinesweeperUI()


     