# Terminal Blackjack
A stylish command-line implementation of Blackjack with a modern dark theme interface, written in Python 3.

## Features

- 🎨 Modern dark theme interface with colored cards and text
- 🎮 Intuitive gameplay with clear visual feedback
- 💰 Persistent game statistics and balance tracking
- 🎵 Sound effects for enhanced gaming experience
- 📊 Detailed statistics tracking (wins, losses, streaks)
- 💾 Auto-save functionality
- 🎲 Professional card visuals with suit symbols
- 🏆 Achievement system with unlockable rewards
- 🧠 Strategic gameplay assistance
- 📈 Card counting and streak tracking

## Achievement System

Unlock special achievements as you play:
- **High Roller**: Win with a bet of $500 or more
- **Blackjack Master**: Get 5 natural blackjacks
- **Comeback King**: Win after being down to less than 20% of starting balance
- **Lucky Seven**: Win 7 hands in a row
- **Card Counter**: Win 10 hands in one session

## Strategy Features

- Basic strategy hints for optimal play
- Card counting status indicator
- Hot streak tracking
- Progressive betting suggestions

## Installation

1. Clone or download the repository:
```bash
git clone https://github.com/rcapers/bj-term.git
cd bj-term
```

2. Set up a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the game with default settings:
```bash
python bj-term.py
```

Available options:
```bash
python bj-term.py --help     # Show all available options
python bj-term.py --no-sound # Run without sound effects
python bj-term.py --no-hints # Disable strategy hints
```

## Game Controls

- `H` - Hit (draw another card)
- `S` - Stand (keep current hand)
- `D` - Double down (double bet & draw one card)
- `Q` - Quit (save and exit)
- `?` - Help (show game rules)

## Game Rules

Standard Blackjack rules apply:
- Beat the dealer's hand without going over 21
- Card values:
  - Number cards (2-10): Face value
  - Face cards (J, Q, K): 10
  - Aces: 1 or 11
- Dealer must hit on 16 and stand on 17
- Blackjack pays 3:2

## Statistics Tracking

The game tracks:
- Games played
- Wins/Losses/Pushes
- Biggest wins and losses
- Current and best winning streaks
- Hot streak status
- Card counting progress
- Achievement progress

## Example Screenshot

<img width="579" alt="image" src="https://github.com/user-attachments/assets/07740eab-dcf9-4ba3-80ad-597d25e4383e">

## Development

Developed by Ryan Capers as a Python learning project. Recent improvements include:
- Achievement system
- Strategy assistance
- Enhanced statistics tracking
- Card counting features
- Progressive betting system

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
