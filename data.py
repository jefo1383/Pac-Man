import json
from typing import Any, cast, TYPE_CHECKING
import random
import sys
if TYPE_CHECKING:
    MazeGenerator = Any
else:
    from mazegenerator.mazegenerator import MazeGenerator
from constants import THEMES_CONFIG, THEMES_ANIMATIONS, TILE_SIZE
import pygame


def load_theme_sprites(theme_name: str) ->\
        dict[str, dict[str, list[pygame.surface.Surface]]]:
    """
    Charge, découpe et applique les transformations aux sprites
    selon le thème choisi.

    Cette fonction parcourt les configurations d'animations du thème, charge la
    Sprite Sheet associée, extrait les morceaux correspondants aux textures de
    chaque personnage, applique des rotations ou des inversions miroirs si
    nécessaire, et redimensionne le tout à la taille des tuiles de la grille.

    Args:
        theme_name: Le nom du thème graphique à appliquer
        ("NORMAL" ou "ZELDA").
    Returns:
        Un dictionnaire imbriqué associant chaque personnage et chaque
        direction à une liste de surfaces Pygame prêtes pour l'animation.
    """
    theme_surfaces: dict[str, dict[str, list[pygame.surface.Surface]]] = {}
    loaded_images: dict[str, pygame.surface.Surface] = {}

    config = THEMES_CONFIG[theme_name]
    animations = THEMES_ANIMATIONS[theme_name]

    for character, dirs in animations.items():
        theme_surfaces[character] = {}

        image_path = config[character]["IMAGE_PATH"]

        if image_path not in loaded_images:
            loaded_images[image_path] =\
                pygame.image.load(image_path).convert_alpha()
        sheet = loaded_images[image_path]
        atlas: dict[str, tuple[int, int, int, int]] =\
            config[character]["ATLAS"]
        for direction, frame_names in dirs.items():
            theme_surfaces[character][direction] = []
            for frame_name in frame_names:
                x, y, w, h = atlas[frame_name]
                piece = sheet.subsurface((x, y, w, h))
                if direction == "W" and theme_name == "ZELDA":
                    piece = pygame.transform.flip(piece, True, False)
                if theme_name == "NORMAL" and character in ["BLINKY", "PINKY",
                                                            "INKY", "CLYDE"]:
                    if direction == "E":
                        piece = pygame.transform.flip(piece, True, False)
                if theme_name == "NORMAL" and character == "PLAYER":
                    if direction == "N":
                        piece = pygame.transform.rotate(piece, 90)
                    if direction == "W":
                        piece = pygame.transform.rotate(piece, 180)
                    if direction == "S":
                        piece = pygame.transform.rotate(piece, 270)
                piece = pygame.transform.scale(piece, (TILE_SIZE, TILE_SIZE))
                piece_bg_color = piece.get_at((0, 0))
                piece.set_colorkey(piece_bg_color)
                theme_surfaces[character][direction].append(piece)
    return theme_surfaces


def parse_config(file_path: str) -> dict[Any, Any]:
    """
    Lit et extrait les données du fichier de configuration JSON.

    La fonction ouvre 'config.json', nettoie les espaces superflus et ignore
    systématiquement toutes les lignes de commentaires débutant par le
    caractère '#'.

    Args:
        None
    Returns:
        Un dictionnaire contenant les données brutes lues, ou un dictionnaire
        vide si le fichier est absent ou corrompu.
    """
    try:
        buffer: str = ""
        with open(file_path, "r") as file:
            for _, line in enumerate(file, 1):
                clean_line = line.strip()
                if not clean_line or clean_line.startswith("#"):
                    continue
                buffer += clean_line
        return cast(dict[Any, Any], json.loads(buffer))
    except FileNotFoundError:
        print(f"Error: The configuration file '{file_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Syntax error in '{file_path}'. "
              "It must be a valid JSON.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied to read '{file_path}'.")
        sys.exit(1)


