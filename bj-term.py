# Import necessary modules
import os
import sys
import random
from art import *
import argparse
import json
from datetime import datetime
from colorama import init, Fore, Back, Style
import time

# Initialize colorama for cross-platform colored output
init(autoreset=True)
print(Back.BLACK + Fore.WHITE, end='')

class Stats:
    def __init__(self):
        self.games_played = 0
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.biggest_win = 0
        self.biggest_loss = 0
        self.current_streak = 0
        self.best_streak = 0
        
    def update(self, result, amount):
        self.games_played += 1
        if result == "win":
            self.wins += 1
            self.current_streak = max(1, self.current_streak + 1)
            self.biggest_win = max(self.biggest_win, amount)
        elif result == "loss":
            self.losses += 1
            self.current_streak = min(-1, self.current_streak - 1)
            self.biggest_loss = min(self.biggest_loss, amount)
        else:  # push
            self.pushes += 1
            self.current_streak = 0
        self.best_streak = max(self.best_streak, abs(self.current_streak))
        
    def display(self, current_balance=None):
        stats_display = f"""{Back.BLACK}{Fore.CYAN}
    STATISTICS

    Games Played:   {Back.BLACK}{stats.games_played}{Style.RESET_ALL}
    Wins:           {Back.BLACK}{Fore.GREEN}{stats.wins}{Style.RESET_ALL}
    Losses:         {Back.BLACK}{Fore.RED}{stats.losses}{Style.RESET_ALL}
    Pushes:         {Back.BLACK}{stats.pushes}{Style.RESET_ALL}
    Biggest Win:    ${Back.BLACK}{Fore.GREEN}{stats.biggest_win}{Style.RESET_ALL}
    Biggest Loss:   ${Back.BLACK}{Fore.RED}{stats.biggest_loss}{Style.RESET_ALL}
    Current Streak: {Back.BLACK}{stats.current_streak}{Style.RESET_ALL}
    Best Streak:    {Back.BLACK}{stats.best_streak}{Style.RESET_ALL}
    Current Balance: ${Back.BLACK}{current_balance}{Style.RESET_ALL}
    {Style.RESET_ALL}"""
        print(stats_display)

class Deck:
    def __init__(self):
        self.reset()
        
    def reset(self):
        suits = ["Spades", "Diamonds", "Hearts", "Clubs"]
        values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards = [{"suit": s, "value": v} for s in suits for v in values]
        random.shuffle(self.cards)
        
    def deal(self):
        if len(self.cards) < 10:  # Reshuffle when deck gets low
            self.reset()
        return self.cards.pop()

def save_game(balance, stats):
    save_data = {
        "balance": balance,
        "stats": stats.__dict__,
        "timestamp": datetime.now().isoformat()
    }
    with open("blackjack_save.json", "w") as f:
        json.dump(save_data, f)
    print(f"{Back.BLACK}{Fore.GREEN}    Game saved successfully!{Style.RESET_ALL}")

def load_game():
    try:
        with open("blackjack_save.json", "r") as f:
            data = json.load(f)
            stats = Stats()
            stats.__dict__.update(data["stats"])
            return data["balance"], stats
    except FileNotFoundError:
        return 100, Stats()

# Suppress pygame welcome message
old_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')

import pygame
from pygame import mixer

sys.stdout = old_stdout

# Clear the terminal or console screen
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')
    try:
        # Try to get terminal size and fill with black background
        columns, lines = os.get_terminal_size()
        print(Back.BLACK + ' ' * columns * lines, end='')
        print('\033[H', end='')  # Move cursor to top-left
    except OSError:
        # Fallback if we can't get terminal size
        print(Back.BLACK + '\n' * 100, end='')
        print('\033[H', end='')  # Move cursor to top-left

# Initialize pygame and mixer
pygame.init()
mixer.init()

# Function to play a sound file
def play_sound(file):
    if not args.no_sound:
        mixer.Sound(file).play()

