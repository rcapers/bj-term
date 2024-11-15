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
python bj-term.py --help  # Show all available options
python bj-term.py --no-sound  # Run without sound effects
python bj-term.py --new-game  # Start a fresh game (ignore saved data)
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
- Current balance

## Example Screenshot


<img width="579" alt="image" src="https://github.com/user-attachments/assets/07740eab-dcf9-4ba3-80ad-597d25e4383e">


## Development

Developed by Ryan Capers as a Python learning project. Recent improvements include:
- Modern dark theme interface
- Enhanced visual card representations
- Improved statistics display
- Consistent UI styling
- Better error handling

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
