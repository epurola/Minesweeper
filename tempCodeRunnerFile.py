def update_grid_width_label(self,value):
    
     self.my_label.configure(text=str(value))
        
    def launch_custom_game_settings(self):
        self.clear_root()
        
        settings_frame = ctk.CTkFrame(master=self.root, bg_color=BACKGROUND)
        settings_frame.pack(pady=20, padx=20, fill="both", expand=True)
        # Grid width slider)
        self.grid_width_entry = ctk.CTkSlider(master=settings_frame, from_=1, to=30, number_of_steps=29, bg_color=BACKGROUNDLIGHT, command = self.update_grid_width_label)
        self.my_label = ctk.CTkLabel(master=settings_frame, text=self.grid_width_entry.get()  , text_color="white", font=("Arial", 14)).pack(pady=10)
        self.grid_width_entry.pack(pady=2)
        self.grid_width_entry.set(10)