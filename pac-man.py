from data import parse_config, validate_config, MazeAdapter, load_theme_sprites
from game import Game
import random
import pygame
from high_scores import load_highscores, save_highscores, sanitize_name, \
    add_highscore
import sys


def show_instructions() -> None:
    """
    Affiche l'écran des instructions, incluant les règles du jeu
    et les contrôles.

    Génère une interface visuelle listant l'objectif, le fonctionnement des
    super-pacgums, les raccourcis clavier et les commandes de débogage
    (triche).
    La fonction lance une boucle d'événement qui bloque l'exécution jusqu'à
    ce que l'utilisateur presse une touche pour retourner au menu.
    """
    screen = pygame.display.set_mode((600, 800))
    font_title = pygame.font.SysFont("Arial", 40, bold=True)
    font_text = pygame.font.SysFont("Arial", 22)
    font_small = pygame.font.SysFont("Arial", 18)

    screen.fill((0, 0, 0))

    title_surf = font_title.render("INSTRUCTIONS", False, (0, 204, 204))
    title_rect = title_surf.get_rect(centerx=screen.get_width() // 2, top=50)
    screen.blit(title_surf, title_rect)

    instructions = [
        ("GOAL:", (255, 255, 0)),
        ("Eat all the small dots (pacgums) to clear the level.",
         (255, 255, 255)),
        ("Avoid the ghosts! If they catch you, you lose a life.",
         (255, 255, 255)),
        ("", (255, 255, 255)),
        ("POWER PELLETS:", (255, 255, 0)),
        ("Eat the big dots in the corners to become super-powered.",
         (255, 255, 255)),
        ("Ghosts will turn blue and run away. Eat them!", (255, 255, 255)),
        ("", (255, 255, 255)),
        ("CONTROLS:", (255, 255, 0)),
        ("Arrow Keys or 'W'A'S'D: Move Pac-Man", (255, 255, 255)),
        ("ESC : Pause the game", (255, 255, 255)),
        ("", (255, 255, 255)),
        ("CHEAT MODE:", (255, 0, 0)),
        ("Press 'N' : Skip to the next level", (255, 255, 255)),
        ("Press 'I' : Toggle Invincibility", (255, 255, 255)),
        ("Press 'L' in the start menu : Launch a special mode",
         (255, 255, 255))
    ]

    current_y = 130
    for text, color in instructions:
        if text:
            text_surf = font_text.render(text, False, color)
            text_rect = text_surf.get_rect(centerx=screen.get_width() // 2,
                                           top=current_y)
            screen.blit(text_surf, text_rect)
        current_y += 35

    prompt_surf = font_small.render("PRESS ANY KEY TO RETURN", False,
                                    (150, 150, 150))
    prompt_rect = prompt_surf.get_rect(centerx=screen.get_width() // 2,
                                       bottom=750)
    screen.blit(prompt_surf, prompt_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def show_menu(message: str) -> tuple[str, str]:
    """
    Affiche le menu principal ou les écrans de transition
    (victoire/défaite) et gère la navigation.

    Cette fonction dessine l'interface utilisateur contenant
    le message principal, les différentes options d'interaction
    (jouer, instructions, quitter) et affiche dynamiquement la liste
    des meilleurs scores (highscores).
    Elle lance ensuite une boucle d'événements bloquante pour capter
    le choix du joueur, incluant la sélection du thème secret via le
    raccourci clavier approprié.

    Args:
        message: Le texte principal à afficher en haut de l'écran
                 (ex: "Pac-Man", "GAME OVER", "VICTORY").

    Returns:
        Un tuple contenant deux chaînes de caractères :
        - Le prochain état de l'application
        (ex: "PLAYING", "QUIT", "INSTRUCTIONS").
        - Le thème visuel sélectionné par le joueur
        ("NORMAL" ou "ZELDA").
    """

    screen = pygame.display.set_mode((600, 800))
    pygame.display.set_caption("Pac-Man 42 by Jfoeller & Yafranco")
    screen.fill((0, 0, 0))

    font_1 = pygame.font.SysFont("Arial", 60)
    text_surface_1 = font_1.render(message, False, (0, 149, 182))
    text_rect_1 = text_surface_1.get_rect(centerx=screen.get_width() // 2,
                                          top=50)
    screen.blit(text_surface_1, text_rect_1)

    font_2 = pygame.font.SysFont("Arial", 30)

    text_play = font_2.render("PRESS 'SPACE' TO PLAY", False,
                              (58, 152, 105))
    rect_play = text_play.get_rect(centerx=screen.get_width() // 2,
                                   top=140)
    screen.blit(text_play, rect_play)

    text_inst = font_2.render("PRESS 'C' FOR INSTRUCTIONS", False,
                              (255, 165, 0))
    rect_inst = text_inst.get_rect(centerx=screen.get_width() // 2,
                                   top=190)
    screen.blit(text_inst, rect_inst)

    text_exit = font_2.render("PRESS 'ESC' TO EXIT", False,
                              (255, 0, 0))
    rect_exit = text_exit.get_rect(centerx=screen.get_width() // 2,
                                   top=240)
    screen.blit(text_exit, rect_exit)

    text_hs = font_2.render("Highscores :", False, (243, 237, 0))
    rect_hs = text_hs.get_rect(centerx=screen.get_width() // 2,
                               top=310)
    screen.blit(text_hs, rect_hs)

    best_scores = load_highscores()
    current_y = 360
    for i, entry in enumerate(best_scores):
        text_score = font_2.render(f"{i+1}. {entry.name} - {entry.score}",
                                   False, (255, 255, 255))
        score_rect = text_score.get_rect(centerx=screen.get_width() // 2,
                                         top=current_y)
        screen.blit(text_score, score_rect)
        current_y += 30
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ("QUIT", "NORMAL")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return ("PLAYING", "NORMAL")
                if event.key == pygame.K_l:
                    return ("PLAYING", "ZELDA")
                if event.key == pygame.K_c:
                    return ("INSTRUCTIONS", "NORMAL")
                if event.key == pygame.K_ESCAPE:
                    return ("QUIT", "NORMAL")


def get_player_name(score: int, is_victory: bool = False) -> str:
    """
    Affiche l'écran de fin de partie et capture la saisie clavier
    pour le nom du joueur.

    Cette fonction gère à la fois les scénarios de victoire
    et de défaite (Game Over) en adaptant le texte du titre
    et sa couleur. Elle crée une boucle d'événements
    spécifique pour intercepter les frappes clavier
    (lettres, retour arrière, entrée) afin de construire dynamiquement
    le nom du joueur pour le système de highscores.

    Args:
        score: Le score final obtenu par le joueur à afficher à l'écran.
        is_victory: Indique si l'écran doit célébrer une victoire (True) ou
                    afficher un Game Over classique (False, par défaut).

    Returns:
        Une chaîne de caractères représentant le nom saisi par le joueur,
        ou "QUIT" si l'utilisateur ferme la fenêtre.
    """
    screen = pygame.display.set_mode((600, 800))
    font_title = pygame.font.SysFont("Arial", 40)
    font_text = pygame.font.SysFont("Arial", 24)
    name: str = ""
    if is_victory:
        title_text = "CONGRATULATIONS"
        title_color = (0, 255, 0)  # Vert
    else:
        title_text = "GAME OVER"
        title_color = (255, 0, 0)  # Rouge
    while True:
        screen.fill((0, 0, 0))

        title_surf = font_title.render(title_text, False, title_color)
        title_rect = title_surf.get_rect(centerx=screen.get_width() // 2,
                                         top=150)
        screen.blit(title_surf, title_rect)

        score_surf = font_text.render(f"Your score : {score}", False,
                                      (255, 255, 255))
        score_rect = score_surf.get_rect(centerx=screen.get_width() // 2,
                                         top=250)
        screen.blit(score_surf, score_rect)

        prompt_surf = font_text.render("Enter your name (Enter to valid) :",
                                       False, (255, 255, 255))
        prompt_rect = prompt_surf.get_rect(centerx=screen.get_width() // 2,
                                           top=350)
        screen.blit(prompt_surf, prompt_rect)

        name_surf = font_text.render(name + "_", False, (255, 255, 0))
        name_rect = name_surf.get_rect(centerx=screen.get_width() // 2,
                                       top=400)
        screen.blit(name_surf, name_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or\
                        event.key == pygame.K_KP_ENTER:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode


def set_pacgums(size_levels: dict[str, dict[str, int]], maze: list[list[int]],
                current_lvl: int, start_x: int, start_y: int,
                total_pacgums: int) -> list[list[int]]:
    """
    Répartit les pacgums classiques et les super-pacgums sur
    la grille du niveau.

    Cette fonction applique des règles de placement spécifiques
    via des opérations sur les masques binaires de la grille :
    1. Place un super-pacgum (masque binaire 32) dans chacun des
    4 coins du labyrinthe.
    2. Définit une zone d'exclusion centrale en forme de logo "42"
    (`ft_small`) pour empêcher l'apparition de pacgums à cet endroit.
    3. Exclut la position de départ du joueur pour éviter une collecte
    immédiate.
    4. Répartit aléatoirement le nombre défini de pacgums (`total_pacgums`) sur
       les cases libres restantes (masque binaire 16).

    Args:
        size_levels: Dictionnaire contenant les dimensions
        (largeur/hauteur) par niveau.
        maze: La matrice 2D du niveau actuel (grille d'entiers).
        current_lvl: L'identifiant (entier) du niveau en cours
        pour récupérer sa taille.
        start_x: La coordonnée X de départ du joueur sur la grille.
        start_y: La coordonnée Y de départ du joueur sur la grille.
        total_pacgums: Le nombre exact de pacgums standards à générer.

    Returns:
        La matrice du labyrinthe (list[list[int]]) mise à jour
        avec les entités intégrées.
    """

    ft_small = [
        [1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1]
    ]
    width = size_levels[str(current_lvl)]['width']
    height = size_levels[str(current_lvl)]['height']
    posy = (height - len(ft_small)) // 2
    posx = (width - len(ft_small[0])) // 2

    corners = [(0, 0), (0, height - 1), (width - 1, 0),
               (width - 1, height - 1)]
    for cell in corners:
        x, y = cell
        maze[y][x] |= 32

    free_cells = []
    for y in range(height):
        for x in range(width):
            if (x, y) != (start_x, start_y) and (x, y) not in corners:
                in_ft_small = (posy <= y < posy + len(ft_small)) and\
                    (posx <= x < posx + len(ft_small[0]))
                in_pattern = in_ft_small and\
                    (ft_small[y - posy][x - posx] == 1)
                if not in_pattern:
                    free_cells.append((x, y))

    cells_pacgum = random.sample(free_cells, total_pacgums)
    for p_cell in cells_pacgum:
        x, y = p_cell
        maze[y][x] |= 16
    return maze


if __name__ == "__main__":
    # Vérification : Est-ce qu'on tourne depuis l'exécutable PyInstaller ?
    if getattr(sys, 'frozen', False):
        # --- MODE EXÉCUTABLE ---
        if len(sys.argv) == 1:
            config_file = "config.json"  # Mode silencieux par défaut
        elif len(sys.argv) == 2:
            config_file = sys.argv[1]
        else:
            sys.exit(1)
    else:
        # --- MODE NORMAL (Exigence stricte du sujet) ---
        if len(sys.argv) != 2:
            print("Error: The program must be launched with exactly "
                  "one argument.")
            print("Usage: python3 pac-man.py <config_file.json>")
            sys.exit(1)
        config_file = sys.argv[1]

    # Vérification commune de l'extension
    if not config_file.endswith(".json"):
        print("Error: The configuration file must be a .json file.")
        sys.exit(1)

    play_mode: str = "NORMAL"
    try:
        pygame.init()
        config = parse_config(config_file)
        valid_config = validate_config(config)
        current_lvl = 1
        if isinstance(valid_config["size_levels"], dict):
            size_levels: dict[str, dict[str, int]] =\
                valid_config["size_levels"]
        if isinstance(valid_config["seed"], int):
            seed = valid_config["seed"]
        if isinstance(valid_config["pacgum"], dict):
            pacgums_lvl: dict[str, int] = valid_config["pacgum"]
        generator = MazeAdapter(size_levels, seed)
        app_status = "START_MENU"
        current_score: int = 0
        current_lives: int = valid_config["lives"]
        while True:
            if app_status == "START_MENU":
                app_status, play_mode = show_menu("PAC-MAN")
                current_lvl = 1
                current_score = 0
                current_lives = valid_config["lives"]

            elif app_status == "INSTRUCTIONS":
                show_instructions()
                app_status = "START_MENU"

            elif app_status == "PLAYING":
                if isinstance(pacgums_lvl[str(current_lvl)], int):
                    total_pacgums = int(pacgums_lvl[str(current_lvl)])
                maze = generator.generate_level(current_lvl)
                width = size_levels[str(current_lvl)]['width']
                height = size_levels[str(current_lvl)]['height']
                if height >= 10 and width >= 14:
                    posx = (width - 7) // 2
                    posy = (height - 5) // 2
                    start_x = posx + 3
                    start_y = posy + 2
                else:
                    start_x = width // 2
                    start_y = height // 2
                theme_sprites = load_theme_sprites(play_mode)
                maze = set_pacgums(size_levels, maze, current_lvl, start_x,
                                   start_y, total_pacgums)
                game = Game(start_x, start_y, maze, valid_config, current_lvl,
                            current_score, theme_sprites, current_lives)
                game.draw()
                app_status = game.run()
                current_score = game.score
                current_lives = game.pacman.lives

            elif app_status == "GAME_OVER":
                scores = load_highscores()
                name = get_player_name(game.score, is_victory=False)
                if name == "QUIT":
                    app_status = "QUIT"
                else:
                    valid_name = sanitize_name(name)
                    add_highscore(scores, valid_name, game.score)
                    save_highscores(scores)
                    app_status = "START_MENU"

            elif app_status == "QUIT":
                break

            elif app_status == "NEXT_LEVEL":
                if current_lvl < len(size_levels):
                    current_lvl += 1
                    app_status = "PLAYING"
                else:
                    scores = load_highscores()
                    name = get_player_name(game.score, is_victory=True)
                    if name == "QUIT":
                        app_status = "QUIT"
                    else:
                        valid_name = sanitize_name(name)
                        add_highscore(scores, valid_name, game.score)
                        save_highscores(scores)
                        app_status, play_mode = show_menu("VICTORY")
    except (Exception, FileNotFoundError) as e:
        print(f"Fatal error: {e}")
    finally:
        pygame.quit()
