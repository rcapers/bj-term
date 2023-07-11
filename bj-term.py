# Import necessary modules
import os
import sys
import random
from art import *
import argparse

parser = argparse.ArgumentParser(description='-- BlackJack Help Menu -----------------------')
parser.add_argument('-help', action='store_true', help='list all command line arguments')
# add other arguments here
args = parser.parse_args()

if args.help:
    parser.print_help()
    
# Suppress pygame welcome message
old_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')

import pygame
from pygame import mixer

sys.stdout = old_stdout

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
    # Prints the player's hand and its total score
    print("\nPlayer's hand (Total: {}):".format(calculate_score(player_hand)))
    print_cards([reg_card_visual(c) for c in player_hand])
    
    # Prints the dealer's hand and its total score
    print("\nDealer's hand:", end=" ")
    if hidden:
        print("(Total: Hidden)")
        print_cards([reg_card_visual(c) for c in dealer_hand[:1]])
        print("Hidden card")
    else:
        print("(Total: {})".format(calculate_score(dealer_hand)))
        print_cards([reg_card_visual(c) for c in dealer_hand])

# This function gets the bet from the player
def get_bet(balance):
    while True:
        try:
            # Prompts the user to enter their bet
            bet = int(input(f"Enter your bet (1-{balance}): "))
            # Checks if the bet is valid
            if bet > 0 and bet <= balance:
                return bet
            else:
                print("Invalid bet, please try again.")
        except ValueError:
            print("Invalid input, please enter a number.")

# This function handles the player's turn
def player_turn(player_hand, dealer_hand):
    while True:
        # Prompts the user to hit or stand
        choice = input("\nDo you want to (h)it or (s)tand? ").lower()
        if choice == "h":
            # Deals a card to the player
            player_hand.append(deal_card())
            play_sound("sounds/deal.wav")
            display_hands(player_hand, dealer_hand)
            # Checks if the player has gone over 21
            if calculate_score(player_hand) > 21:
                return False
        elif choice == "s":
            return True
        else:
            print("Invalid input, please try again.")
# Dealer's turn to draw cards until score is 17 or higher
def dealer_turn(dealer_hand):
    while calculate_score(dealer_hand) < 17:
        dealer_hand.append(deal_card())
    return calculate_score(dealer_hand) <= 21

def display_result(message, balance_change, balance):
    # Prints out the result of the game
    print(f"{message} Your balance changed by {balance_change}. New balance: {balance}")

# Determines the winner of the game based on scores
def determine_winner(player_hand, dealer_hand, bet, balance):
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    if player_score > 21:
        play_sound("sounds/lose.wav")
        display_result("You bust!", -bet, balance - bet)
        return balance - bet
    elif dealer_score > 21:
        play_sound("sounds/win.wav")
        display_result("Dealer busts! You win!", bet, balance + bet)
        return balance + bet
    elif player_score > dealer_score:
        play_sound("sounds/win.wav")
        display_result("You win!", bet, balance + bet)
        return balance + bet
    elif player_score < dealer_score:
        play_sound("sounds/lose.wav")
        display_result("You lose!", -bet, balance - bet)
        return balance
    else:
        display_result("It's a tie!", 0, balance)
        play_sound("sounds/tie.wav")
        return balance

# Prints out the cards in a visual format
def print_cards(cardlist):
    for card in zip(*cardlist):
        print(' '.join(card))

# Creates a visual representation of the card
def reg_card_visual(card):
    suits = "Spades Diamonds Hearts Clubs".split()
    suit_symbols = ['♠','♦','♥','♣']
    suit_pairs = dict(zip(suits, suit_symbols))
    v = card['value']
    s = suit_pairs[card['suit']]
    visual = [
        '  ╔═══════╗',
        f'  ║ {v:<5} ║',
        '  ║       ║',
        f'  ║{s:^7}║',
        '  ║       ║',
        f'  ║ {v:>5} ║',
        '  ╚═══════╝'
    ]

    return visual
# Main function that runs the game
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-sound', action='store_true', help='Disable sound effects')
    global args
    args = parser.parse_args()
    print("Welcome to the Blackjack game!")
    balance = 100
    print(f"Your starting balance is: ${balance}")
    
    while balance > 0:
        player_hand = [deal_card(), deal_card()]
        dealer_hand = [deal_card(), deal_card()]

        bet = get_bet(balance)

        play_sound("sounds/deal.wav")
        display_hands(player_hand, dealer_hand)

        if not player_turn(player_hand, dealer_hand):
            balance = determine_winner(player_hand, dealer_hand, bet, balance)
        else:
            if not dealer_turn(dealer_hand):
                display_hands(player_hand, dealer_hand, hidden=False)
                balance = determine_winner(player_hand, dealer_hand, bet, balance)
            else:
                display_hands(player_hand, dealer_hand, hidden=False)
                balance = determine_winner(player_hand, dealer_hand, bet, balance)

        if balance > 0:
            if play_again():
                print("Starting a new game...")
            else:
                print("Thanks for playing!")
                break
    else:
        print("You're out of money. Thanks for playing!")

 # Runs the main() function
if __name__ == "__main__":
    main()
