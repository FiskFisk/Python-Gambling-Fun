import tkinter as tk
from tkinter import font as tkfont
from roulette_game import start_roulette_game
import dice_roll
from mines_game import start_mines_game  # Import the Mines game

# Initialize user money
user_money = 10000

def main_menu(user_money):
    main_window = tk.Tk()
    main_window.title("Casino Menu")
    main_window.geometry("800x500")
    main_window.configure(bg="#2E8B57")

    # Custom font
    custom_font = tkfont.Font(family="Helvetica", size=16, weight="bold")

    # Title label
    title_label = tk.Label(main_window, text="Welcome to the Casino!", font=("Arial", 24, "bold"), bg="#2E8B57", fg="#FFD700")
    title_label.pack(pady=20)

    # Display current money
    money_label = tk.Label(main_window, text=f"Money: ${user_money}", font=custom_font, bg="#2E8B57", fg="#FFD700")
    money_label.pack(pady=10)

    # Roulette Button
    btn_roulette = tk.Button(main_window, text="Play Roulette", command=lambda: [main_window.destroy(), start_roulette_game(user_money)],
                             font=custom_font, width=20, height=2, bg="#FFD700", fg="#2E8B57", relief="raised")
    btn_roulette.pack(pady=15)

    # Dice Roll Button
    btn_dice_roll = tk.Button(main_window, text="Roll the Dice", command=lambda: [main_window.destroy(), dice_roll.start_dice_roll_game(user_money)],
                              font=custom_font, width=20, height=2, bg="#FF6347", fg="#FFFFFF", relief="raised")
    btn_dice_roll.pack(pady=15)

    # Mines Game Button
    btn_mines = tk.Button(main_window, text="Play Mines", command=lambda: [main_window.destroy(), start_mines_game(user_money)],
                          font=custom_font, width=20, height=2, bg="#32CD32", fg="#FFFFFF", relief="raised")
    btn_mines.pack(pady=15)

    # Spacing at the bottom
    bottom_frame = tk.Frame(main_window, bg="#2E8B57")
    bottom_frame.pack(pady=20)

    main_window.mainloop()

if __name__ == "__main__":
    main_menu(user_money)
