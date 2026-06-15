*This activity has been created as part of the 42 curriculum by jfoeller, yafranco.*

# Pac-Man 42

```text
██████╗  █████╗  ██████╗███╗   ███╗ █████╗ ███╗   ██╗
██╔══██╗██╔══██╗██╔════╝████╗ ████║██╔══██╗████╗  ██║
██████╔╝███████║██║     ██╔████╔██║███████║██╔██╗ ██║
██╔═══╝ ██╔══██║██║     ██║╚██╔╝██║██╔══██║██║╚██╗██║
██║     ██║  ██║╚██████╗██║ ╚═╝ ██║██║  ██║██║ ╚████║
╚═╝     ╚═╝  ╚═╝ ╚═════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
```

## Description
Pac-Man 42 is a modern Python recreation of the classic 1980 arcade game. Navigate the maze, eat all the pacgums to score points, and avoid the four ghosts with unique behaviors. Eat a super-pacgum to temporarily turn the tables and eat the ghosts! This project features a robust configuration parser, persistent highscores, strict typing validation, and a secret "Zelda" theme.

## Instructions
The project relies on a `Makefile` for easy execution and strict dependency management.
* **Install dependencies:** `make install` (Uses modern environment managers for strict dependency isolation).
* **Run the game:** `make run` (Alternatively: `python3 pac-man.py config.json`).
* **Clean environment:** `make clean` or `make fclean` to delete the virtual environment.
`make re` for fclean + install.
* **Debug:** `make debug` to run in debug mode with pdb.
* **Linting:** `make lint` or `make lint-strict` to run `flake8` and `mypy --strict` checks.
* **Packaging the game:** `make package` to package the game in one exe file.

## Resources
* Official Python and Pygame documentation.
* Refactoring.guru for exploring the State Pattern and Adapter Pattern.
* AI was used strictly as a learning assistant to brainstorm architectural refactoring (e.g., handling Pygame surface colorkeys, optimizing dictionaries) and to debug strict typing (`mypy --strict`) edge cases. Code logic was written manually.

## Configuration
The game is dynamically configured via a `config.json` file. 
* It supports inline comments starting with `#`. 
* Our parser manually reads the file line by line, strips out the comments, and rebuilds a clean string before passing it to Python's standard `json.loads` module.
* **Safe Defaults:** Handled in `data.py`. If any keys are missing, invalid, or out of bounds (e.g., missing levels or pacgum limits), the game automatically clamps them to safe default values to guarantee no crashes.

## Highscore System
We implemented a persistent highscore system that saves the top 10 players and their scores.
* **Technical Choice:** We chose to store the scores in a dedicated JSON file (`high_scores.json`). This approach was selected over CSV or SQLite because it is highly readable, seamlessly integrates with Python dictionaries, and allows for very simple manual editing during testing.
* **Data Sanitization:** Handled in `high_scores.py`, ensuring names are strictly alphanumeric and capped at 10 characters via `sanitize_name`.

## Maze Generation
The game levels are generated using the external `A-Maze-ing` package.
* **Technical Choice:** To avoid strong coupling, we implemented an **Adapter/Wrapper class** (`MazeAdapter`). This design pattern acts as a bridge, converting the external package's maze format into our game's clean internal format. 
* Level 1 uses a fixed seed (e.g., 42), while subsequent levels use a random seed to offer unlimited replayability.

## Implementation & General Software Architecture
Our software architecture is built around modularity and Object-Oriented Programming (OOP):

* **Movement & Collisions:** We opted for a **Tile-based grid system**. The game logic considers entities to be within specific grid cells, making collision detection with walls straightforward and reliable without complex hitboxes.
* **Ghost AI:** Ghosts use a **Weighted Random algorithm**(75% chance to take the shortest path, 25% to choose randomly) at intersections. They choose their direction dynamically based on distance calculations (euclidian distance for chasing, BFS when they're dead) to reach specific targets unique to their personalities (Blinky, Pinky, Inky, Clyde).
* **Game States:** Pac-Man and the ghosts change behaviors depending on events. We used the **State Pattern (OOP)** to create distinct classes for each state (e.g., `ChasingState`, `FrightenedState`, `DeadState`), completely avoiding messy conditional "spaghetti" code.
* **Scene Manager:** Navigation between the Menu, Game, Pause, and Game Over screens is handled via an explicit state loop in `pac-man.py`.
* **Rendering:** We use native text rendering for the HUD and a complete screen refresh logic per frame to ensure visual integrity.
* **Packaging:** Designed to be compiled as a standalone executable (e.g., using PyInstaller) so players do not need Python installed to launch the game.
Visit https://jfoelleryafranco.itch.io/pac-man-42 .
Password : Pac-man42$
* **Cheat Mode:** Accessible via secret keyboard shortcuts (for review purposes). Press `i` to toggle invincibility, `n` to skip the current level, and `l` on the start screen to launch the secret Zelda theme.
* **Controllers:** We chose to offer 2 controller options:
    - `A` for Left, `D` for Right, `W` for Up, `S` for Down.
    - `Left-Arrow` for Left, `Right-Arrow` for Right, `Up-Arrow` for Up, `Down-Arrow` for Down.

## Project Management
The project was conducted over a 2-week period (divided into 5 distinct phases) using a structured task assignment.
* **jfoeller:** Configuration parsing, Maze generation integration, Ghost AI & States, Game loop/Menu navigation, and Makefile/Packaging.
* **yafranco:** Highscore system, Player mechanics (movement/lives), Collision management, Score calculation, and Visual rendering.
* **Together:** Cheat mode implementation and project documentation.

Detailed tracking (timelines, specific choices, and risk analysis) can be found in the project management directory.