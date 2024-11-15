# Import necessary modules
import os
import sys
import random
from art import *
import argparse
import json
from datetime import datetime
from colorama import init, Fore, Back, Style

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
        
    def display(self):
        print(f"\n{Fore.CYAN}=== Statistics ==={Style.RESET_ALL}")
        print(f"Games Played: {self.games_played}")
        print(f"Wins: {Fore.GREEN}{self.wins}{Style.RESET_ALL}")
        print(f"Losses: {Fore.RED}{self.losses}{Style.RESET_ALL}")
        print(f"Pushes: {self.pushes}")
        print(f"Biggest Win: ${Fore.GREEN}{self.biggest_win}{Style.RESET_ALL}")
        print(f"Biggest Loss: ${Fore.RED}{self.biggest_loss}{Style.RESET_ALL}")
        print(f"Current Streak: {self.current_streak}")
        print(f"Best Streak: {self.best_streak}")

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
    print(f"{Fore.GREEN}Game saved successfully!{Style.RESET_ALL}")

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
        choice = input("Do you want to play again? (y/n): ").lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("Invalid input, please try again.")

# This function displays the hands of both the player and the dealer
def display_hands(player_hand, dealer_hand, hidden=True):
    score = calculate_score(player_hand)
    color = Fore.GREEN if score <= 21 else Fore.RED
    
    # Create decorative separator
    separator = f"{Back.BLACK}{Fore.CYAN}═══════════════════════════{Style.RESET_ALL}"
    
    # Display dealer's hand
    print(f"\n{separator}")
    dealer_header = f"{Back.BLACK}{Fore.CYAN}♠ ♥ DEALER'S HAND ♦ ♣{Style.RESET_ALL}"
    print(dealer_header)
    
    if hidden:
        print(f"{Back.BLACK}Total: {Fore.YELLOW}Hidden{Style.RESET_ALL}")
        print_cards([reg_card_visual(c) for c in dealer_hand[:1]] + [hidden_card()])
    else:
        dealer_score = calculate_score(dealer_hand)
        color_dealer = Fore.GREEN if dealer_score <= 21 else Fore.RED
        print(f"{Back.BLACK}Total: {color_dealer}{dealer_score}{Style.RESET_ALL}")
        print_cards([reg_card_visual(c) for c in dealer_hand])
    
    # Display player's hand
    print(f"\n{separator}")
    player_header = f"{Back.BLACK}{Fore.CYAN}♠ ♥ PLAYER'S HAND ♦ ♣{Style.RESET_ALL}"
    print(player_header)
    print(f"{Back.BLACK}Total: {color}{score}{Style.RESET_ALL}")
    print_cards([reg_card_visual(c) for c in player_hand])
    print(separator)

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
    title = f"""
{Back.BLACK}{Fore.YELLOW}
     {Fore.GREEN}♠ ♥{Style.RESET_ALL}{Back.BLACK}{Fore.YELLOW}  WELCOME TO BLACKJACK  {Fore.RED}♦ ♣{Style.RESET_ALL}
{Back.BLACK}{Fore.YELLOW}═══════════════════════════════════════════{Style.RESET_ALL}
"""
    print(title)

def display_stats(stats):
    stats_display = f"""{Back.BLACK}{Fore.CYAN}
════════════ STATISTICS ════════════

Games Played: {stats.games_played}
Wins:         {Fore.GREEN}{stats.wins}{Back.BLACK}{Fore.CYAN}
Losses:       {Fore.RED}{stats.losses}{Back.BLACK}{Fore.CYAN}
Pushes:       {stats.pushes}
Biggest Win:  ${Fore.GREEN}{stats.biggest_win}{Back.BLACK}{Fore.CYAN}
Biggest Loss: ${Fore.RED}{stats.biggest_loss}{Back.BLACK}{Fore.CYAN}
Current Streak: {stats.current_streak}
Best Streak:    {stats.best_streak}
{Fore.CYAN}═══════════════════════════════════{Style.RESET_ALL}"""
    print(stats_display)

