# Super Mario Game in Python

A classic Super Mario-style platformer game built with Python and Pygame.

## Features

### Mario Character
- **Movement**: Left/Right arrow keys or A/D keys
- **Jumping**: Spacebar, Up arrow, or W key  
- **Physics**: Realistic gravity and jumping mechanics
- **Power-ups**: Small Mario, Big Mario, Fire Mario (visual indicators)
- **Lives System**: Start with 3 lives
- **Visual Design**: Mario with red hat, blue overalls, and mustache

### Game Elements
- **Platforms**: Multiple jumping platforms at different heights
- **Enemies**: Goomba enemies that patrol platforms and ground
- **Coins**: Spinning collectible coins worth 200 points each
- **Background**: Sky with clouds and ground
- **Collision Detection**: Mario vs platforms, enemies, and coins

### Gameplay Mechanics
- **Enemy Interaction**: 
  - Jump on Goombas to defeat them (+100 points)
  - Getting hit by Goombas reduces power-up or life
- **Coin Collection**: Collect spinning coins for points
- **Death Conditions**: Falling off screen or losing all lives
- **Scoring System**: Points for defeating enemies and collecting coins
- **Game Over/Restart**: Press R to restart when game over

### Controls
- **Movement**: 
  - Left Arrow / A: Move left
  - Right Arrow / D: Move right
  - Up Arrow / W / Spacebar: Jump
- **Game Controls**:
  - R: Restart game (when game over)
  - ESC: Quit game

## Installation

1. **Install Python** (3.7 or higher)

2. **Install Pygame**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or manually:
   ```bash
   pip install pygame==2.5.2
   ```

## How to Run

### Quick Start (Recommended)
```bash
python3 launcher.py
```
The launcher will check for pygame and provide installation instructions if needed.

### Direct Run (if pygame is installed)
```bash
python3 mario_game.py
```

### View Demo (no pygame required)
```bash
python3 demo.py
```

### Installation Troubleshooting

If you encounter installation issues:

1. **Virtual Environment Method** (safest):
   ```bash
   python3 -m venv mario_env
   source mario_env/bin/activate  # On Windows: mario_env\Scripts\activate
   pip install pygame==2.5.2
   python3 mario_game.py
   ```

2. **User Installation**:
   ```bash
   pip install --user pygame==2.5.2
   python3 mario_game.py
   ```

3. **System Package Manager** (Ubuntu/Debian):
   ```bash
   sudo apt install python3-pygame
   python3 mario_game.py
   ```

## Game Objects

### Mario
- Red/Blue character with hat and overalls
- Responsive controls with momentum
- Power-up system (Small → Big → Fire)
- Lives and scoring system

### Platforms
- Brown rectangular platforms
- Solid collision detection
- Multiple platform levels for jumping

### Goombas (Enemies)
- Brown mushroom-like enemies
- Patrol behavior with direction changes
- Can be defeated by jumping on them
- Deal damage to Mario on contact

### Coins
- Yellow spinning coins
- Rotate animation for visual appeal
- Disappear when collected
- Award points to player

## Technical Details

- **Resolution**: 1200x800 pixels
- **Frame Rate**: 60 FPS
- **Physics**: Custom gravity and collision system
- **Graphics**: Pure Pygame primitives (no external sprites needed)
- **Architecture**: Object-oriented design with separate classes

## Game Mechanics

1. **Physics**: Gravity affects Mario's movement, realistic jumping
2. **Collision Detection**: Precise rectangle-based collision system
3. **Enemy AI**: Simple patrol patterns with boundary detection
4. **Scoring**: Points for defeating enemies and collecting items
5. **Lives System**: Traditional 3-life system with respawning

## Future Enhancements

Potential additions for expanded gameplay:
- Multiple levels
- Power-up items (mushrooms, fire flowers)
- More enemy types
- Sound effects and background music
- Sprite-based graphics
- Moving platforms
- Boss battles

## Requirements

- Python 3.7+
- Pygame 2.5.2
- Standard library modules (sys, math)

Enjoy playing this classic Super Mario-style platformer!