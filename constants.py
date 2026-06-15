from typing import Any

# Dictionnaire regroupant les coordonnées de la Sprite Sheet
# Format pour chaque clé : (start_x, start_y, largeur, hauteur)
SPRITE_ATLAS: dict[str, tuple[int, int, int, int]] = {
    "PACMAN_CLOSED": (2, 1, 18, 19),
    "PACMAN_HALF_OPEN": (20, 1, 18, 19),
    "PACMAN_OPEN": (38, 1, 18, 19),
    "PINKY_UP_TENT1": (114, 3, 18, 18),
    "PINKY_UP_TENT2": (114, 19, 18, 18),
    "PINKY_DOWN_TENT1": (114, 36, 18, 18),
    "PINKY_DOWN_TENT2": (114, 54, 18, 18),
    "PINKY_SIDE_TENT1": (114, 71, 18, 18),
    "PINKY_SIDE_TENT2": (114, 88, 18, 18),
    "BLINKY_UP_TENT1": (133, 3, 18, 18),
    "BLINKY_UP_TENT2": (133, 19, 18, 18),
    "BLINKY_DOWN_TENT1": (133, 36, 18, 18),
    "BLINKY_DOWN_TENT2": (133, 54, 18, 18),
    "BLINKY_SIDE_TENT1": (133, 71, 18, 18),
    "BLINKY_SIDE_TENT2": (133, 88, 18, 18),
    "CLYDE_UP_TENT1": (154, 3, 18, 18),
    "CLYDE_UP_TENT2": (154, 19, 18, 18),
    "CLYDE_DOWN_TENT1": (154, 36, 18, 18),
    "CLYDE_DOWN_TENT2": (154, 54, 18, 18),
    "CLYDE_SIDE_TENT1": (154, 71, 18, 18),
    "CLYDE_SIDE_TENT2": (154, 88, 18, 18),
    "INKY_UP_TENT1": (174, 3, 18, 18),
    "INKY_UP_TENT2": (174, 19, 18, 18),
    "INKY_DOWN_TENT1": (174, 36, 18, 18),
    "INKY_DOWN_TENT2": (174, 54, 18, 18),
    "INKY_SIDE_TENT1": (174, 71, 18, 18),
    "INKY_SIDE_TENT2": (174, 88, 18, 18),
    "WH_SCARED_GHOST_TENT1": (93, 21, 18, 18),
    "WH_SCARED_GHOST_TENT2": (75, 21, 18, 18),
    "BL_SCARED_GHOST_TENT1": (93, 4, 18, 18),
    "BL_SCARED_GHOST_TENT2": (75, 4, 18, 18),
    "UP_EATEN_GHOST_EYES_DOWN": (2, 24, 18, 18),
    "UP_EATEN_GHOST_EYES_UP": (38, 24, 18, 18),
    "UP_EATEN_GHOST_EYES_LEFT": (21, 24, 18, 18),
    "UP_EATEN_GHOST_EYES_RIGHT": (55, 24, 18, 18),
    "DOWN_EATEN_GHOST_EYES_DOWN": (2, 22, 18, 18),
    "DOWN_EATEN_GHOST_EYES_UP": (38, 22, 18, 18),
    "DOWN_EATEN_GHOST_EYES_LEFT": (21, 22, 18, 18),
    "DOWN_EATEN_GHOST_EYES_RIGHT": (55, 22, 18, 18)
}

TILE_SIZE: int = 50
HUD_HEIGHT: int = 70

# --- PAC-MAN ---
PACMAN_SPRITES: list[str] = ["PACMAN_CLOSED",
                             "PACMAN_HALF_OPEN",
                             "PACMAN_OPEN",
                             "PACMAN_HALF_OPEN"]

# --- BLINKY (Fantôme Rouge) ---
BLINKY_UP: list[str] = ["BLINKY_UP_TENT1", "BLINKY_UP_TENT2"]
BLINKY_DOWN: list[str] = ["BLINKY_DOWN_TENT1", "BLINKY_DOWN_TENT2"]
BLINKY_SIDE: list[str] = ["BLINKY_SIDE_TENT1", "BLINKY_SIDE_TENT2"]

# --- PINKY (Fantôme Rose) ---
PINKY_UP: list[str] = ["PINKY_UP_TENT1", "PINKY_UP_TENT2"]
PINKY_DOWN: list[str] = ["PINKY_DOWN_TENT1", "PINKY_DOWN_TENT2"]
PINKY_SIDE: list[str] = ["PINKY_SIDE_TENT1", "PINKY_SIDE_TENT2"]

# --- CLYDE (Fantôme Orange) ---
CLYDE_UP: list[str] = ["CLYDE_UP_TENT1", "CLYDE_UP_TENT2"]
CLYDE_DOWN: list[str] = ["CLYDE_DOWN_TENT1", "CLYDE_DOWN_TENT2"]
CLYDE_SIDE: list[str] = ["CLYDE_SIDE_TENT1", "CLYDE_SIDE_TENT2"]