def display_game_options():
    options = f"""{Back.BLACK}{Fore.YELLOW}
════════════ OPTIONS ════════════

(H) Hit     - Draw another card
(S) Stand   - Keep current hand
(D) Double  - Double bet & draw
(Q) Quit    - Save and exit
(?) Help    - Show game rules

═══════════════════════════════{Style.RESET_ALL}"""
    print(options)

def display_next_move_options():
    options = f"""{Back.BLACK}{Fore.YELLOW}
════════════ NEXT MOVE ════════════

1. Continue playing
2. Save and quit
3. View detailed statistics

═══════════════════════════════════{Style.RESET_ALL}"""
    print(options)

def display_game_over():
    message = f"""{Back.BLACK}{Fore.RED}
════════════════════════════
   You're out of money!
   Thanks for playing!
════════════════════════════{Style.RESET_ALL}"""
    print(message)

def display_bet_prompt(balance):
    print(f"\n{Back.BLACK}{Fore.CYAN}Current Balance: ${balance}{Style.RESET_ALL}")
    print(f"{Back.BLACK}{Fore.CYAN}═══════════════════════════{Style.RESET_ALL}")
    return get_bet(balance)

def display_result(message, balance_change, balance):
    result_color = Fore.GREEN if balance_change > 0 else Fore.RED if balance_change < 0 else Fore.YELLOW
    
    result = f"""
{Back.BLACK}{result_color}═══════════════════════════
{message}"""
    
    if balance_change != 0:
        result += f"\nBalance change: ${balance_change}"
    
    result += f"""
New balance: ${balance}
═══════════════════════════{Style.RESET_ALL}"""
    
    print(result)

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

def print_cards(cardlist):
    # Add spacing between cards
    spaced_cards = []
    for card_lines in zip(*cardlist):
        spaced_cards.append(f"{Back.BLACK}  {Style.RESET_ALL}".join(card_lines))
    
    # Print each line
    for line in spaced_cards:
        print(f"{Back.BLACK}{line}{Style.RESET_ALL}")

def get_bet(balance):
    while True:
        try:
            # Prompts the user to enter their bet
            bet = int(input(f"{Back.BLACK}{Fore.CYAN}Enter your bet (1-{balance}): {Style.RESET_ALL}"))
            # Checks if the bet is valid
            if bet > 0 and bet <= balance:
                return bet
            else:
                print("Invalid bet, please try again.")
        except ValueError:
            print("Invalid input, please enter a number.")

# Function to handle the player's turn
def player_turn(player_hand, dealer_hand, bet, balance):
    while True:
        choice = input(f"\n{Fore.YELLOW}(h)it, (s)tand, (d)ouble, (q)uit, or (?) help: {Style.RESET_ALL}").lower()
        if choice in ['h', 'hit']:
            player_hand.append(deck.deal())
            play_sound("sounds/deal.wav")
            display_hands(player_hand, dealer_hand)
            if calculate_score(player_hand) > 21:
                return False, bet
        elif choice in ['s', 'stand']:
            return True, bet
        elif choice in ['d', 'double'] and len(player_hand) == 2 and balance >= bet:
            bet *= 2
            player_hand.append(deck.deal())
            play_sound("sounds/deal.wav")
            display_hands(player_hand, dealer_hand)
            return calculate_score(player_hand) <= 21, bet
        elif choice in ['q', 'quit']:
            save_game(balance, stats)
            sys.exit()
        elif choice in ['?', 'help']:
            display_help()
        else:
            print(f"{Fore.RED}Invalid input, please try again.{Style.RESET_ALL}")

# Dealer's turn to draw cards until score is 17 or higher
def dealer_turn(dealer_hand):
    while calculate_score(dealer_hand) < 17:
        dealer_hand.append(deck.deal())
    return calculate_score(dealer_hand) <= 21

