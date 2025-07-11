#!/usr/bin/env python3
"""
Super Mario Game Launcher
This script checks for pygame availability and launches the game or provides installation instructions.
"""

import sys
import subprocess

def check_pygame():
    """Check if pygame is available."""
    try:
        import pygame
        return True, pygame.version.ver
    except ImportError:
        return False, None

def install_pygame():
    """Attempt to install pygame using different methods."""
    print("Attempting to install pygame...")
    
    # Try pip install
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame==2.5.2"])
        print("Successfully installed pygame using pip!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Failed to install pygame using pip.")
    
    # Try with --user flag
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "pygame==2.5.2"])
        print("Successfully installed pygame using pip --user!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Failed to install pygame using pip --user.")
    
    return False

def main():
    print("=" * 60)
    print("🍄 SUPER MARIO GAME LAUNCHER 🍄")
    print("=" * 60)
    
    # Check if pygame is available
    pygame_available, pygame_version = check_pygame()
    
    if pygame_available:
        print(f"✅ Pygame {pygame_version} is available!")
        print("🚀 Starting Super Mario Game...")
        print("\nControls:")
        print("  • Arrow Keys or WASD: Move Mario")
        print("  • Spacebar: Jump")
        print("  • R: Restart (when game over)")
        print("  • ESC: Quit game")
        print("\nGame Features:")
        print("  • Jump on Goombas to defeat them (+100 points)")
        print("  • Collect spinning coins (+200 points)")
        print("  • Avoid falling off platforms!")
        print("\n" + "=" * 60)
        
        # Import and run the game
        try:
            from mario_game import Game
            game = Game()
            game.run()
        except Exception as e:
            print(f"❌ Error running the game: {e}")
            print("Make sure mario_game.py is in the same directory.")
    else:
        print("❌ Pygame is not available!")
        print("\nTo install pygame, try one of these methods:")
        print("\n1. Using pip (recommended):")
        print("   pip install pygame==2.5.2")
        print("\n2. Using pip with --user flag:")
        print("   pip install --user pygame==2.5.2")
        print("\n3. Using system package manager (Ubuntu/Debian):")
        print("   sudo apt install python3-pygame")
        print("\n4. Using conda:")
        print("   conda install pygame")
        print("\n5. In a virtual environment:")
        print("   python -m venv mario_env")
        print("   source mario_env/bin/activate  # On Windows: mario_env\\Scripts\\activate")
        print("   pip install pygame==2.5.2")
        
        # Offer to try automatic installation
        try:
            choice = input("\nWould you like me to try installing pygame automatically? (y/n): ").lower().strip()
            if choice == 'y' or choice == 'yes':
                if install_pygame():
                    print("\n🎉 Installation successful! Please run the launcher again.")
                else:
                    print("\n❌ Automatic installation failed. Please try manual installation.")
            else:
                print("Please install pygame manually and run the launcher again.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
        except:
            print("Please install pygame manually and run the launcher again.")

if __name__ == "__main__":
    main()