# --- INKY (Fantôme Bleu) ---
INKY_UP: list[str] = ["INKY_UP_TENT1", "INKY_UP_TENT2"]
INKY_DOWN: list[str] = ["INKY_DOWN_TENT1", "INKY_DOWN_TENT2"]
INKY_SIDE: list[str] = ["INKY_SIDE_TENT1", "INKY_SIDE_TENT2"]

# --- SCARED GHOST ---
SCARED_GHOST: list[str] = ["WH_SCARED_GHOST_TENT1",
                           "WH_SCARED_GHOST_TENT2",
                           "BL_SCARED_GHOST_TENT2",
                           "BL_SCARED_GHOST_TENT1"]

# --- EATED GHOST (Eyes only) ---
EATED_GHOST_UP: list[str] = ["UP_EATEN_GHOST_EYES_UP",
                             "DOWN_EATEN_GHOST_EYES_UP"]
EATED_GHOST_DOWN: list[str] = ["UP_EATEN_GHOST_EYES_DOWN",
                               "DOWN_EATEN_GHOST_EYES_DOWN"]
EATED_GHOST_LEFT: list[str] = ["UP_EATEN_GHOST_EYES_LEFT",
                               "DOWN_EATEN_GHOST_EYES_LEFT"]
EATED_GHOST_RIGHT: list[str] = ["UP_EATEN_GHOST_EYES_RIGHT",
                                "DOWN_EATEN_GHOST_EYES_RIGHT"]

SPRITE_ATLAS2: dict[str, tuple[int, int, int, int]] = {
    "LINK_DOWN_1": (70, 4, 16, 21),
    "LINK_DOWN_2": (138, 4, 16, 21),
    "LINK_UP_1": (36, 111, 16, 21),
    "LINK_UP_2": (121, 110, 16, 21),
    "LINK_SIDE_1": (21, 58, 15, 23),
    "LINK_SIDE_2": (200, 60, 15, 22)
}

SPRITE_ATLAS3: dict[str, tuple[int, int, int, int]] = {
    "MONSTER1_DOWN1": (8, 79, 17, 24),
    "MONSTER1_DOWN2": (29, 79, 17, 24),
    "MONSTER1_UP1": (94, 80, 16, 24),
    "MONSTER1_UP2": (116, 80, 16, 24),
    "MONSTER1_SIDE1": (51, 79, 16, 24),
    "MONSTER1_SIDE2": (72, 79, 16, 24),

    "MONSTER2_DOWN1": (384, 80, 16, 24),
    "MONSTER2_DOWN2": (406, 80, 16, 24),
    "MONSTER2_UP1": (472, 80, 16, 24),
    "MONSTER2_UP2": (494, 80, 16, 24),
    "MONSTER2_SIDE1": (428, 80, 17, 24),
    "MONSTER2_SIDE2": (450, 80, 17, 24),

    "MONSTER_SCARED_DOWN1": (384, 409, 17, 27),
    "MONSTER_SCARED_DOWN2": (405, 409, 17, 25),
    "MONSTER_SCARED_UP1": (471, 409, 17, 27),
    "MONSTER_SCARED_UP2": (492, 409, 17, 27),
    "MONSTER_SCARED_SIDE1": (428, 409, 17, 27),
    "MONSTER_SCARED_SIDE2": (449, 409, 17, 27),
}

SPRITE_ATLAS4: dict[str, tuple[int, int, int, int]] = {
    "MONSTER3_DOWN1": (687, 79, 14, 16),
    "MONSTER3_DOWN2": (704, 79, 14, 16),
    "MONSTER3_UP1": (757, 79, 14, 16),
    "MONSTER3_UP2": (774, 79, 14, 16),
    "MONSTER3_SIDE1": (722, 79, 14, 16),
    "MONSTER3_SIDE2": (740, 80, 14, 16),

    "MONSTER4_DOWN1": (933, 43, 16, 20),
    "MONSTER4_DOWN2": (954, 43, 16, 20),
    "MONSTER4_UP1": (1020, 43, 16, 20),
    "MONSTER4_UP2": (1042, 43, 16, 20),
    "MONSTER4_SIDE1": (976, 43, 17, 20),
    "MONSTER4_SIDE2": (998, 43, 16, 20)
}

