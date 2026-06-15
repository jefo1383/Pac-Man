from player import Player, Direction
from ghost_engine import Ghost, Blinky, Pinky, Clyde, Inky, ChasingState, \
    DeadState, FrightenedState, WaitingState
import pygame
from typing import Any
import constants


class Game:
    def __init__(self, start_x: int, start_y: int, maze: list[list[int]],
                 config_data: dict[str, Any],
                 current_lvl: int,
                 initial_score: int = 0,
                 theme_sprites: dict[str, Any] = {},
                 initial_lives: int | None = None) -> None:
        """
        Initialise le moteur principal du jeu et configure l'état
        initial du niveau.

        Cette méthode met en place la fenêtre Pygame aux bonnes dimensions,
        extrait les paramètres de jeu (points, limites de temps,
        nombre de pacgums) depuis les données de configuration,
        et instancie les entités principales :
        le joueur (Pac-Man) et les quatre fantômes avec leurs positions
        de départ.
        Elle initialise également les variables d'état pour le score,
        le chronomètre, et les modes spéciaux (pause, intro, triche).

        Args:
            start_x: La coordonnée X de départ du joueur.
            start_y: La coordonnée Y de départ du joueur.
            maze: La matrice 2D du niveau (grille d'entiers).
            config_data: Les paramètres du jeu chargés et validés
            depuis le fichier JSON.
            current_lvl: Le numéro du niveau en cours de génération.
            initial_score: Le score cumulé conservé depuis les niveaux
            précédents (0 par défaut).
            theme_sprites: Les ressources visuelles (sprites) chargées
            pour le thème actif.
            initial_lives: Les vies restantes du joueur,
            surchargeant la configuration par défaut si une partie
            est déjà en cours.
        """

        pygame.display.set_caption("Pac-Man 42 by Jfoeller & Yafranco")
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.screen: pygame.surface.Surface = pygame.display.set_mode(
            (len(maze[0]) * constants.TILE_SIZE,
             (len(maze) * constants.TILE_SIZE)
             + constants.HUD_HEIGHT))
        self.current_lvl = current_lvl
        self.theme_sprites = theme_sprites
        if initial_lives is not None:
            self.lives = initial_lives
        elif isinstance(config_data["lives"], int):
            self.lives = config_data["lives"]
        if isinstance(config_data["points_per_pacgum"], int):
            self.pts_pacgum = config_data["points_per_pacgum"]
        if isinstance(config_data["points_per_super_pacgum"], int):
            self.pts_super_pacgum = config_data["points_per_super_pacgum"]
        if isinstance(config_data["points_per_ghost"], int):
            self.pts_ghost = config_data["points_per_ghost"]
        if isinstance(config_data["pacgum"], dict):
            self.pacgums = config_data["pacgum"]
            if isinstance(self.pacgums[str(current_lvl)], int):
                self.total_pacgums = int(self.pacgums[str(self.current_lvl)])
        self.pacman: Player = Player(start_x, start_y,
                                     self.theme_sprites["PLAYER"], self.lives)
        self.maze: list[list[int]] = maze
        self.dots_left = self.total_pacgums + 4
        self.score: int = initial_score
        self.font = pygame.font.SysFont("Arial", 24)
        self.power_start_time = 0
        blinky: Blinky = Blinky(0, 1, self.maze,
                                (self.pacman.x, self.pacman.y), "E",
                                self.theme_sprites["BLINKY"])
        pinky: Pinky = Pinky(len(self.maze[0]) - 1, 1, self.maze,
                             (self.pacman.x, self.pacman.y), "W",
                             self.theme_sprites["PINKY"])
        clyde: Clyde = Clyde(len(self.maze[0]) - 1, len(self.maze) - 2,
                             self.maze, (self.pacman.x, self.pacman.y), "W",
                             self.theme_sprites["CLYDE"])
        inky: Inky = Inky(0, len(self.maze) - 2, self.maze,
                          (self.pacman.x, self.pacman.y), "E",
                          self.theme_sprites["INKY"])
        self.ghosts: list[Ghost] = [blinky, pinky, clyde, inky]
        self.scar_gh_sprites = self.theme_sprites["SCARED_GHOSTS"]["N"]
        self.dead_gh_sprites = self.theme_sprites["EATED_GHOSTS"]

        if isinstance(config_data["level_max_time"], int):
            self.level_max_time = config_data["level_max_time"]
        self.time_left = self.level_max_time
        self.last_timer_update = 0

        # Variables pour l'intro, menu pause et cheat
        self.in_intro = True
        self.intro_start_ticks = pygame.time.get_ticks()
        self.is_paused = False
        self.cheat_invincible = False

    SCORE_MARGIN = 5
    SCORE_SPACE = 30

    def run(self) -> str:
        """
        Exécute la boucle principale du jeu pour le niveau en cours.

        Cette méthode gère le cycle de vie complet d'une session de jeu
        à 60 FPS :
        1. L'animation d'introduction (gel de l'action de 5 secondes
        avec compte à rebours).
        2. La gestion de l'état de pause et des menus intermédiaires.
        3. La capture des événements clavier (mouvements du joueur,
        codes de triche).
        4. La mise à jour de la logique métier (déplacements, collisions,
        gestion du temps et de l'invincibilité).
        5. Le rendu graphique continu de tous les éléments à l'écran.

        Returns:
            Une chaîne de caractères indiquant le prochain état de
            l'application :
            - "QUIT" : L'utilisateur a fermé la fenêtre.
            - "START_MENU" : L'utilisateur a quitté la partie depuis
            le menu pause.
            - "NEXT_LEVEL" : Le niveau est terminé (toutes les
            pacgums mangées ou raccourci utilisé).
            - "GAME_OVER" : Le joueur a perdu toutes ses vies ou
            le temps est écoulé.
        """

        while True:
            current_ticks = pygame.time.get_ticks()
            if self.is_paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return "QUIT"
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            # Retourne au menu principal de pac-man.py
                            return "START_MENU"
                        elif event.key == pygame.K_RETURN:
                            self.is_paused = False
                            # On réinitialise le timer
                            self.last_timer_update = pygame.time.get_ticks()
                # On redessine l'écran avec le filtre de pause par-dessus
                self.screen.fill((0, 0, 0))
                self.draw()
                self.draw_pause()
                pygame.display.flip()
                self.clock.tick(60)
                continue
            # GESTION DE L'INTRO (FREEZE DE 5 SECONDES)
            if self.in_intro:
                elapsed_intro = (current_ticks - self.intro_start_ticks
                                 ) // 1000
                if elapsed_intro >= 5:
                    self.in_intro = False
                    # On déclenche le top départ du vrai chronomètre de jeu ici
                    self.last_timer_update = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_paused = True
                    elif not self.in_intro:
                        if event.key == pygame.K_n:
                            return "NEXT_LEVEL"
                        elif event.key == pygame.K_i:
                            self.cheat_invincible = not self.cheat_invincible
                            self.pacman.is_powered = self.cheat_invincible
                            if self.cheat_invincible:
                                self.power_start_time = pygame.time.get_ticks()
                        elif event.key == pygame.K_UP or \
                                event.key == pygame.K_w:
                            self.pacman.next_direction = Direction.N
                        elif event.key == pygame.K_DOWN or \
                                event.key == pygame.K_s:
                            self.pacman.next_direction = Direction.S
                        elif event.key == pygame.K_LEFT or \
                                event.key == pygame.K_a:
                            self.pacman.next_direction = Direction.W
                        elif event.key == pygame.K_RIGHT or \
                                event.key == pygame.K_d:
                            self.pacman.next_direction = Direction.E
            if not self.in_intro:
                self.pacman.move(self.maze)
                for ghost in self.ghosts:
                    ghost.check_state(self.pacman)
                    ghost.move(self.pacman)
                self.check_collisions()
                if self.pacman.lives < 1:
                    return "GAME_OVER"
                if self.pacman.is_powered:
                    current_time = pygame.time.get_ticks()
                    if current_time - self.power_start_time > 10000 and\
                            not self.cheat_invincible:
                        self.pacman.is_powered = False
                if current_ticks - self.last_timer_update >= 1000:
                    self.time_left -= 1
                    self.last_timer_update = current_ticks
                if self.time_left <= 0:
                    return "GAME_OVER"

            self.screen.fill((0, 0, 0))
            self.draw()

            if self.in_intro:
                elapsed_intro = (current_ticks - self.intro_start_ticks
                                 ) // 1000
                font_intro = pygame.font.SysFont("Arial", 40, bold=True)

                # Écrire le niveau pendant 2 sec, puis Ready/Steady/Go
                if elapsed_intro < 2:
                    text_str = f"LEVEL {self.current_lvl}"
                    color = (0, 255, 255)  # Cyan
                elif elapsed_intro == 2:
                    text_str = "READY?"
                    color = (255, 255, 0)  # Jaune
                elif elapsed_intro == 3:
                    text_str = "STEADY?"
                    color = (255, 128, 0)  # Orange
                else:
                    text_str = "GO!"
                    color = (0, 255, 0)    # Vert

                text_surf = font_intro.render(text_str, True, color)
                text_rect = text_surf.get_rect(center=(self.screen.get_width()
                                               // 2, (self.screen.get_height()
                                               + constants.HUD_HEIGHT) // 2))

                # Un bandeau noir translucide pour que le texte soit lisible
                bg_rect = pygame.Rect(0, text_rect.y - 10,
                                      self.screen.get_width(),
                                      text_rect.height + 20)
                pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
                self.screen.blit(text_surf, text_rect)

            pygame.display.flip()
            self.clock.tick(60)
            if self.dots_left == 0:
                return "NEXT_LEVEL"

    def check_collisions(self) -> None:
        """
        Vérifie et gère toutes les interactions entre Pac-Man, le décor
        et les fantômes.

        Cette méthode évalue l'état du jeu à chaque frame pour trois types
        de collisions :
        1. Les pacgums classiques (masque binaire 16) : incrémente le score
        et met à jour la grille.
        2. Les super-pacgums (masque binaire 32) : déclenche l'état
        d'invincibilité (mode puissance) du joueur et démarre le
        chronomètre associé.
        3. Les fantômes : utilise un calcul de distance en pixels
        entre les entités.
        Si une collision survient, le résultat dépend de l'état
        du joueur :
        - Invincible : le fantôme est mangé (passe en DeadState)
        et le score augmente.
        - Vulnérable : le joueur perd une vie, toutes les entités
        retournent à leur position de départ, et la phase d'introduction
        (gel de l'écran) est relancée.
        """

        if self.maze[self.pacman.y][self.pacman.x] & 16:
            self.score += self.pts_pacgum
            self.maze[self.pacman.y][self.pacman.x] &= ~16
            self.dots_left -= 1
        if self.maze[self.pacman.y][self.pacman.x] & 32:
            self.score += self.pts_super_pacgum
            self.maze[self.pacman.y][self.pacman.x] &= ~32
            self.dots_left -= 1
            self.pacman.is_powered = True
            self.power_start_time = pygame.time.get_ticks()
        for ghost in self.ghosts:
            if not isinstance(ghost.state, (DeadState, WaitingState)):
                distance = ghost.position.distance_to(self.pacman.position)
                if distance < (constants.TILE_SIZE // 2):
                    if self.pacman.is_powered:
                        ghost.state = DeadState()
                        self.score += self.pts_ghost
                    else:
                        self.pacman.lives -= 1
                        self.pacman.x = self.pacman.start_x
                        self.pacman.y = self.pacman.start_y
                        self.pacman.position.x = self.pacman.start_x *\
                            constants.TILE_SIZE
                        self.pacman.position.y = self.pacman.start_y *\
                            constants.TILE_SIZE
                        for g in self.ghosts:
                            g.x = g.start_x
                            g.y = g.start_y
                            g.position.x = g.start_x * constants.TILE_SIZE
                            g.position.y = g.start_y * constants.TILE_SIZE
                            g.direction = g.start_direction
                            g.state = ChasingState()
                        self.in_intro = True
                        self.intro_start_ticks = pygame.time.get_ticks()
                        return

    def draw_pause(self) -> None:
        """
        Applique un voile semi-transparent sur l'écran et affiche
        l'interface de pause.

        Cette méthode superpose une surface noire avec une opacité
        partielle (alpha 150) par-dessus le rendu visuel actuel du jeu
        pour assombrir l'action. Elle dessine ensuite le texte "PAUSE"
        ainsi que les indications clavier pour reprendre la partie ou
        retourner au menu principal.
        """
        overlay = pygame.Surface((self.screen.get_width(),
                                  self.screen.get_height()))
        overlay.set_alpha(150)  # Transparence (0 à 255)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        font_pause = pygame.font.SysFont("Arial", 50, bold=True)
        text_surf = font_pause.render("PAUSE", True, (0, 204, 204))
        text_rect = text_surf.get_rect(center=(self.screen.get_width() // 2,
                                               self.screen.get_height()
                                               // 2 - 40))
        self.screen.blit(text_surf, text_rect)

        font_sub = pygame.font.SysFont("Arial", 22)
        sub_surf = font_sub.render("ENTRÉE = Reprendre  |  ÉCHAP = Quitter",
                                   True, (255, 255, 255))
        sub_rect = sub_surf.get_rect(center=(self.screen.get_width() // 2,
                                             self.screen.get_height()
                                             // 2 + 20))
        self.screen.blit(sub_surf, sub_rect)

    def _draw_walls(self,
                    x: int,
                    y: int,
                    cell_value: int,
                    color: tuple[int, int, int]) -> None:
        """
        Dessine les murs (bordures) d'une cellule spécifique en
        fonction de son masque binaire.

        Cette méthode convertit les coordonnées de la grille (tuiles)
        en pixels réels sur l'écran, en appliquant un décalage vertical
        pour ne pas empiéter sur l'interface utilisateur (HUD).
        Elle utilise des opérations bit à bit sur `cell_value` pour
        déterminer quels côtés de la cellule doivent être tracés
        (1 = Nord, 2 = Est, 4 = Sud, 8 = Ouest).

        Args:
            x: L'index de la colonne de la cellule sur la grille.
            y: L'index de la ligne de la cellule sur la grille.
            cell_value: L'entier représentant la configuration des
            murs via ses bits.
            color: Le tuple RGB (Rouge, Vert, Bleu) définissant
            la couleur des lignes.
        """
        x_px = x * constants.TILE_SIZE
        y_px = y * constants.TILE_SIZE + constants.HUD_HEIGHT
        w = 5  # Épaisseur visuelle

        if cell_value & 1:
            pygame.draw.line(self.screen,
                             color,
                             (x_px, y_px),
                             (x_px + constants.TILE_SIZE, y_px),
                             w)
        if cell_value & 2:
            pygame.draw.line(self.screen,
                             color,
                             (x_px + constants.TILE_SIZE,
                              y_px),
                             (x_px + constants.TILE_SIZE,
                              y_px + constants.TILE_SIZE),
                             w)
        if cell_value & 4:
            pygame.draw.line(self.screen,
                             color,
                             (x_px,
                              y_px + constants.TILE_SIZE),
                             (x_px + constants.TILE_SIZE,
                              y_px + constants.TILE_SIZE),
                             w)
        if cell_value & 8:
            pygame.draw.line(self.screen, color,
                             (x_px, y_px),
                             (x_px, y_px + constants.TILE_SIZE),
                             w)

    def draw(self) -> None:
        """
        Gère le rendu graphique complet de la frame actuelle
        (labyrinthe, entités et HUD).

        Cette méthode effectue le dessin de l'écran en plusieurs
        couches successives :
        1. Le labyrinthe : dessine le fond spécifique au motif "42",
        place les pacgums et super-pacgums, puis trace les murs
        (bleus classiques et turquoise pour le motif).
        2. Les fantômes : sélectionne et affiche le sprite approprié selon
        leur état (clignotement de fin d'invincibilité en mode Frightened,
        yeux seuls en mode Dead, ou animation normale).
        3. Le joueur : affiche le sprite de Pac-Man correspondant à sa
        direction actuelle.
        4. L'interface (HUD) : génère et positionne dynamiquement le score,
        le niveau, le temps restant et les icônes des vies
        (redimensionnées proportionnellement).
        """
        # Passage 1 : Dessin du fond blanc pour le 42 et placement des pacgums
        for y, row in enumerate(self.maze):
            for x, cell_value in enumerate(row):
                x_px = x * constants.TILE_SIZE
                y_px = y * constants.TILE_SIZE + constants.HUD_HEIGHT

                # Le pattern 42 est identifié par la valeur de cellule 15
                if cell_value == 15:
                    pygame.draw.rect(self.screen,
                                     (255, 255, 255),
                                     (x_px,
                                      y_px,
                                      constants.TILE_SIZE,
                                      constants.TILE_SIZE))

                if cell_value & 16:
                    pygame.draw.circle(self.screen,
                                       (255, 184, 174),
                                       (x_px + (constants.TILE_SIZE // 2),
                                        y_px + (constants.TILE_SIZE // 2)),
                                       2)
                if cell_value & 32:
                    pygame.draw.circle(self.screen,
                                       (255, 0, 0),
                                       (x_px + (constants.TILE_SIZE // 2),
                                        y_px + (constants.TILE_SIZE // 2)),
                                       4)

        # Passage 2 : Dessin des murs classiques (bleus)
        for y, row in enumerate(self.maze):
            for x, cell_value in enumerate(row):
                if cell_value != 15:
                    self._draw_walls(x, y, cell_value, (0, 0, 255))

        # Passage 3 : Dessin des murs du pattern 42
        # (Turquoise de l'école) par dessus le bleu
        for y, row in enumerate(self.maze):
            for x, cell_value in enumerate(row):
                if cell_value == 15:
                    self._draw_walls(x, y, cell_value, (0, 204, 204))

        for ghost in self.ghosts:
            if isinstance(ghost.state, WaitingState):
                continue
            ghost_x = ghost.position.x
            ghost_y = ghost.position.y + constants.HUD_HEIGHT
            anim_index = int((ghost.position.x + ghost.position.y) // 8) % 2
            if isinstance(ghost.state, FrightenedState):
                time_active = pygame.time.get_ticks() - self.power_start_time
                if time_active > 8000:
                    if (time_active // 200) % 2 == 0:
                        ghost_sprite = self.scar_gh_sprites[anim_index]
                    else:
                        ghost_sprite = self.scar_gh_sprites[2 + anim_index]
                else:
                    ghost_sprite = self.scar_gh_sprites[2 + anim_index]
            elif isinstance(ghost.state, DeadState):
                ghost_sprite =\
                    self.dead_gh_sprites[ghost.direction][anim_index]
            else:
                ghost_sprite = ghost.sprites[ghost.direction][anim_index]
            self.screen.blit(ghost_sprite, (ghost_x, ghost_y))

        current_sprite = self.pacman.sprites[int(self.pacman.frame_index)]
        self.screen.blit(current_sprite,
                         (self.pacman.position.x,
                          self.pacman.position.y + constants.HUD_HEIGHT))

        # CONFIGURATION DE LA BARRE DU HAUT (HUD)
        y1 = 2
        y2 = 40
        screen_width = self.screen.get_width()

        score_surf = self.font.render(f"Score: {self.score}",
                                      True,
                                      (255, 255, 255))
        self.screen.blit(score_surf, (10, y1))

        # Gestion Dynamique des Vies - TAILLE RÉDUITE
        num_lives = self.pacman.lives
        if num_lives > 0:
            lives_text_surf = self.font.render("Lives:", True, (255, 255, 255))

            # Réduction à 60% de la taille d'une Tile normale
            icon_w = int(constants.TILE_SIZE * 0.6)
            space_lives = icon_w + 8
            calculus_lives: int = (num_lives - 1) * space_lives
            x_leftmost_icon = screen_width - icon_w - (calculus_lives)
            lives_text_x = x_leftmost_icon - lives_text_surf.get_width() - 5

            if lives_text_x > (score_surf.get_width() + 20):
                self.screen.blit(lives_text_surf, (lives_text_x, y1))

            # Transformation de la taille du sprite de vie
            scaled_life_icon = pygame.transform.scale(
                self.theme_sprites["PLAYER"]["E"][1],
                (icon_w, icon_w))
            scaled_life_icon_bg_color = scaled_life_icon.get_at((0, 0))
            scaled_life_icon.set_colorkey(scaled_life_icon_bg_color)

            for i in range(num_lives):
                icon_x = screen_width - icon_w - (i * space_lives)
                self.screen.blit(scaled_life_icon, (icon_x, y1))

        lvl_surf = self.font.render(f"Level: {self.current_lvl}",
                                    True,
                                    (255, 255, 255))
        self.screen.blit(lvl_surf, (10, y2))

        time_surf = self.font.render(f"Time: {self.time_left}s",
                                     True,
                                     (255, 255, 255))
        self.screen.blit(time_surf,
                         (screen_width - time_surf.get_width() - 10, y2))