# Function to randomly deal a card
def deal_card():
    suits = ["Spades", "Diamonds", "Hearts", "Clubs"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    card = {"suit": random.choice(suits), "value": random.choice(values)}
    return card

# Function to calculate the score of a hand
def calculate_score(hand):
    total = 0
    aces = 0
    for card in hand:
        value = card["value"]
        if value == "A":
            aces += 1
            total += 11
        elif value in ["K", "Q", "J"]:
            total += 10
        else:
            total += int(value)

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total

# Function to ask user if they want to play again
def play_again():
    while True:
        choice = input("    Do you want to play again? (y/n): ").lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("    Invalid input, please try again.")

# This function displays the hands of both the player and the dealer
def display_hands(player_hand, dealer_hand, hidden=True):
    clear_screen()
    print(Back.BLACK, end='')  # Ensure black background persists
    display_title()
    
    score = calculate_score(player_hand)
    color = Fore.GREEN if score <= 21 else Fore.RED
    
    # Display dealer's hand
    print(f"{Back.BLACK}    {Fore.CYAN}♠ ♥ DEALER'S HAND ♦ ♣{Style.RESET_ALL}{Back.BLACK}")
    
    if hidden:
        print(f"{Back.BLACK}    {Fore.YELLOW}Hidden{Style.RESET_ALL}{Back.BLACK}")
        print_cards([reg_card_visual(c) for c in dealer_hand[:1]] + [hidden_card()], padding=f"{Back.BLACK}    ")
    else:
        dealer_score = calculate_score(dealer_hand)
        color_dealer = Fore.GREEN if dealer_score <= 21 else Fore.RED
        print(f"{Back.BLACK}    {color_dealer}{dealer_score}{Style.RESET_ALL}{Back.BLACK}")
        print_cards([reg_card_visual(c) for c in dealer_hand], padding=f"{Back.BLACK}    ")
    
    # Display player's hand
    print(f"{Back.BLACK}\n{Back.BLACK}")
    print(f"{Back.BLACK}    {Fore.CYAN}♠ ♥ PLAYER'S HAND ♦ ♣{Style.RESET_ALL}{Back.BLACK}")
    print(f"{Back.BLACK}    {color}{score}{Style.RESET_ALL}{Back.BLACK}")
    print_cards([reg_card_visual(c) for c in player_hand], padding=f"{Back.BLACK}    ")
    print(Back.BLACK)

def hidden_card():
    card = [
        f'{Back.BLACK}{Fore.WHITE}╭─────────╮{Style.RESET_ALL}',
        f'{Back.BLACK}{Fore.WHITE}│{Fore.BLUE}░░░░░░░░░{Fore.WHITE}│{Style.RESET_ALL}',
        f'{Back.BLACK}{Fore.WHITE}│{Fore.BLUE}░░░░░░░░░{Fore.WHITE}│{Style.RESET_ALL}',
        f'{Back.BLACK}{Fore.WHITE}│{Fore.BLUE}░░░░░░░░░{Fore.WHITE}│{Style.RESET_ALL}',
        f'{Back.BLACK}{Fore.WHITE}│{Fore.BLUE}░░░░░░░░░{Fore.WHITE}│{Style.RESET_ALL}',
        f'{Back.BLACK}{Fore.WHITE}│{Fore.BLUE}░░░░░░░░░{Fore.WHITE}│{Style.RESET_ALL}',
        f'{Back.BLACK}{Fore.WHITE}╰─────────╯{Style.RESET_ALL}'
    ]
    return card

def display_title():
    title = f"""{Back.BLACK}
{Back.BLACK}
{Back.BLACK}    {Fore.BLUE}██████╗ ██╗      █████╗  ██████╗██╗  ██╗     ██╗ █████╗  ██████╗██╗  ██╗{Style.RESET_ALL}{Back.BLACK}
{Back.BLACK}    {Fore.BLUE}██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝     ██║██╔══██╗██╔════╝██║ ██╔╝{Style.RESET_ALL}{Back.BLACK}
{Back.BLACK}    {Fore.CYAN}██████╔╝██║     ███████║██║     █████╔╝      ██║███████║██║     █████╔╝{Style.RESET_ALL}{Back.BLACK}
{Back.BLACK}    {Fore.CYAN}██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██   ██║██╔══██║██║     ██╔═██╗{Style.RESET_ALL}{Back.BLACK}
{Back.BLACK}    {Fore.WHITE}██████╔╝███████╗██║  ██║╚██████╗██║  ██╗╚█████╔╝██║  ██║╚██████╗██║  ██╗{Style.RESET_ALL}{Back.BLACK}
{Back.BLACK}    {Fore.WHITE}╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝{Style.RESET_ALL}{Back.BLACK}

{Back.BLACK}             {Fore.BLUE}♠{Fore.WHITE} Press ENTER to start  {Fore.CYAN}♥{Fore.WHITE} 'h' for help  {Fore.WHITE}♦{Fore.WHITE} 'q' to quit {Fore.BLUE}♣{Style.RESET_ALL}{Back.BLACK}

{Back.BLACK}"""
    print(title)

def display_stats(stats, current_balance=None):
    stats_display = f"""{Back.BLACK}
{Back.BLACK}    {Fore.CYAN}STATISTICS{Style.RESET_ALL}{Back.BLACK}

{Back.BLACK}    Games Played:   {stats.games_played}{Style.RESET_ALL}{Back.BLACK}
{Back.BLACK}    Wins:           {Fore.GREEN}{stats.wins}{Style.RESET_ALL}{Back.BLACK}
{Back.BLACK}    Losses:         {Fore.RED}{stats.losses}{Style.RESET_ALL}{Back.BLACK}
{Back.BLACK}    Pushes:         {stats.pushes}{Style.RESET_ALL}{Back.BLACK}
{Back.BLACK}    Biggest Win:    ${Fore.GREEN}{stats.biggest_win}{Style.RESET_ALL}{Back.BLACK}
{Back.BLACK}    Biggest Loss:   ${Fore.RED}{stats.biggest_loss}{Style.RESET_ALL}{Back.BLACK}
{Back.BLACK}    Current Streak: {stats.current_streak}{Style.RESET_ALL}{Back.BLACK}
{Back.BLACK}    Best Streak:    {stats.best_streak}{Style.RESET_ALL}{Back.BLACK}
{Back.BLACK}    Current Balance: ${current_balance}{Style.RESET_ALL}{Back.BLACK}
"""
    print(stats_display)

def display_game_options():
    options = f"""{Back.BLACK}
{Back.BLACK}    {Fore.CYAN}OPTIONS{Style.RESET_ALL}{Back.BLACK}

{Back.BLACK}    (H) Hit     - Draw another card{Style.RESET_ALL}{Back.BLACK}
{Back.BLACK}    (S) Stand   - Keep current hand{Style.RESET_ALL}{Back.BLACK}
{Back.BLACK}    (D) Double  - Double bet & draw{Style.RESET_ALL}{Back.BLACK}
{Back.BLACK}    (Q) Quit    - Exit game{Style.RESET_ALL}{Back.BLACK}
{Back.BLACK}    (?) Help    - Show commands{Style.RESET_ALL}{Back.BLACK}
"""
    print(options)

def display_next_move_options():
    print(f"\n{Back.BLACK}    {Fore.CYAN}What would you like to do next?{Style.RESET_ALL}{Back.BLACK}")
    print(f"{Back.BLACK}    1. Continue playing{Style.RESET_ALL}{Back.BLACK}")
    print(f"{Back.BLACK}    2. Save and quit{Style.RESET_ALL}{Back.BLACK}")
    print(f"{Back.BLACK}    3. View statistics{Style.RESET_ALL}{Back.BLACK}")
    print(f"{Back.BLACK}    4. Reset balance to $100{Style.RESET_ALL}{Back.BLACK}")

def display_game_over():
    message = f"""{Back.BLACK}
{Back.BLACK}    Game Over! Your balance has been reset to $100.
{Back.BLACK}    Better luck next time!{Style.RESET_ALL}{Back.BLACK}
{Back.BLACK}"""
    print(message)
    input(f"{Back.BLACK}    Press Enter to continue...{Style.RESET_ALL}{Back.BLACK}")
    return 100

def display_bet_prompt(balance):
    print(f"\n{Back.BLACK}    {Fore.CYAN}Current Balance: ${balance}{Style.RESET_ALL}{Back.BLACK}")
    return get_bet(balance)

def display_result(message, amount, new_balance):
    color = Fore.GREEN if amount > 0 else Fore.RED if amount < 0 else Fore.YELLOW
    print(f"\n{Back.BLACK}    {color}{message}{Style.RESET_ALL}{Back.BLACK}")
    print(f"{Back.BLACK}    New Balance: ${new_balance}{Style.RESET_ALL}{Back.BLACK}")

def get_bet(balance):
    while True:
        try:
            bet = int(input(f"{Back.BLACK}    {Fore.CYAN}Enter your bet (1-{balance}): {Style.RESET_ALL}{Back.BLACK}"))
            if bet > 0 and bet <= balance:
                return bet
            else:
                print(f"{Back.BLACK}    Invalid bet, please try again.{Style.RESET_ALL}{Back.BLACK}")
        except ValueError:
            print(f"{Back.BLACK}    Invalid input, please enter a number.{Style.RESET_ALL}{Back.BLACK}")

def player_turn(player_hand, dealer_hand, bet, balance):
    while True:
        choice = input(f"\n{Back.BLACK}    {Fore.CYAN}(h)it, (s)tand, (d)ouble, (q)uit, or (?) help: {Style.RESET_ALL}{Back.BLACK}").lower()
        if choice in ['h', 'hit']:
            player_hand.append(deck.deal())
            play_sound("sounds/deal.wav")
            display_hands(player_hand, dealer_hand)
            if calculate_score(player_hand) > 21:
                return ('bust', bet)
        elif choice in ['s', 'stand', 'stay']:
            return ('stand', bet)
        elif choice in ['d', 'dbl', 'double']:
            if len(player_hand) == 2 and balance >= bet:
                player_hand.append(deck.deal())
                play_sound("sounds/deal.wav")
                display_hands(player_hand, dealer_hand)
                return ('double', bet * 2)
            else:
                print(f"{Back.BLACK}    You can only double down on your first two cards and if you have enough balance.{Style.RESET_ALL}{Back.BLACK}")
        elif choice in ['q', 'quit']:
            return ('quit', bet)
        elif choice == '?':
            display_help()
            display_hands(player_hand, dealer_hand)
        else:
            print(f"{Back.BLACK}    Invalid choice. Type ? for help.{Style.RESET_ALL}{Back.BLACK}")

def display_help():
    print(f"\n{Back.BLACK}    {Fore.CYAN}=== Blackjack Commands ==={Style.RESET_ALL}{Back.BLACK}")
    print(f"{Back.BLACK}    h or hit  - Draw another card{Style.RESET_ALL}{Back.BLACK}")
    print(f"{Back.BLACK}    s or stay - Keep your current hand{Style.RESET_ALL}{Back.BLACK}")
    print(f"{Back.BLACK}    d or dbl  - Double down (double bet, one more card){Style.RESET_ALL}{Back.BLACK}")
    print(f"{Back.BLACK}    q or quit - Save and exit game{Style.RESET_ALL}{Back.BLACK}")
    print(f"{Back.BLACK}    ?        - Show this help message{Style.RESET_ALL}{Back.BLACK}")
    
    print(f"\n{Back.BLACK}    {Fore.CYAN}=== Game Rules ==={Style.RESET_ALL}{Back.BLACK}")
    print(f"{Back.BLACK}    • Try to get closer to 21 than the dealer without going over{Style.RESET_ALL}{Back.BLACK}")
    print(f"{Back.BLACK}    • Number cards are worth their face value{Style.RESET_ALL}{Back.BLACK}")
    print(f"{Back.BLACK}    • Face cards (J, Q, K) are worth 10{Style.RESET_ALL}{Back.BLACK}")
    print(f"{Back.BLACK}    • Aces are worth 11 or 1, whichever is better{Style.RESET_ALL}{Back.BLACK}")
    print(f"{Back.BLACK}    • Dealer must hit on 16 and below, stand on 17 and above{Style.RESET_ALL}{Back.BLACK}")
    print(f"{Back.BLACK}    • Blackjack (A + 10/Face card) pays 3:2{Style.RESET_ALL}{Back.BLACK}")

def print_cards(cardlist, padding=""):
    if not cardlist:
        return
    
    # Add black background to padding and between cards
    formatted_padding = f"{Back.BLACK}{padding}"
    card_separator = f"{Back.BLACK}  "
    
    for i in range(len(cardlist[0])):
        print(formatted_padding + card_separator.join(card[i] for card in cardlist) + Back.BLACK)

def reg_card_visual(card):
    suits = "Spades Diamonds Hearts Clubs".split()
    suit_symbols = ['♠','♦','♥','♣']
    suit_colors = {
        '♠': Fore.WHITE,
        '♦': Fore.RED,
        '♥': Fore.RED,
        '♣': Fore.WHITE
    }
    
    # Get card details
    value = card["value"]
    suit = suit_symbols[suits.index(card["suit"])]
    color = suit_colors[suit]
    
    # Create a decorative card
    card = [
        f'{Back.BLACK}{Fore.WHITE}╭─────────╮{Style.RESET_ALL}',
        f'{Back.BLACK}{Fore.WHITE}│{color}{value:<9}{Fore.WHITE}│{Style.RESET_ALL}',
        f'{Back.BLACK}{Fore.WHITE}│         │{Style.RESET_ALL}',
        f'{Back.BLACK}{Fore.WHITE}│    {color}{suit}    {Fore.WHITE}│{Style.RESET_ALL}',
        f'{Back.BLACK}{Fore.WHITE}│         │{Style.RESET_ALL}',
        f'{Back.BLACK}{Fore.WHITE}│{color}{value:>9}{Fore.WHITE}│{Style.RESET_ALL}',
        f'{Back.BLACK}{Fore.WHITE}╰─────────╯{Style.RESET_ALL}'
    ]
    return card

def dealer_turn(dealer_hand):
    """Handle dealer's turn according to standard Blackjack rules."""
    while calculate_score(dealer_hand) < 17:  # Dealer must hit on 16 and below
        dealer_hand.append(deck.deal())
        play_sound("sounds/deal.wav")
        display_hands(dealer_hand, dealer_hand, hidden=False)
        time.sleep(1)  # Add a slight delay for dramatic effect

def determine_winner(player_hand, dealer_hand, bet, balance):
    """Determine the winner and update balance accordingly."""
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)
    
    # Handle blackjack cases
    player_blackjack = len(player_hand) == 2 and player_score == 21
    dealer_blackjack = len(dealer_hand) == 2 and dealer_score == 21
    
    if player_blackjack and not dealer_blackjack:
        winnings = int(bet * 1.5)  # Blackjack pays 3:2
        balance += winnings
        display_result("Blackjack! You win!", winnings, balance)
        stats.update("win", winnings)
    elif dealer_blackjack and not player_blackjack:
        balance -= bet
        display_result("Dealer has Blackjack! You lose!", -bet, balance)
        stats.update("loss", -bet)
    elif player_blackjack and dealer_blackjack:
        display_result("Both have Blackjack! Push!", 0, balance)
        stats.update("push", 0)
    # Handle regular cases
    elif dealer_score > 21:
        balance += bet
        display_result("Dealer busts! You win!", bet, balance)
        stats.update("win", bet)
    elif player_score > dealer_score:
        balance += bet
        display_result("You win!", bet, balance)
        stats.update("win", bet)
    elif dealer_score > player_score:
        balance -= bet
        display_result("Dealer wins!", -bet, balance)
        stats.update("loss", -bet)
    else:
        display_result("Push!", 0, balance)
        stats.update("push", 0)
    
    return balance

