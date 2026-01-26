# 🎮 Super Tic Tac Toe

<div align="center">

![Game Banner](path/to/banner-image.png)
<!-- PLACEHOLDER: Add a banner image showing the game title and main board -->

**A modern, strategic twist on the classic game - built with Python and PyQt6**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)](https://pypi.org/project/PyQt6/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

[Features](#features) • [Installation](#installation) • [How to Play](#how-to-play) • [Screenshots](#screenshots) • [Contributing](#contributing)

</div>

---

## 📖 About

Super Tic Tac Toe takes the traditional 3×3 grid to an entirely new level. Instead of one board, you're playing on **nine interconnected boards simultaneously**. Each move determines where your opponent must play next, creating a dynamic, strategic experience that's easy to learn but challenging to master.

![Gameplay Demo](path/to/gameplay-demo.gif)
<!-- PLACEHOLDER: Add an animated GIF showing actual gameplay -->

---

## ✨ Features

### 🎯 Game Modes
- **Player vs Player** - Challenge a friend locally
- **Player vs AI** - Test your skills against the computer
  - 🟢 **Easy** - Perfect for learning the ropes
  - 🟡 **Medium** - Strategic blocking and winning moves
  - 🔴 **Hard** - Board-level strategic thinking

### 🎨 Modern Interface
- Clean, minimalist design with smooth animations
- Color-coded players (Red for X, Blue for O)
- Visual feedback for active boards and valid moves
- Hover effects to guide your gameplay
- Responsive layout that scales beautifully

### 🏆 Gameplay Features
- Dynamic board highlighting shows where you can play
- Instant win detection for both mini-boards and overall game
- Draw detection when boards fill up
- One-click game reset
- Comprehensive instructions built-in

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/super-tictactoe.git
   cd super-tictactoe
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**
   ```bash
   python main.py
   ```

---

## 🎮 How to Play

### The Basics

Super Tic Tac Toe consists of a 3×3 grid of **mini-boards**, each containing another 3×3 grid of squares.

![Board Layout](path/to/board-layout-annotated.png)
<!-- PLACEHOLDER: Add an annotated image showing the 9 mini-boards and overall structure -->

### Rules

1. **Starting the Game**
   - X (Red) always goes first
   - The first player can choose any square on any mini-board

2. **Making Moves**
   - Click on an empty square to place your mark
   - The position of your move determines which mini-board your opponent must play in next
   - Example: If you play in the top-right square of a mini-board, your opponent must play in the top-right mini-board

   ![Move Example](path/to/move-example.png)
   <!-- PLACEHOLDER: Add a visual showing how move position determines next board -->

3. **Winning Mini-Boards**
   - Get three in a row (horizontal, vertical, or diagonal) to claim a mini-board
   - Won mini-boards are marked with a large X or O
   
   ![Mini-Board Win](path/to/mini-board-win.png)
   <!-- PLACEHOLDER: Add image showing a won mini-board with overlay -->

4. **Free Choice**
   - If you're sent to a mini-board that's already won or full, you can play anywhere

5. **Winning the Game**
   - Win three mini-boards in a row (horizontal, vertical, or diagonal) to win the overall game!
   
   ![Overall Win](path/to/overall-win.png)
   <!-- PLACEHOLDER: Add image showing three mini-boards won in a row -->

6. **Draw**
   - If all mini-boards are won or filled without anyone getting three in a row, the game is a draw

### Visual Cues

- 🟨 **Yellow Border** - Indicates the active mini-board where you must play
- **Hover Effect** - Shows which mini-boards you can play in
- **Large Overlays** - Show which player won each mini-board

---

## 📸 Screenshots

<div align="center">

### Main Menu
![Main Menu](path/to/screenshot-menu.png)
<!-- PLACEHOLDER: Add screenshot of the main menu with mode selection -->

### Gameplay
![Active Game](path/to/screenshot-gameplay.png)
<!-- PLACEHOLDER: Add screenshot of an active game in progress -->

### Victory Screen
![Victory Dialog](path/to/screenshot-victory.png)
<!-- PLACEHOLDER: Add screenshot of the victory popup dialog -->

### Instructions
![Instructions](path/to/screenshot-instructions.png)
<!-- PLACEHOLDER: Add screenshot of the instructions window -->

</div>

---

## 🛠️ Technical Details

### Built With
- **Python 3.8+** - Core programming language
- **PyQt6** - Modern GUI framework
- **Qt Designer** - UI styling and theming

### Project Structure
```
super-tictactoe/
├── main.py                 # Entry point
├── windows/
│   ├── menu_window.py     # Main menu interface
│   ├── main_window.py     # Game window
│   ├── instructions_window.py
│   └── game_components/
│       ├── board.py       # Main game board logic
│       ├── mini_game.py   # Individual mini-board
│       ├── board_square.py
│       ├── game_result.py # Victory dialog
│       └── overlays/
├── styling/
│   ├── styles.qss         # Qt stylesheet
│   └── colours.py         # Color definitions
└── requirements.txt
```

### AI Implementation
The AI uses different strategies based on difficulty:
- **Easy**: Random move selection from valid moves
- **Medium**: Tactical play - attempts to win mini-boards and blocks opponent wins
- **Hard**: Strategic play - considers overall board state and thinks multiple moves ahead

---

## 🎯 Strategy Tips

1. **Control the Center** - The center mini-board gives you the most flexibility for your next move
2. **Think Ahead** - Consider not just winning the current mini-board, but where your move sends your opponent
3. **Force Bad Positions** - Send your opponent to mini-boards that are already won or give them limited options
4. **Balance Offense and Defense** - Don't focus solely on winning mini-boards; block your opponent too
5. **Avoid Giving Free Choice** - Try not to send your opponent to won/full boards, as it gives them free reign

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contributions
- [ ] Online multiplayer functionality
- [ ] Move history and undo feature
- [ ] Game statistics and win tracking
- [ ] Custom themes and color schemes
- [ ] Sound effects and music
- [ ] Tournament mode
- [ ] Replay saved games

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👏 Acknowledgments

- Inspired by the classic Super Tic Tac Toe variant
- Built as a project for ComSSA
- Special thanks to the PyQt6 community for excellent documentation

---

## 📧 Contact

**Your Name** - [@yourhandle](https://twitter.com/yourhandle)

Project Link: [https://github.com/yourusername/super-tictactoe](https://github.com/yourusername/super-tictactoe)

---

<div align="center">

**Enjoy the game? Give it a ⭐️ on GitHub!**

Made with ❤️ and Python

</div>