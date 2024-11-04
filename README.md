# Linked List Snake Game

A classic Snake game implemented in Python using the Pygame library. This game leverages a linked list structure to manage the snake's body, and includes various types of food, trash, and obstacles to create a unique gameplay experience.

## Features

- **Linked List-Based Snake**: Each segment of the snake is represented as a node in a linked list.
- **Food and Trash Items**: The snake grows when it eats food, and its length reduces when it eats trash.
- **Obstacles**: Avoid obstacles that appear on the grid, adding a challenge to navigation.
- **Score Tracking**: Tracks the player's score with visual feedback for high and low scores.
- **Game Restart with Space Bar**: On the game-over screen, press the space bar to start a new game.

## Preview
![Game Start Screen](path/to/your/image2.png)
![Game Play Preview](path/to/your/image1.png)
![Game Over Screen](path/to/your/image2.png)

> **Note**: Replace `path/to/your/image1.png` and `path/to/your/image2.png` with the relative path to your images within the repository.

## Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/snake-linkedlist-game.git
   cd snake-linkedlist-game

2. **Install required dependencies**:
   ```bash
   pip install pygame

3. **Place game assets: Ensure you have the following assets organized in the specified folder structure**:
  - Assets/judul.png
  - Fruit images in Assets/buah/: apple.png, banana.png, watermelon.png
  - Trash images in Assets/sampah/: dirty.png, kulitPisang.png, appleSisa.png, trash.png
  - Obstacle images in Assets/obstacle/: stone1.png through stone9.png
  - Sounds in Sound/: crunch.wav, game-over-arcade.mp3

4. **Run the game**:
   ```bash
   python snake-linkedlist.py

## How to Play

1. **Controls**:
  - Arrow keys to move:
        - Up Arrow: Move up
        - Down Arrow: Move down
        - Left Arrow: Move left
        - Right Arrow: Move right

2. **Objective**:
   Eat food items to grow longer and increase your score. Avoid obstacles and trash.

3. **Game Over Conditions**:
   - Collision with obstacles or the snake itself.
   - The score reaches -1 due to eating trash.

4. **Restarting the Game**:
   On the game-over screen, press the space bar to restart.
