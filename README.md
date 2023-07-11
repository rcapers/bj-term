# Terminal Blackjack
Developed by Ryan Capers, as a way to learn Python (just because)

This is a simple command-line implementation of the classic Blackjack game, written in Python 3. To run the game, follow the instructions below:

## Installation

- Clone or download the repository to your local machine
- Install pygame library by running `pip install pygame`

## Usage

- Open a terminal or command prompt and navigate to the directory where you cloned or downloaded the repository
- Run the following command to start the game: `python blackjack.py` 
- For a list of available options, use command `python blackjack.py --help`
- Follow the on-screen instructions to play the game

## Latest Functionality and Features
- Added support for flag parameters in bj-term.py to customize the game experience

## Example Screenshot ##
<img src="https://user-images.githubusercontent.com/2326739/232260821-4d5d10e0-6ab2-4fce-ac3a-41fc07db7284.png" alt="image" width="400"/>


## Game Rules

The game follows the standard rules of Blackjack:

- The player's goal is to get closer to 21 points than the dealer without going over 21
- Numbered cards are worth their face value, face cards (Jacks, Queens, and Kings) are worth 10, and Aces are worth 1 or 11
- The player starts with two cards and can choose to "hit" to receive additional cards or "stand" to keep their current hand
- The dealer also starts with two cards, but only one card is visible to the player until the end of the game
- If the player's hand exceeds 21 points, they "bust" and lose the game
- If the dealer's hand exceeds 21 points, they "bust" and the player wins the game
- If neither player busts, the one with the highest hand value below 22 wins the game

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
