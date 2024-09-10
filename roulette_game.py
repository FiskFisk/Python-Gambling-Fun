import tkinter as tk
import random

# Roulette numbers and corresponding colors
roulette_wheel = {
    0: "Green", 1: "Red", 2: "Black", 3: "Red", 4: "Black", 5: "Red",
    6: "Black", 7: "Red", 8: "Black", 9: "Red", 10: "Black", 11: "Black",
    12: "Red", 13: "Black", 14: "Red", 15: "Black", 16: "Red", 17: "Black",
    18: "Red", 19: "Red", 20: "Black", 21: "Red", 22: "Black", 23: "Red",
    24: "Black", 25: "Red", 26: "Black", 27: "Red", 28: "Black", 29: "Black",
    30: "Red", 31: "Black", 32: "Red", 33: "Black", 34: "Red", 35: "Black",
    36: "Red"
}

class RouletteGame:
    def __init__(self, root, money, return_to_menu):
        self.root = root
        self.root.title("Roulette Game")
        
        # Set window to fullscreen but windowed
        self.root.attributes('-fullscreen', True)
        self.root.bind("<F11>", self.toggle_fullscreen)  # Allow toggling fullscreen mode with F11
        self.root.bind("<Escape>", self.quit_fullscreen)  # Exit fullscreen mode with Escape

        self.money = money
        self.return_to_menu = return_to_menu

        # Set background color and fonts
        self.bg_color = "#2E8B57"  # Medium sea green background color
        self.accent_color = "#FFD700"  # Gold accent color
        self.text_color = "#FFFFFF"  # White text color
        self.title_font = ("Arial", 24, "bold")
        self.label_font = ("Arial", 16)
        self.button_font = ("Arial", 14)
        self.canvas_font = ("Arial", 48)
        
        self.root.configure(bg=self.bg_color)

        # Game title
        self.title_label = tk.Label(root, text="Welcome to Roulette!", font=self.title_font, bg=self.bg_color, fg=self.accent_color)
        self.title_label.pack(pady=20)

        # Display current money
        self.money_label = tk.Label(root, text=f"Current Balance: ${self.money}", font=self.label_font, bg=self.bg_color, fg=self.accent_color)
        self.money_label.pack(pady=10)

        # Canvas for the roulette wheel (just a decorative circle)
        self.canvas = tk.Canvas(root, width=300, height=300, bg=self.bg_color, highlightthickness=0)
        self.oval = self.canvas.create_oval(20, 20, 280, 280, fill="black", outline="white")
        self.number_text = self.canvas.create_text(150, 150, text="", font=self.canvas_font, fill="white")
        self.canvas.pack(pady=10)

        # Bet buttons arranged in a grid
        self.bet_frame = tk.Frame(root, bg=self.bg_color)
        self.bet_frame.pack(pady=10)

        self.bet_number_btn = tk.Button(self.bet_frame, text="Bet on Numbers", command=self.bet_numbers, font=self.button_font, bg="#FF6347", fg=self.text_color)
        self.bet_color_btn = tk.Button(self.bet_frame, text="Bet on Color", command=self.bet_color, font=self.button_font, bg="#4682B4", fg=self.text_color)
        self.bet_odd_even_btn = tk.Button(self.bet_frame, text="Bet on Odd/Even", command=self.bet_odd_even, font=self.button_font, bg="#32CD32", fg=self.text_color)
        self.bet_range_btn = tk.Button(self.bet_frame, text="Bet on Range", command=self.bet_range, font=self.button_font, bg="#FFD700", fg=self.text_color)

        self.bet_number_btn.grid(row=0, column=0, padx=15, pady=5)
        self.bet_color_btn.grid(row=0, column=1, padx=15, pady=5)
        self.bet_odd_even_btn.grid(row=1, column=0, padx=15, pady=5)
        self.bet_range_btn.grid(row=1, column=1, padx=15, pady=5)

        # Result label (Winner text)
        self.result_label = tk.Label(root, text="", font=self.label_font, bg=self.bg_color, fg=self.accent_color)
        self.result_label.pack(pady=10)

        # Back to Menu button
        self.back_button = tk.Button(root, text="Back to Menu", command=self.back_to_menu, font=self.label_font, bg="#32CD32", fg=self.text_color)
        self.back_button.pack(pady=20, side=tk.BOTTOM)

    def toggle_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))

    def quit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)

    def spin_wheel(self):
        return random.randint(0, 36)

    def update_money(self, amount):
        self.money += amount
        self.money_label.config(text=f"Current Balance: ${self.money}")

    def bet_numbers(self):
        self.get_user_input("Enter the numbers ye want to bet on (separated by commas):", 'number')

    def bet_color(self):
        self.get_user_input("Enter the color (Red or Black):", 'color')

    def bet_odd_even(self):
        self.get_user_input("Enter Odd or Even:", 'odd_even')

    def bet_range(self):
        self.get_user_input("Enter 'low' for 1-18 or 'high' for 19-36:", 'range')

    def get_user_input(self, prompt, bet_type):
        self.input_window = tk.Toplevel(self.root)
        self.input_window.title("Input")
        self.input_window.geometry("300x200")
        self.input_window.configure(bg=self.bg_color)

        tk.Label(self.input_window, text=prompt, bg=self.bg_color, fg=self.text_color).pack(pady=10)
        self.user_input = tk.Entry(self.input_window)
        self.user_input.pack(pady=10)

        bet_amount_label = tk.Label(self.input_window, text="Enter yer bet amount:", bg=self.bg_color, fg=self.text_color)
        bet_amount_label.pack(pady=10)
        self.bet_amount_input = tk.Entry(self.input_window)
        self.bet_amount_input.pack(pady=10)

        submit_btn = tk.Button(self.input_window, text="Submit", command=lambda: self.submit_bet(bet_type))
        submit_btn.pack(pady=10)

    def submit_bet(self, bet_type):
        bets = self.user_input.get().strip().split(',')
        bets = [bet.strip() for bet in bets]
        try:
            bet_amount = int(self.bet_amount_input.get().strip())
        except ValueError:
            self.result_label.config(text="Invalid bet amount. Please enter a number.")
            self.input_window.destroy()
            return
        
        if bet_amount <= 0:
            self.result_label.config(text="Bet amount must be greater than zero.")
            self.input_window.destroy()
            return

        self.input_window.destroy()

        total_bet = bet_amount * len(bets)

        if total_bet > self.money:
            self.result_label.config(text="Not enough doubloons to place this bet.")
            return

        self.update_money(-total_bet)

        winning_number = self.spin_wheel()
        winning_color = roulette_wheel[winning_number]

        win, payout = self.check_win(bet_type, bets, winning_number)

        # Update the circle with the winning number and change its color
        self.canvas.itemconfig(self.oval, fill=winning_color.lower())
        self.canvas.itemconfig(self.number_text, text=str(winning_number))

        if win:
            winnings = bet_amount * payout
            self.update_money(winnings)
            self.result_label.config(text=f"The ball lands on {winning_number} ({winning_color})! Ye win ${winnings}!")
        else:
            self.result_label.config(text=f"The ball lands on {winning_number} ({winning_color})! Ye lost ${total_bet}. Try again!")

    def check_win(self, bet_type, bets, winning_number):
        winning_color = roulette_wheel[winning_number]
        win = False
        payout = 0

        if bet_type == 'number':
            if str(winning_number) in bets:
                win = True
                payout = 35
        elif bet_type == 'color':
            if bets[0].lower() == winning_color.lower():
                win = True
                payout = 2
        elif bet_type == 'odd_even':
            if (bets[0].lower() == "odd" and winning_number % 2 != 0) or (bets[0].lower() == "even" and winning_number % 2 == 0):
                win = True
                payout = 2
        elif bet_type == 'range':
            if (bets[0].lower() == 'low' and 1 <= winning_number <= 18) or (bets[0].lower() == 'high' and 19 <= winning_number <= 36):
                win = True
                payout = 2

        return win, payout

    def back_to_menu(self):
        self.root.destroy()  # Closes the current window
        start_main_menu(self.money)  # Reopens the main menu with the updated money

def start_roulette_game(user_money):
    root = tk.Tk()
    game = RouletteGame(root, user_money, return_to_menu=start_main_menu)
    root.mainloop()

def start_main_menu(user_money):
    import main_menu  # Import here to avoid circular import
    main_menu.main_menu(user_money)

if __name__ == "__main__":
    start_roulette_game(1000)  # Starts the game with initial money of 1000