THEMES_ANIMATIONS: dict[str, Any] = {
    "NORMAL": {
        "PLAYER": {   # Link
            "N": ["PACMAN_CLOSED",
                  "PACMAN_HALF_OPEN",
                  "PACMAN_OPEN",
                  "PACMAN_HALF_OPEN"],
            "S": ["PACMAN_CLOSED",
                  "PACMAN_HALF_OPEN",
                  "PACMAN_OPEN",
                  "PACMAN_HALF_OPEN"],
            "E": ["PACMAN_CLOSED",
                  "PACMAN_HALF_OPEN",
                  "PACMAN_OPEN",
                  "PACMAN_HALF_OPEN"],
            "W": ["PACMAN_CLOSED",
                  "PACMAN_HALF_OPEN",
                  "PACMAN_OPEN",
                  "PACMAN_HALF_OPEN"]
        },
        "BLINKY": {  # Blinky
            "N": ["BLINKY_UP_TENT1", "BLINKY_UP_TENT2"],
            "S": ["BLINKY_DOWN_TENT1", "BLINKY_DOWN_TENT2"],
            "E": ["BLINKY_SIDE_TENT1", "BLINKY_SIDE_TENT2"],
            "W": ["BLINKY_SIDE_TENT1", "BLINKY_SIDE_TENT2"]
        },
        "PINKY": {  # Pinky
            "N": ["PINKY_UP_TENT1", "PINKY_UP_TENT2"],
            "S": ["PINKY_DOWN_TENT1", "PINKY_DOWN_TENT2"],
            "E": ["PINKY_SIDE_TENT1", "PINKY_SIDE_TENT2"],
            "W": ["PINKY_SIDE_TENT1", "PINKY_SIDE_TENT2"]
        },
        "CLYDE": {  # Clyde
            "N": ["CLYDE_UP_TENT1", "CLYDE_UP_TENT2"],
            "S": ["CLYDE_DOWN_TENT1", "CLYDE_DOWN_TENT2"],
            "E": ["CLYDE_SIDE_TENT1", "CLYDE_SIDE_TENT2"],
            "W": ["CLYDE_SIDE_TENT1", "CLYDE_SIDE_TENT2"]
        },
        "INKY": {  # Inky
            "N": ["INKY_UP_TENT1", "INKY_UP_TENT2"],
            "S": ["INKY_DOWN_TENT1", "INKY_DOWN_TENT2"],
            "E": ["INKY_SIDE_TENT1", "INKY_SIDE_TENT2"],
            "W": ["INKY_SIDE_TENT1", "INKY_SIDE_TENT2"]
        },
        "SCARED_GHOSTS": {
            "N": ["WH_SCARED_GHOST_TENT1",
                  "WH_SCARED_GHOST_TENT2",
                  "BL_SCARED_GHOST_TENT2",
                  "BL_SCARED_GHOST_TENT1"],
            "S": ["WH_SCARED_GHOST_TENT1",
                  "WH_SCARED_GHOST_TENT2",
                  "BL_SCARED_GHOST_TENT2",
                  "BL_SCARED_GHOST_TENT1"],
            "E": ["WH_SCARED_GHOST_TENT1",
                  "WH_SCARED_GHOST_TENT2",
                  "BL_SCARED_GHOST_TENT2",
                  "BL_SCARED_GHOST_TENT1"],
            "W": ["WH_SCARED_GHOST_TENT1",
                  "WH_SCARED_GHOST_TENT2",
                  "BL_SCARED_GHOST_TENT2",
                  "BL_SCARED_GHOST_TENT1"],
        },
        "EATED_GHOSTS": {
            "N": ["UP_EATEN_GHOST_EYES_UP", "DOWN_EATEN_GHOST_EYES_UP"],
            "S": ["UP_EATEN_GHOST_EYES_DOWN", "DOWN_EATEN_GHOST_EYES_DOWN"],
            "E": ["UP_EATEN_GHOST_EYES_RIGHT", "DOWN_EATEN_GHOST_EYES_RIGHT"],
            "W": ["UP_EATEN_GHOST_EYES_LEFT", "DOWN_EATEN_GHOST_EYES_LEFT"],
        },
    },
    "ZELDA": {
        "PLAYER": {  # Link !
            "N": ["LINK_UP_1", "LINK_UP_2"],
            "S": ["LINK_DOWN_1", "LINK_DOWN_2"],
            "E": ["LINK_SIDE_1", "LINK_SIDE_2"],
            "W": ["LINK_SIDE_1", "LINK_SIDE_2"]
        },
        "BLINKY": {  # Blinky
            "N": ["MONSTER1_UP1", "MONSTER1_UP2"],
            "S": ["MONSTER1_DOWN1", "MONSTER1_DOWN2"],
            "E": ["MONSTER1_SIDE1", "MONSTER1_SIDE2"],
            "W": ["MONSTER1_SIDE1", "MONSTER1_SIDE2"]
        },
        "PINKY": {  # Pinky
            "N": ["MONSTER2_UP1", "MONSTER2_UP2"],
            "S": ["MONSTER2_DOWN1", "MONSTER2_DOWN2"],
            "E": ["MONSTER2_SIDE1", "MONSTER2_SIDE2"],
            "W": ["MONSTER2_SIDE1", "MONSTER2_SIDE2"]
        },
        "CLYDE": {  # Clyde
            "N": ["MONSTER3_UP1", "MONSTER3_UP2"],
            "S": ["MONSTER3_DOWN1", "MONSTER3_DOWN2"],
            "E": ["MONSTER3_SIDE1", "MONSTER3_SIDE2"],
            "W": ["MONSTER3_SIDE1", "MONSTER3_SIDE2"]
        },
        "INKY": {  # Inky
            "N": ["MONSTER4_UP1", "MONSTER4_UP2"],
            "S": ["MONSTER4_DOWN1", "MONSTER4_DOWN2"],
            "E": ["MONSTER4_SIDE1", "MONSTER4_SIDE2"],
            "W": ["MONSTER4_SIDE1", "MONSTER4_SIDE2"]
        },
        "SCARED_GHOSTS": {
            "N": ["MONSTER_SCARED_UP1",
                  "MONSTER_SCARED_UP2",
                  "MONSTER_SCARED_UP1",
                  "MONSTER_SCARED_UP2"],
            "S": ["MONSTER_SCARED_DOWN1",
                  "MONSTER_SCARED_DOWN2",
                  "MONSTER_SCARED_DOWN1",
                  "MONSTER_SCARED_DOWN2"],
            "E": ["MONSTER_SCARED_SIDE1",
                  "MONSTER_SCARED_SIDE2",
                  "MONSTER_SCARED_SIDE1",
                  "MONSTER_SCARED_SIDE2"],
            "W": ["MONSTER_SCARED_SIDE1",
                  "MONSTER_SCARED_SIDE2",
                  "MONSTER_SCARED_SIDE1",
                  "MONSTER_SCARED_SIDE2"],
        },
        "EATED_GHOSTS": {
            "N": ["UP_EATEN_GHOST_EYES_UP", "DOWN_EATEN_GHOST_EYES_UP"],
            "S": ["UP_EATEN_GHOST_EYES_DOWN", "DOWN_EATEN_GHOST_EYES_DOWN"],
            "E": ["UP_EATEN_GHOST_EYES_RIGHT", "DOWN_EATEN_GHOST_EYES_RIGHT"],
            "W": ["UP_EATEN_GHOST_EYES_LEFT", "DOWN_EATEN_GHOST_EYES_LEFT"],
        },
    }
}

