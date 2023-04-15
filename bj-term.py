import random

def deal_card():
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    return random.choice(cards)

def calculate_score(hand):
    if sum(hand) > 21 and 11 in hand:
        hand.remove(11)
        hand.append(1)
    return sum(hand)

def print_banner(text, width=80):
    print("-" * width)
    print(text.center(width))
    print("-" * width)

def display_hands(player_hand, dealer_hand, hidden=True):
    print("\n" + "-" * 50)
    print("Your hand: ", end="")
    print(*player_hand, sep=", ", end=" | ")
    print(f"Score: {calculate_score(player_hand)}")

    print("Dealer's hand: ", end="")
    if hidden:
        print(dealer_hand[0], "X" * (len(dealer_hand) - 1), sep=", ", end=" | ")
    else:
        print(*dealer_hand, sep=", ", end=" | ")
    print("Score: ??" if hidden else f"Score: {calculate_score(dealer_hand)}")
    print("-" * 50 + "\n")

def get_bet(balance):
    bet = int(input(f"\nYour current balance is ${balance}. How much would you like to bet? $"))
    while bet > balance:
        bet = int(input("You don't have enough balance. Please enter a valid amount: $"))
    return bet

def player_turn(player_hand, dealer_hand):
    while True:
        action = input("Type 'hit' to draw another card or 'stand' to pass: ").lower()
        if action == 'hit':
            player_hand.append(deal_card())
            display_hands(player_hand, dealer_hand)
            if calculate_score(player_hand) > 21:
                return False
        elif action == 'stand':
            return True
        else:
            print("Invalid input. Please type 'hit' or 'stand'.")

def dealer_turn(dealer_hand):
    while calculate_score(dealer_hand) < 17:
        dealer_hand.append(deal_card())

def display_result(message, balance_change, balance):
    print(message)
    if balance_change != 0:
        print(f"{'+' if balance_change > 0 else ''}${balance_change}")
    print(f"New balance: ${balance}")
    print("-" * 30 + "\n")

def determine_winner(player_hand, dealer_hand, bet, balance):
    display_hands(player_hand, dealer_hand, hidden=False)

    if calculate_score(player_hand) > 21:
        print("Bust! You lose.")
        return balance - bet
    elif calculate_score(dealer_hand) > 21 or calculate_score(player_hand) > calculate_score(dealer_hand):
        print("You win!")
        return balance + bet
    elif calculate_score(player_hand) < calculate_score(dealer_hand):
        print("You lose!")
        return balance - bet
    else:
        print("It's a draw!")
        return balance

def play_blackjack(balance):
    print_banner("Let's play!")

    player_hand = [deal_card(), deal_card()]
    dealer_hand = [deal_card(), deal_card()]

    display_hands(player_hand, dealer_hand)
    bet = get_bet(balance)

    if calculate_score(player_hand) == 21:
        print("Blackjack! You win!")
        balance += bet * 1.5
        display_result("Blackjack!", bet * 1.5, balance)
        return balance

    game_over = not player_turn(player_hand, dealer_hand)

    if game_over:
        display_result("Bust! You lose.", -bet, balance - bet)
        return balance - bet

    dealer_turn(dealer_hand)
    new_balance = determine_winner(player_hand, dealer_hand, bet, balance)
    display_result("You win!" if new_balance > balance else "You lose!" if new_balance < balance else "It's a draw!", new_balance - balance, new_balance)
    return new_balance

def blackjack():
    print_banner("Welcome to Blackjack!")
    starting_balance = 100
    balance = starting_balance

    while True:
        balance = play_blackjack(balance)
        play_again = input("\nDo you want to play again? Type 'yes' or 'no': ").lower()
        if play_again != 'yes':
            break

    print_banner("Thanks for playing!")

blackjack()

