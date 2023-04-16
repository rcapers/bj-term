import os
import sys
import random
from art import *

old_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')

import pygame
from pygame import mixer

sys.stdout = old_stdout

pygame.init()
mixer.init()

def play_sound(file):
    mixer.Sound(file).play()

def deal_card():
    suits = ["Spades", "Diamonds", "Hearts", "Clubs"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    card = {"suit": random.choice(suits), "value": random.choice(values)}
    return card

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

def play_again():
    while True:
        choice = input("Do you want to play again? (y/n): ").lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("Invalid input, please try again.")

def display_hands(player_hand, dealer_hand, hidden=True):
    print("\nPlayer's hand (Total: {}):".format(calculate_score(player_hand)))
    print_cards([reg_card_visual(c) for c in player_hand])
    
    print("\nDealer's hand:", end=" ")
    if hidden:
        print("(Total: Hidden)")
        print_cards([reg_card_visual(c) for c in dealer_hand[:1]])
        print("Hidden card")
    else:
        print("(Total: {})".format(calculate_score(dealer_hand)))
        print_cards([reg_card_visual(c) for c in dealer_hand])

def get_bet(balance):
    while True:
        try:
            bet = int(input(f"Enter your bet (1-{balance}): "))
            if bet > 0 and bet <= balance:
                return bet
            else:
                print("Invalid bet, please try again.")
        except ValueError:
            print("Invalid input, please enter a number.")

def player_turn(player_hand, dealer_hand):
    while True:
        choice = input("\nDo you want to (h)it or (s)tand? ").lower()
        if choice == "h":
            player_hand.append(deal_card())
            play_sound("sounds/deal.wav")
            display_hands(player_hand, dealer_hand)
            if calculate_score(player_hand) > 21:
                return False
        elif choice == "s":
            return True
        else:
            print("Invalid input, please try again.")

def dealer_turn(dealer_hand):
    while calculate_score(dealer_hand) < 17:
        dealer_hand.append(deal_card())
    return calculate_score(dealer_hand) <= 21

def display_result(message, balance_change, balance):
    print(f"{message} Your balance changed by {balance_change}. New balance: {balance}")

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
        return balance

def print_cards(cardlist):
    for card in zip(*cardlist):
        print(' '.join(card))

def reg_card_visual(card):
    suits = "Spades Diamonds Hearts Clubs".split()
    suit_symbols = ['♠','♦','♥','♣']
    suit_pairs = dict(zip(suits, suit_symbols))
    v = card['value']
    s = suit_pairs[card['suit']]
    visual = [
        '  ╔════════════╗',
        f'  ║ {v:<5}      ║',
        '  ║            ║',
        '  ║            ║',
        f'  ║     {s:^3}    ║',
        '  ║            ║',
        '  ║            ║',
        '  ║            ║',
        f'  ║      {v:>5} ║',
        '  ╚════════════╝'
    ]

    return visual

def main():
    print("Welcome to the Blackjack game!")
    balance = 100
    print(f"Your starting balance is: ${balance}")
    
    while balance > 0:
        player_hand = [deal_card(), deal_card()]
        dealer_hand = [deal_card(), deal_card()]

        play_sound("sounds/deal.wav")
        pygame.time.delay(300)  # Add delay to play the sound before displaying hands
        
        display_hands(player_hand, dealer_hand)
        bet = get_bet(balance)

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

if __name__ == "__main__":
    main()