THEMES_CONFIG: dict[str, dict[str, Any]] = {
    "NORMAL": {
        "PLAYER": {
            "IMAGE_PATH": "assets/PacMan.gif",
            "ATLAS": SPRITE_ATLAS,
        },
        "BLINKY": {
            "IMAGE_PATH": "assets/PacMan.gif",
            "ATLAS": SPRITE_ATLAS,
        },
        "PINKY": {
            "IMAGE_PATH": "assets/PacMan.gif",
            "ATLAS": SPRITE_ATLAS,
        },
        "CLYDE": {
            "IMAGE_PATH": "assets/PacMan.gif",
            "ATLAS": SPRITE_ATLAS,
        },
        "INKY": {
            "IMAGE_PATH": "assets/PacMan.gif",
            "ATLAS": SPRITE_ATLAS,
        },
        "SCARED_GHOSTS": {
            "IMAGE_PATH": "assets/PacMan.gif",
            "ATLAS": SPRITE_ATLAS,
        },
        "EATED_GHOSTS": {
            "IMAGE_PATH": "assets/PacMan.gif",
            "ATLAS": SPRITE_ATLAS,
        }
    },
    "ZELDA": {
        "PLAYER": {
            "IMAGE_PATH": "assets/Link.png",
            "ATLAS": SPRITE_ATLAS2,
        },
        "BLINKY": {
            "IMAGE_PATH": "assets/Monster_1_2.png",
            "ATLAS": SPRITE_ATLAS3,
        },
        "PINKY": {
            "IMAGE_PATH": "assets/Monster_1_2.png",
            "ATLAS": SPRITE_ATLAS3,
        },
        "CLYDE": {
            "IMAGE_PATH": "assets/Monster_3_4.png",
            "ATLAS": SPRITE_ATLAS4,
        },
        "INKY": {
            "IMAGE_PATH": "assets/Monster_3_4.png",
            "ATLAS": SPRITE_ATLAS4,
        },
        "SCARED_GHOSTS": {
            "IMAGE_PATH": "assets/Monster_1_2.png",
            "ATLAS": SPRITE_ATLAS3,
        },
        "EATED_GHOSTS": {
            "IMAGE_PATH": "assets/PacMan.gif",
            "ATLAS": SPRITE_ATLAS,
        }
    }
}
