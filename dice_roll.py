import tkinter as tk
import random

class DiceRollGame:
    def __init__(self, root, money, return_to_menu):
        self.root = root
        self.root.title("Dice Roll Game")
        
        # Set window to fullscreen but windowed
        self.root.attributes('-fullscreen', True)
        self.root.bind("<F11>", self.toggle_fullscreen)  # Allow toggling fullscreen mode with F11
        self.root.bind("<Escape>", self.quit_fullscreen)  # Exit fullscreen mode with Escape

        self.money = money
        self.return_to_menu = return_to_menu

        # Set background color and font
        self.bg_color = "#2E8B57"
        self.accent_color = "#FFD700"
        self.text_color = "#FFFFFF"
        self.title_font = ("Arial", 24, "bold")
        self.label_font = ("Arial", 16)
        self.dice_font = ("Arial", 48)

        self.root.configure(bg=self.bg_color)

        # Game title
        self.title_label = tk.Label(root, text="Welcome to Dice Roll!", font=self.title_font, bg=self.bg_color, fg=self.accent_color)
        self.title_label.pack(pady=15)  # Reduced padding

        # Display current money
        self.money_label = tk.Label(root, text=f"Current Balance: ${self.money}", font=self.label_font, bg=self.bg_color, fg=self.accent_color)
        self.money_label.pack(pady=5)  # Reduced padding

        # Frame for dice display
        self.dice_frame = tk.Frame(root, bg=self.bg_color)
        self.dice_frame.pack(pady=15)  # Reduced padding

        # Dice boxes
        self.dice1_box = tk.Label(self.dice_frame, text="", font=self.dice_font, width=5, height=3, bg="white", borderwidth=2, relief="solid")
        self.dice2_box = tk.Label(self.dice_frame, text="", font=self.dice_font, width=5, height=3, bg="white", borderwidth=2, relief="solid")
        self.dice1_box.grid(row=0, column=0, padx=15, pady=5)  # Reduced padding
        self.dice2_box.grid(row=0, column=1, padx=15, pady=5)  # Reduced padding

        # Result display for total of dice
        self.result_label = tk.Label(root, text="", font=self.dice_font, bg=self.bg_color, fg=self.accent_color)
        self.result_label.pack(pady=5)  # Reduced padding

        # Bet options
        self.bet_frame = tk.Frame(root, bg=self.bg_color)
        self.bet_frame.pack(pady=15)  # Reduced padding

        self.bet_number_btn = tk.Button(self.bet_frame, text="Bet on Number", command=self.bet_number, font=self.label_font, bg="#FF6347", fg=self.text_color)
        self.bet_odd_even_btn = tk.Button(self.bet_frame, text="Bet on Odd/Even", command=self.bet_odd_even, font=self.label_font, bg="#4682B4", fg=self.text_color)
        self.bet_number_btn.grid(row=0, column=0, padx=15, pady=5)  # Reduced padding
        self.bet_odd_even_btn.grid(row=0, column=1, padx=15, pady=5)  # Reduced padding

        # Winner text
        self.winner_label = tk.Label(root, text="", font=self.label_font, bg=self.bg_color, fg=self.accent_color)
        self.winner_label.pack(pady=5)  # Reduced padding

        # Back to Menu button
        self.back_button = tk.Button(root, text="Back to Menu", command=self.back_to_menu, font=self.label_font, bg="#32CD32", fg=self.text_color)
        self.back_button.pack(pady=20, side=tk.BOTTOM)  # Added more padding to bottom

    def toggle_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))

    def quit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)

    def roll_dice(self):
        return random.randint(1, 6), random.randint(1, 6)

    def update_money(self, amount):
        self.money += amount
        self.money_label.config(text=f"Current Balance: ${self.money}")

    def bet_number(self):
        self.get_user_input("Enter the number you want to bet on (2-12):", 'number')

    def bet_odd_even(self):
        self.get_user_input("Enter Odd or Even:", 'odd_even')

    def get_user_input(self, prompt, bet_type):
        self.input_window = tk.Toplevel(self.root)
        self.input_window.title("Input")
        self.input_window.geometry("300x200")
        self.input_window.configure(bg=self.bg_color)

        tk.Label(self.input_window, text=prompt, bg=self.bg_color, fg=self.text_color).pack(pady=10)
        self.user_input = tk.Entry(self.input_window)
        self.user_input.pack(pady=10)

        bet_amount_label = tk.Label(self.input_window, text="Enter your bet amount:", bg=self.bg_color, fg=self.text_color)
        bet_amount_label.pack(pady=10)
        self.bet_amount_input = tk.Entry(self.input_window)
        self.bet_amount_input.pack(pady=10)

        submit_btn = tk.Button(self.input_window, text="Submit", command=lambda: self.submit_bet(bet_type))
        submit_btn.pack(pady=10)

    def submit_bet(self, bet_type):
        bet_value = self.user_input.get().strip()
        try:
            bet_amount = int(self.bet_amount_input.get().strip())
        except ValueError:
            self.winner_label.config(text="Invalid bet amount. Please enter a number.")
            self.input_window.destroy()
            return

        if bet_amount <= 0:
            self.winner_label.config(text="Bet amount must be greater than zero.")
            self.input_window.destroy()
            return

        self.input_window.destroy()

        total_bet = bet_amount
        if total_bet > self.money:
            self.winner_label.config(text="Not enough money to place this bet.")
            return

        self.update_money(-total_bet)

        die1, die2 = self.roll_dice()
        total = die1 + die2

        self.dice1_box.config(text=str(die1))
        self.dice2_box.config(text=str(die2))
        self.result_label.config(text=f"Total: {total}")

        win, payout = self.check_win(bet_type, bet_value, total)

        if win:
            winnings = bet_amount * payout
            self.update_money(winnings)
            self.winner_label.config(text=f"Ye rolled {die1} and {die2}! Ye win ${winnings}!")
        else:
            self.winner_label.config(text=f"Ye rolled {die1} and {die2}. Ye lost ${total_bet}. Try again!")

    def check_win(self, bet_type, bet_value, total):
        win = False
        payout = 0

        if bet_type == 'number':
            if str(total) == bet_value:
                win = True
                payout = 6
        elif bet_type == 'odd_even':
            if (bet_value.lower() == "odd" and total % 2 != 0) or (bet_value.lower() == "even" and total % 2 == 0):
                win = True
                payout = 2

        return win, payout

    def back_to_menu(self):
        self.root.destroy()  # Closes the current window
        start_main_menu(self.money)  # Reopens the main menu with the updated money

def start_dice_roll_game(user_money):
    root = tk.Tk()
    game = DiceRollGame(root, user_money, return_to_menu=start_main_menu)
    root.mainloop()

def start_main_menu(user_money):
    import main_menu  # Import here to avoid circular import
    main_menu.main_menu(user_money)

if __name__ == "__main__":
    start_dice_roll_game(1000)  # Starts the dice roll game with initial money of 1000
