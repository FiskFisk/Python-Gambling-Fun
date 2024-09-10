import tkinter as tk
import random

class MinesGame:
    def __init__(self, root, money, return_to_menu):
        self.root = root
        self.root.title("Mines Game")

        # Set window to fullscreen but windowed
        self.root.attributes('-fullscreen', True)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.quit_fullscreen)

        self.money = money
        self.return_to_menu = return_to_menu

        # Set background color and fonts
        self.bg_color = "#2E8B57"  # Medium sea green
        self.accent_color = "#FFD700"  # Gold
        self.text_color = "#FFFFFF"  # White
        self.title_font = ("Arial", 24, "bold")
        self.label_font = ("Arial", 16)
        self.button_font = ("Arial", 14)

        self.root.configure(bg=self.bg_color)

        # Game title
        self.title_label = tk.Label(root, text="Welcome to the Mines Game!", font=self.title_font, bg=self.bg_color, fg=self.accent_color)
        self.title_label.pack(pady=20)

        # Display current money
        self.money_label = tk.Label(root, text=f"Current Balance: ${self.money}", font=self.label_font, bg=self.bg_color, fg=self.accent_color)
        self.money_label.pack(pady=10)

        # Bet input
        self.bet_frame = tk.Frame(root, bg=self.bg_color)
        self.bet_frame.pack(pady=10)

        tk.Label(self.bet_frame, text="Enter your bet amount:", font=self.label_font, bg=self.bg_color, fg=self.text_color).grid(row=0, column=0, padx=10)
        self.bet_amount_input = tk.Entry(self.bet_frame)
        self.bet_amount_input.grid(row=0, column=1, padx=10)

        # Mines input
        tk.Label(self.bet_frame, text="Enter number of mines (1-24):", font=self.label_font, bg=self.bg_color, fg=self.text_color).grid(row=1, column=0, padx=10)
        self.mines_input = tk.Entry(self.bet_frame)
        self.mines_input.grid(row=1, column=1, padx=10)

        # Start game button
        self.start_game_btn = tk.Button(root, text="Start Game", font=self.button_font, bg=self.accent_color, fg=self.bg_color, command=self.start_game)
        self.start_game_btn.pack(pady=20)

        # Frame for the minefield grid and control panel
        self.main_frame = tk.Frame(root, bg=self.bg_color)
        self.main_frame.pack(pady=10)

        # Grid frame
        self.grid_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.grid_frame.pack(side=tk.LEFT, padx=10)

        # Control panel frame
        self.control_panel = tk.Frame(self.main_frame, bg=self.bg_color)
        self.control_panel.pack(side=tk.LEFT, padx=10)

        # Bet amount display
        self.bet_amount_label = tk.Label(self.control_panel, text="Current Bet Amount: $0", font=self.label_font, bg=self.bg_color, fg=self.accent_color)
        self.bet_amount_label.pack(pady=10)

        # Finish button
        self.finish_button = tk.Button(self.control_panel, text="Finish Game", command=self.finish_game, font=self.button_font, bg="#32CD32", fg=self.text_color)
        self.finish_button.pack(pady=10)

        # Winner text
        self.winner_label = tk.Label(self.control_panel, text="", font=self.label_font, bg=self.bg_color, fg=self.accent_color)
        self.winner_label.pack(pady=10)

        # Back to Menu button
        self.back_button = tk.Button(self.control_panel, text="Back to Menu", command=self.back_to_menu, font=self.label_font, bg="#32CD32", fg=self.text_color)
        self.back_button.pack(pady=20)

        # Initialize game variables
        self.grid_size = 5  # 5x5 grid
        self.mine_positions = []
        self.bet_amount = 0
        self.num_mines = 0
        self.mine_grid = []
        self.current_bet_amount = 0
        self.game_active = False
        self.initial_balance = money

    def toggle_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))

    def quit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)

    def start_game(self):
        try:
            self.bet_amount = int(self.bet_amount_input.get().strip())
            self.num_mines = int(self.mines_input.get().strip())
        except ValueError:
            self.money_label.config(text="Invalid input. Please enter valid numbers.")
            return

        if self.bet_amount <= 0 or self.num_mines <= 0 or self.num_mines >= self.grid_size * self.grid_size:
            self.money_label.config(text="Invalid bet amount or number of mines. Try again.")
            return

        if self.bet_amount > self.money:
            self.money_label.config(text="Not enough balance. Try a lower bet.")
            return

        self.money -= self.bet_amount
        self.update_money()

        # Generate random mine positions
        self.mine_positions = random.sample(range(self.grid_size * self.grid_size), self.num_mines)

        # Create the grid
        self.create_grid()
        self.game_active = True

    def create_grid(self):
        # Clear the previous grid, if any
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.mine_grid = []  # To store buttons in the grid

        # Create 5x5 grid of buttons inside grid_frame
        for row in range(self.grid_size):
            row_buttons = []
            for col in range(self.grid_size):
                button = tk.Button(self.grid_frame, text="?", width=4, height=2, font=("Arial", 16),
                                   command=lambda r=row, c=col: self.reveal_tile(r, c))
                button.grid(row=row, column=col, padx=5, pady=5)
                row_buttons.append(button)
            self.mine_grid.append(row_buttons)

    def reveal_tile(self, row, col):
        if not self.game_active:
            return
        
        index = row * self.grid_size + col

        if index in self.mine_positions:
            self.mine_grid[row][col].config(text="💣", bg="red", fg="white", state="disabled")
            self.money_label.config(text=f"You hit a mine! You lost ${self.bet_amount}.")
            self.current_bet_amount = 0
            self.update_bet_amount()
            self.reveal_all_mines()
            self.game_active = False
        else:
            self.mine_grid[row][col].config(text="✓", bg="green", fg="white", state="disabled")
            # Calculate bet amount increment
            increment = self.initial_balance * (self.num_mines / 10)
            self.current_bet_amount += increment
            self.update_bet_amount()

    def reveal_all_mines(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                index = row * self.grid_size + col
                if index in self.mine_positions:
                    self.mine_grid[row][col].config(text="💣", bg="red", fg="white", state="disabled")
                else:
                    self.mine_grid[row][col].config(text="✓", bg="green", fg="white", state="disabled")

    def update_bet_amount(self):
        self.bet_amount_label.config(text=f"Current Bet Amount: ${self.current_bet_amount:.2f}")

    def finish_game(self):
        if not self.game_active:
            return

        if self.current_bet_amount > 0:
            total_winnings = self.current_bet_amount + self.bet_amount  # Add initial bet to winnings
            self.money += total_winnings
            self.winner_label.config(text=f"Game finished. You won ${total_winnings:.2f}!")
        else:
            self.winner_label.config(text="Game finished. You lost everything.")

        self.update_money()
        self.reveal_all_mines()
        self.current_bet_amount = 0
        self.update_bet_amount()
        self.game_active = False

    def update_money(self):
        self.money_label.config(text=f"Current Balance: ${self.money:.2f}")

    def back_to_menu(self):
        self.root.destroy()  # Closes the current window
        self.return_to_menu(self.money)  # Reopens the main menu with the updated money

def start_mines_game(user_money):
    root = tk.Tk()
    game = MinesGame(root, user_money, return_to_menu=start_main_menu)
    root.mainloop()

def start_main_menu(user_money):
    import main_menu  # Import here to avoid circular import
    main_menu.main_menu(user_money)

if __name__ == "__main__":
    start_mines_game(1000)  # Starts the game with initial money of 1000
