MAZE GAME

WHAT IT DOES:
This program will generate a random "perfect maze" with only one solution and only one path between any given two points on the "grid" of the maze. You pick a maze size between 3x3 and 100x100, click generate, and then navigate using the arrow keys. You always start in the top left and finish in the bottom right. Your movement will leave a trail behind you, but can be backtracked.

REQUIREMENTS:

Python 3 (I used Python 3.8.8)

Pygame

HOW TO RUN:
1) Put all program files in the same folder
2) Open Command Prompt in that folder
3) Run the main program with "python main.py"

(If this doesn't work, make sure pygame is installed with "pip install pygame")

HOW TO USE:
1) Click the size input box at the top left of the window, you'll see a blinking cursor to show that it's selected
2) Type an integer maze size from 3 to 100
3) Click the generate button
4) Use the arrow keys to move through the maze
5) Navigate to the bottom right cell to win

CONTROLS:
Mouse and keyboard

NOTES:
Maze size will scale to fit in the window no matter what size you select.

Each time you click generate, you get a new randomly generated maze, even if you don't select a new size.

If you think it's impossible, type "solve" and you'll be shown the solution!
