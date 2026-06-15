from enum import Enum
import pygame
from constants import TILE_SIZE


class Direction(Enum):
    N = "N"
    S = "S"
    W = "W"
    E = "E"
    STOP = "STOP"


class Player:

    def __init__(self, start_x: int, start_y: int,
                 theme_sprites: dict[str, list[pygame.surface.Surface]],
                 initial_lives: int = 3) -> None:
        """
        Initialise une nouvelle instance du joueur avec
        ses caractéristiques de base.

        Configure les coordonnées sur la grille et en pixels,
        la vitesse de déplacement, le nombre de vies, les sprites
        d'animation et l'état de puissance par défaut.

        Args:
            start_x: La coordonnée X initiale sur la grille.
            start_y: La coordonnée Y initiale sur la grille.
            theme_sprites: Un dictionnaire contenant les listes
            de sprites du joueur, organisées par direction.
            initial_lives: Le nombre de vies attribuées
            au départ (3 par défaut).
        """
        # 1. La Position
        self.x: int = start_x
        self.y: int = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.position: pygame.math.Vector2 = pygame.math.Vector2(
            start_x * TILE_SIZE,
            start_y * TILE_SIZE)
        self.speed: float = 2.5
        self.lives: int = initial_lives

        self.direction: Direction = Direction.STOP
        self.next_direction: Direction = Direction.STOP

        # 4. L'État de puissance (Le mode chasseur de fantômes)
        # False = Mode fuite normal
        # True = Mode Super-Pacgum (peut manger les fantômes)
        self.theme_sprites: dict[str,
                                 list[pygame.surface.Surface]] = theme_sprites
        self.is_powered: bool = False
        self.sprites: list[pygame.surface.Surface] = []
        self.frame_index: float = 0.0
        self.set_direction(Direction.STOP)

    def get_next_position(self) -> tuple[float, float]:
        """
        Calcule la position future sur la grille en fonction
        de la direction et de la vitesse actuelles.

        Returns:
            Un tuple contenant les futures coordonnées (x, y).
        """
        futur_pos = pygame.math.Vector2(self.position)
        match self.direction:
            case Direction.N:
                futur_pos.y -= self.speed
            case Direction.S:
                futur_pos.y += self.speed
            case Direction.W:
                futur_pos.x -= self.speed
            case Direction.E:
                futur_pos.x += self.speed
            case Direction.STOP:
                pass
        return (futur_pos.x, futur_pos.y)

    def move(self, maze: list[list[int]]) -> None:
        """
        Gère la logique de déplacement sur la grille avec
        détection des collisions.

        Le mouvement respecte trois règles principales :
        1. Les demi-tours sont immédiats (fluidité du contrôle).
        2. Les changements de direction à 90 degrés nécessitent
        un alignement parfait sur la case.
        3. Le mouvement est bloqué si un mur est détecté dans
        la direction actuelle.
        Si le mouvement est valide, les coordonnées sont mises à jour
        et l'animation est jouée.

        Args:
            maze: La matrice du niveau actuel
                où chaque cellule est un entier
                agissant comme un masque binaire
                (1=Nord, 2=Est, 4=Sud, 8=Ouest)
                pour représenter les murs.
        """
        is_aligned = (self.position.x % TILE_SIZE == 0
                      and self.position.y % TILE_SIZE == 0)
        current_x = int(self.position.x / TILE_SIZE)
        current_y = int(self.position.y / TILE_SIZE)
        # Detection de demi-tour
        is_u_turn = False
        if (self.direction == Direction.N and
                self.next_direction == Direction.S) or \
           (self.direction == Direction.S and
                self.next_direction == Direction.N) or \
           (self.direction == Direction.E and
                self.next_direction == Direction.W) or \
           (self.direction == Direction.W and
                self.next_direction == Direction.E):
            is_u_turn = True
        if is_u_turn:
            # Si c'est un demi-tour, on change de direction IMMÉDIATEMENT
            self.set_direction(self.next_direction)
            self.next_direction = Direction.STOP
        elif is_aligned and self.next_direction != Direction.STOP:
            next_wall: int = 0
            match self.next_direction:
                case Direction.N:
                    next_wall = 1
                case Direction.S:
                    next_wall = 4
                case Direction.W:
                    next_wall = 8
                case Direction.E:
                    next_wall = 2
            if (maze[current_y][current_x] & next_wall) == 0:
                self.set_direction(self.next_direction)
                self.next_direction = Direction.STOP
        wall_code = 0
        match self.direction:
            case Direction.N: wall_code = 1
            case Direction.S: wall_code = 4
            case Direction.W: wall_code = 8
            case Direction.E: wall_code = 2
            case Direction.STOP: wall_code = 0
        can_move = True
        if is_aligned and self.direction != Direction.STOP:
            if (maze[current_y][current_x] & wall_code) != 0:
                can_move = False
        if can_move:
            move_x, move_y = self.get_next_position()
            self.position.x = move_x
            self.position.y = move_y
            self.x = int(self.position.x / TILE_SIZE)
            self.y = int(self.position.y / TILE_SIZE)
            self.animate()

    def set_direction(self, new_direction: Direction) -> None:
        """
        Met à jour la direction de l'entité et charge
        ses sprites d'animation correspondants.

        Gère spécifiquement l'état d'arrêt : si la direction assignée
        est "STOP", l'orientation visuelle bascule par défaut vers
        l'Est ("E") pour conserver une posture d'attente valide à l'écran.

        Args:
            new_direction: La nouvelle direction (Enum)
            à appliquer au personnage.
        """
        self.direction = new_direction
        lettre = new_direction.name
        if lettre == "STOP":
            lettre = "E"
        self.sprites = self.theme_sprites[lettre]

    def animate(self) -> None:
        """
        Fait progresser l'animation de l'entité en mettant à jour
        l'index de la frame.

        L'index est incrémenté d'une valeur fractionnaire (0.2)
        pour contrôler la vitesse de lecture.
        S'il atteint ou dépasse le nombre d'images
        disponibles dans la liste des sprites actuels,
        il est réinitialisé à 0 pour créer une boucle continue.
        """
        # On augmente l'index. Plus la valeur est petite,
        # plus l'animation est lente.
        self.frame_index += 0.2
        # Le modulo (%) permet de revenir à 0 automatiquement
        # après la dernière frame
        if self.frame_index >= len(self.sprites):
            self.frame_index = 0.0

    def respawn(self, start_x: int, start_y: int) -> None:
        """
        Réinitialise le joueur à sa position de départ
        après la perte d'une vie.

        Cette méthode met à jour les coordonnées,
        décrémente le compteur de vies,
        stoppe tout mouvement en cours et annule l'effet d'invincibilité
        (super-pacgum) si le joueur était en mode chasseur.

        Args:
            start_x: La coordonnée X de réapparition sur la grille.
            start_y: La coordonnée Y de réapparition sur la grille.
        """
        self.x = start_x
        self.y = start_y
        self.lives -= 1
        self.direction = Direction.STOP
        self.is_powered = False
