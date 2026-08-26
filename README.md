# pacman_r
Pac-Man (Python + Pygame)

A classic Pac-Man clone built from scratch in Python using Pygame — grid-based maze movement, four ghosts with distinct AI behaviors, power pellets, and a score/game-over loop.

Features
20x20 tile maze rendered from a 2D grid (1 = wall, 2 = pellet, 3 = power pellet, 0/2-eaten = empty)
Animated Pac-Man — 4-frame mouth-chomp animation, image flipped/rotated to match current facing direction
Four ghosts (Red, Pink, Blue, Orange), each with its own sprite and staggered release timer, so they don't all swarm the player at once
Chase AI driven by Manhattan distance (see below)
Power-pellet / frightened mode — eating a power pellet (3) freezes ghost sprites, flips their pathfinding to "flee," and lets the player eat them for +200 points each; eaten ghosts respawn at their home tile
Score tracking and a Game Over / Play Again screen that resets the grid, player, and ghosts
Controls

Arrow keys — move Pac-Man up / down / left / right.

Requirements
pip install pygame

Place these image assets in the same folder as the script: red.png, pink.png, blue.png, orange.png, 1.png, 2.png, 3.png, 4.png, powerup.png

Run with:

python pacman.py
Ghost AI — how it works

Ghosts only make a decision when they're sitting exactly on a grid intersection (x % cellsize == 0 and y % cellsize == 0). Between intersections they just keep moving in their current direction at 2px/frame, which is what gives the smooth (non-teleporting) movement instead of jumping cell-to-cell.

At each intersection, a ghost:

Looks at every neighboring cell that isn't a wall.
Scores each one using Manhattan distance (|Δx| + |Δy|) to a target tile.
Picks the direction with the best score.

There are two modes, using the same logic with the comparison flipped:

Chase (move1) — minimizes distance to the target, so the ghost heads toward it.
Frightened / scatter (scatter) — maximizes distance to the target, so the ghost flees instead.

Each ghost also chases a slightly different target offset rather than the player's exact tile (e.g. a few tiles ahead of or behind Pac-Man). This is the same idea as the original arcade game's Blinky/Pinky/Inky/Clyde personalities — it spreads the ghosts out instead of having all four dogpile the player from the same direction.

Problem faced: ghosts getting stuck oscillating

The bug: with a pure "always pick the direction that minimizes Manhattan distance" rule, a ghost sitting between two cells where the target was equally reachable from either side would end up picking direction A, then on the very next intersection direction B (the reverse of A) would suddenly score better, then back to A again — over and over. Visually this looked like the ghost was stuck vibrating in place instead of actually chasing the player through the maze.

This is a well-known failure mode of a purely greedy, memoryless heuristic: it has no concept of "where I just came from," so nothing stops it from immediately undoing its last move whenever the numbers say to.

The fix — reversal avoidance: each ghost remembers its lastchoice (its previous direction). At every intersection:

Build the list of valid directions and their target distances, same as before.
Find the best-scoring direction(s).
If continuing the ghost's current direction is among the valid options, prefer sticking with it over switching, as long as it isn't strictly worse.
Only allow reversing into the opposite of lastchoice if it is the only legal move left (a dead end).

This mirrors the classic Pac-Man ghost rule ("ghosts never reverse direction except at dead ends") and it's what actually solved the oscillation — once reversing is deprioritized, a ghost can no longer flip-flop between the same two tiles, and it's forced to commit to a direction and make real progress through the maze.

Tech stack
Python 3
Pygame
Possible future improvements
Replace the greedy Manhattan-distance heuristic with real BFS/A* pathfinding for smarter routing around walls
Multiple levels / increasing difficulty
Sound effects and a proper title screen
Smoother animation timing decoupled from the frame counter