def validate_config(config_data: dict[Any, Any]) ->\
        dict[str, Any]:
    """
    Vérifie la validité des données de configuration et applique des valeurs
    de secours.

    Chaque paramètre clé (vies, points, dimensions des niveaux, quantité de
    pacgums) est inspecté. Si une valeur est manquante, erronée ou hors des
    limites de sécurité, un message d'avertissement est affiché et une valeur
    par défaut sécurisée est injectée.

    Args:
        config_data: Le dictionnaire contenant les paramètres bruts extraits
        du JSON.
    Returns:
        Un dictionnaire de configuration totalement validé et nettoyé, prêt à
        l'emploi.
    """
    default_levels = {
        "1": {"width": 20, "height": 20},
        "2": {"width": 19, "height": 19},
        "3": {"width": 18, "height": 18},
        "4": {"width": 17, "height": 17},
        "5": {"width": 16, "height": 16},
        "6": {"width": 15, "height": 15},
        "7": {"width": 14, "height": 14},
        "8": {"width": 13, "height": 13},
        "9": {"width": 12, "height": 12},
        "10": {"width": 10, "height": 10}
    }
    default_pacgum = {
        lvl: (((size["width"] * size["height"]) * 70) // 100) - 23
        for lvl, size in default_levels.items()
    }
    default_config = {
        "highscore_filename": "high_scores.json",
        "size_levels": default_levels,
        "lives": 3,
        "pacgum": default_pacgum,
        "points_per_pacgum": 10,
        "points_per_super_pacgum": 50,
        "points_per_ghost": 200,
        "seed": 42,
        "level_max_time": 90
    }
    validated = default_config.copy()
    if "highscore_filename" not in config_data:
        print("Warning: 'highscore_filename' is missing. Using default.")
    else:
        if isinstance(config_data["highscore_filename"], str) and\
                config_data["highscore_filename"].endswith(".json"):
            validated["highscore_filename"] = config_data["highscore_filename"]
        else:
            print("Warning: 'highscore_filename' is invalid. Using default.")
    if "size_levels" not in config_data:
        print("Warning: 'size_levels' is missing. Using default.")
    else:
        if isinstance(config_data["size_levels"], dict):
            try:
                lvls = [int(lvl) for lvl in config_data["size_levels"].keys()]
                check = range(1, len(lvls) + 1)
                is_valid = True
                if sorted(lvls) == list(check):
                    for value in config_data["size_levels"].values():
                        if not isinstance(value, dict):
                            is_valid = False
                            break
                        else:
                            if "width" not in value or "height" not in value:
                                is_valid = False
                                break
                            if not isinstance(value["width"], int) or not\
                                    6 < value["width"] < 52:
                                is_valid = False
                                break
                            if not isinstance(value["height"], int) or not\
                                    6 < value["height"] < 27:
                                is_valid = False
                                break
                else:
                    is_valid = False
                if is_valid:
                    validated["size_levels"] = config_data["size_levels"]
                else:
                    print("Warning: 'size_levels' is invalid."
                          "Using default.")
            except ValueError as e:
                print(e)
    for key in ["lives", "points_per_pacgum", "points_per_super_pacgum",
                "points_per_ghost", "seed", "level_max_time"]:
        if key in config_data and isinstance(config_data[key], int)\
                and config_data[key] > 0:
            validated[key] = config_data[key]
        else:
            print(f"Warning: '{key}' is invalid or missing. Using default.")
    if "pacgum" not in config_data:
        print("Warning: 'pacgum' is missing. Using default.")
    else:
        if isinstance(config_data["pacgum"], dict):
            try:
                lvls = [int(lvl) for lvl in config_data["pacgum"].keys()]
                check = range(1, len(config_data["size_levels"]) + 1)
                is_valid = True
                if sorted(lvls) == list(check):
                    for lvl, value in config_data["pacgum"].items():
                        if not isinstance(value, int) or not 0 < value < (
                                (cast(dict[str, dict[str, int]],
                                      validated["size_levels"])[lvl]["width"] *
                                 cast(dict[str, dict[str, int]],
                                      validated["size_levels"])[lvl]["height"])
                                - 23):
                            is_valid = False
                            break
                else:
                    is_valid = False
                if is_valid:
                    validated["pacgum"] = config_data["pacgum"]
                else:
                    print("Warning: 'pacgum' is invalid."
                          "Using default.")
            except ValueError as e:
                print(e)
    return validated


class MazeAdapter:
    """
    Classe adaptatrice pour l'intégration du générateur de labyrinthe.
    """
    def __init__(self, size_levels: dict[str, dict[str, int]], seed: int)\
            -> None:
        """
        Initialise l'adaptateur avec les configurations de dimensions et la
        graine de base.

        Args:
            size_levels: Dictionnaire listant la largeur et hauteur pour
            chaque niveau.
            seed: Graine pseudo-aléatoire (seed) globale définie pour la
            partie.
        Returns:
            None
        """
        self.size_levels = size_levels
        self.seed = seed

    def generate_level(self, level: int) -> list[list[int]]:
        """
        Génère la matrice structurelle d'un labyrinthe pour un niveau donné.

        Conformément aux spécifications du sujet, le niveau 1 exploite une
        seed fixe, tandis que les niveaux supérieurs obtiennent une seed
        purement aléatoire. Le générateur externe est configuré avec
        perfect=False pour garantir la présence de boucles et de couloirs
        adaptés au gameplay de Pac-Man.

        Args:
            level: L'index numérique du niveau actuel à générer.
        Returns:
            Une liste bidimensionnelle d'entiers représentant les chemins et
            les murs.
        """
        width = self.size_levels[str(level)]["width"]
        height = self.size_levels[str(level)]["height"]
        maze_size = (width, height)
        if level == 1:
            cur_seed = self.seed
        else:
            cur_seed = random.randint(0, sys.maxsize)
        generator = MazeGenerator(size=maze_size, perfect=False,
                                  entry_cell=(0, 0), exit_cell=(1, 0),
                                  seed=cur_seed)
        return cast(list[list[int]], generator.maze)