def determine_winner(player_hand, dealer_hand, bet, balance):
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)
    
    if player_score > 21:
        play_sound("sounds/lose.wav")
        display_result("You bust!", -bet, balance - bet)
        stats.update("loss", -bet)
        return balance - bet
    elif dealer_score > 21:
        play_sound("sounds/win.wav")
        display_result("Dealer busts! You win!", bet, balance + bet)
        stats.update("win", bet)
        return balance + bet
    elif player_score > dealer_score:
        play_sound("sounds/win.wav")
        display_result("You win!", bet, balance + bet)
        stats.update("win", bet)
        return balance + bet
    elif player_score < dealer_score:
        play_sound("sounds/lose.wav")
        display_result("You lose!", -bet, balance - bet)
        stats.update("loss", -bet)
        return balance - bet
    else:
        display_result("It's a tie!", 0, balance)
        play_sound("sounds/tie.wav")
        stats.update("push", 0)
        return balance

def display_help():
    print(f"\n{Fore.CYAN}=== Blackjack Commands ==={Style.RESET_ALL}")
    print("h or hit  - Draw another card")
    print("s or stand - Keep your current hand")
    print("d or double - Double your bet and receive one more card")
    print("p or split - Split a pair into two hands (if available)")
    print("i or insurance - Buy insurance against dealer blackjack (if available)")
    print("q or quit - Quit the game")
    print("? or help - Show this help menu")
    print("\nGame Rules:")
    print("1. Beat the dealer's hand without going over 21")
    print("2. Face cards are worth 10, Aces are worth 1 or 11")
    print("3. Dealer must hit on 16 and stand on 17")
    print("4. Blackjack pays 3:2")

def main():
    global deck, stats, balance
    parser = argparse.ArgumentParser(description='Terminal Blackjack Game')
    parser.add_argument('--no-sound', action='store_true', help='Disable sound effects')
    parser.add_argument('--new-game', action='store_true', help='Start a new game (ignore saved game)')
    global args
    args = parser.parse_args()
    
    clear_screen()
    display_title()
    
    deck = Deck()
    if args.new_game:
        balance = 100
        stats = Stats()
    else:
        balance, stats = load_game()
    
    print(f"\n{Fore.CYAN}Welcome to Blackjack!{Style.RESET_ALL}")
    print("Type ? for help and commands")
    
    while balance > 0:
        clear_screen()
        print(Back.BLACK, end='')  # Ensure black background persists
        display_title()
        display_stats(stats)
        
        if balance <= 0:
            display_game_over()
            return
        
        player_hand = [deck.deal(), deck.deal()]
        dealer_hand = [deck.deal(), deck.deal()]

        bet = display_bet_prompt(balance)
        play_sound("sounds/deal.wav")
        display_hands(player_hand, dealer_hand)
        display_game_options()

        # Check for dealer blackjack
        if calculate_score(dealer_hand[:1]) == 11:  # Dealer showing Ace
            print(f"\n{Fore.YELLOW}Dealer is showing an Ace. Would you like insurance? (y/n){Style.RESET_ALL}")
            if input().lower() == 'y' and balance >= bet/2:
                insurance = bet/2
                if calculate_score(dealer_hand) == 21:
                    print(f"{Fore.GREEN}Dealer has Blackjack! Insurance pays 2:1{Style.RESET_ALL}")
                    balance += insurance
                    continue
                else:
                    print(f"{Fore.RED}Dealer does not have Blackjack. Insurance lost.{Style.RESET_ALL}")
                    balance -= insurance

        success, bet = player_turn(player_hand, dealer_hand, bet, balance)
        if not success:
            balance = determine_winner(player_hand, dealer_hand, bet, balance)
        else:
            dealer_success = dealer_turn(dealer_hand)
            display_hands(player_hand, dealer_hand, hidden=False)
            balance = determine_winner(player_hand, dealer_hand, bet, balance)

        if balance > 0:
            display_next_move_options()
            choice = input("Choose an option (1-3): ")
            if choice == "2":
                save_game(balance, stats)
                print(f"{Fore.GREEN}Thanks for playing!{Style.RESET_ALL}")
                break
            elif choice == "3":
                display_stats(stats)
            clear_screen()
            display_title()
    else:
        display_game_over()

 # Runs the main() function
if __name__ == "__main__":
    main()