def main():
    global deck, stats, balance
    parser = argparse.ArgumentParser(description='Terminal Blackjack Game')
    parser.add_argument('--no-sound', action='store_true', help='Disable sound effects')
    global args
    args = parser.parse_args()

    # Initialize pygame mixer for sound
    if not args.no_sound:
        pygame.mixer.init()

    # Clear screen and show initial display
    clear_screen()
    print(Back.BLACK, end='')  # Ensure black background persists
    display_title()

    # Load or create new game (only at the very start)
    if not os.path.exists("blackjack_save.json"):
        balance = 100
        stats = Stats()
    else:
        balance, stats = load_game()

    print(f"{Back.BLACK}    {Fore.CYAN}Welcome to Blackjack!{Style.RESET_ALL}{Back.BLACK}")
    print(f"{Back.BLACK}    Type ? for help and commands{Style.RESET_ALL}{Back.BLACK}")

    while True:  # Changed to infinite loop since we'll always reset
        if balance <= 0:  # Check at the start of each round
            balance = 100  # Reset to starting balance
            print(f"{Back.BLACK}{Fore.RED}\n    You're out of money!{Style.RESET_ALL}{Back.BLACK}")
            print(f"{Back.BLACK}{Fore.GREEN}    Balance reset to $100{Style.RESET_ALL}{Back.BLACK}")
            input(f"{Back.BLACK}    Press Enter to continue...{Style.RESET_ALL}{Back.BLACK}")
            clear_screen()
            display_title()

        # Get bet
        bet = display_bet_prompt(balance)
        if not bet:
            clear_screen()
            display_title()
            continue

        # Initialize deck if needed
        if 'deck' not in globals():
            deck = Deck()

        # Deal initial cards
        player_hand = [deck.deal(), deck.deal()]
        dealer_hand = [deck.deal(), deck.deal()]
        
        display_hands(player_hand, dealer_hand)
        
        # Check for dealer blackjack
        if calculate_score(dealer_hand[:1]) == 11:  # Dealer showing Ace
            print(f"\n{Back.BLACK}    {Fore.CYAN}Dealer is showing an Ace. Would you like insurance? (y/n){Style.RESET_ALL}{Back.BLACK}")
            if input().lower() == 'y' and balance >= bet/2:
                insurance = bet/2
                if calculate_score(dealer_hand) == 21:
                    print(f"{Back.BLACK}{Fore.GREEN}    Dealer has Blackjack! Insurance pays 2:1{Style.RESET_ALL}{Back.BLACK}")
                    balance += insurance
                    continue
                else:
                    print(f"{Back.BLACK}{Fore.RED}    Dealer does not have Blackjack. Insurance lost.{Style.RESET_ALL}{Back.BLACK}")
                    balance -= insurance

        action, bet = player_turn(player_hand, dealer_hand, bet, balance)
        if action == 'quit':
            save_game(balance, stats)
            print(f"{Back.BLACK}{Fore.GREEN}    Thanks for playing!{Style.RESET_ALL}{Back.BLACK}")
            break
        elif action == 'bust':
            balance -= bet
            display_result("Bust! You lose!", -bet, balance)
            stats.update("loss", -bet)
            continue
        else:
            dealer_turn(dealer_hand)
            display_hands(player_hand, dealer_hand, hidden=False)
            balance = determine_winner(player_hand, dealer_hand, bet, balance)

        display_next_move_options()
        choice = input("    Choose an option (1-4): ")
        if choice == "2":
            save_game(balance, stats)
            print(f"{Back.BLACK}{Fore.GREEN}    Thanks for playing!{Style.RESET_ALL}{Back.BLACK}")
            break
        elif choice == "3":
            stats.display(current_balance=balance)
            input(f"\n{Back.BLACK}Press Enter to continue...{Style.RESET_ALL}{Back.BLACK}")
        elif choice == "4":
            balance = 100
            print(f"{Back.BLACK}{Fore.GREEN}    Balance reset to $100{Style.RESET_ALL}{Back.BLACK}")
            input(f"{Back.BLACK}    Press Enter to continue...{Style.RESET_ALL}{Back.BLACK}")
        clear_screen()
        display_title()

 # Runs the main() function
if __name__ == "__main__":
    main()
