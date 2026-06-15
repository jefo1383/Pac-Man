from abc import ABC, abstractmethod
import random
from player import Direction, Player
from constants import TILE_SIZE
import pygame


class Ghost(ABC):
    """
    Classe de base abstraite représentant un fantôme.

    Gère les déplacements, la gestion des états (State
    Pattern) et les collisions avec le labyrinthe.
    """
    def __init__(self, start_x: int,
                 start_y: int,
                 maze: list[list[int]],
                 target: tuple[int, int],
                 direction: str,
                 ghost_sprites: dict[str,
                                     list[pygame.surface.Surface]]) -> None:
        """
        Initialise un fantôme avec sa position et ses sprites.

        Args:
            start_x: La coordonnée X de départ sur la grille.
            start_y: La coordonnée Y de départ sur la grille.
            maze: La matrice représentant le labyrinthe.
            target: La cible initiale du fantôme.
            direction: La direction de départ (N, S, E, W).
            ghost_sprites: Les sprites animés du personnage.
        """
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x
        self.y = start_y
        self.state: 'GhostState' = ChasingState()
        self.maze = maze
        self.target = target
        self.direction = direction
        self.start_direction = direction
        self.position = pygame.math.Vector2(start_x * TILE_SIZE,
                                            start_y * TILE_SIZE)
        self.speed: float = 2.5
        self.sprites: dict[str, list[pygame.surface.Surface]] = ghost_sprites
        self.skip_move_counter: int = 0

    def _get_valid_moves(self) -> list[tuple[str, int, int]]:
        """
        Détermine les mouvements possibles depuis la position.

        Le fantôme ne fait jamais demi-tour directement, sauf
        s'il se retrouve coincé dans une impasse.

        Returns:
            Une liste de tuples contenant la direction, la
            coordonnée X future et la coordonnée Y future.
        """
        directions = {
            "N": (0, -1, 1, "S"),
            "S": (0, 1, 4, "N"),
            "E": (1, 0, 2, "W"),
            "W": (-1, 0, 8, "E")
        }
        valid_moves = []
        for dir_key, (dx, dy, wall, opposite) in directions.items():
            nx = self.x + dx
            ny = self.y + dy
            if opposite != self.direction and not self.maze[self.y][self.x]\
                    & wall:
                valid_moves.append((dir_key, nx, ny))
        if not valid_moves:
            for dir_key, (dx, dy, wall, opposite) in directions.items():
                nx = self.x + dx
                ny = self.y + dy
                if not self.maze[self.y][self.x] & wall:
                    valid_moves.append((dir_key, nx, ny))
        return valid_moves

    def move(self, pacman: Player) -> None:
        """
        Gère le déplacement du fantôme à chaque frame.

        Appelle la logique de l'état actuel dès que le
        fantôme est parfaitement aligné sur la grille.

        Args:
            pacman: L'instance du joueur pour ajuster l'IA.
        """
        if isinstance(self.state, FrightenedState):
            self.skip_move_counter += 1
            if self.skip_move_counter >= 3:
                self.skip_move_counter = 0
                return
        x: float = self.position.x
        y: float = self.position.y
        if x % TILE_SIZE == 0 and y % TILE_SIZE == 0:
            self.state.execute_move(self, pacman)
        self.update_position()

    def check_state(self, pacman: Player) -> None:
        """
        Vérifie et met à jour l'état actuel du fantôme.

        Bascule entre les états Chasing et Frightened selon
        le statut de puissance (Super-Pacgum) de Pac-Man.

        Args:
            pacman: L'instance du joueur ciblée.
        """
        if isinstance(self.state, (DeadState, WaitingState)):
            return
        if pacman.is_powered:
            if not isinstance(self.state, FrightenedState):
                self.state = FrightenedState()
        else:
            if not isinstance(self.state, ChasingState):
                self.state = ChasingState()

    def update_position(self) -> None:
        """
        Mise à jour mathématique de la position du fantôme.

        Modifie les coordonnées vectorielles selon la vitesse
        et la direction courante.
        """
        match self.direction:
            case "N":
                self.position.y -= self.speed
            case "S":
                self.position.y += self.speed
            case "W":
                self.position.x -= self.speed
            case "E":
                self.position.x += self.speed
            case "STOP":
                pass

    def get_bfs_distance(self,
                         start_x: int,
                         start_y: int,
                         target_x: int,
                         target_y: int) -> int:
        """
        Calcule la vraie distance vers une cible (via BFS).

        Args:
            start_x: Coordonnée X de départ.
            start_y: Coordonnée Y de départ.
            target_x: Coordonnée X de la cible.
            target_y: Coordonnée Y de la cible.

        Returns:
            La distance calculée en nombre de cases.
        """
        queue = [(start_x, start_y, 0)]
        visited = {(start_x, start_y)}
        directions = [(0, -1, 1), (0, 1, 4), (1, 0, 2), (-1, 0, 8)]

        while queue:
            cx, cy, dist = queue.pop(0)
            if cx == target_x and cy == target_y:
                return dist

            for dx, dy, wall in directions:
                if not self.maze[cy][cx] & wall:
                    nx, ny = cx + dx, cy + dy
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny, dist + 1))

        return 9999  # Sécurité au cas où aucun chemin n'est trouvé

    @abstractmethod
    def get_target(self, pacman: Player) -> tuple[int, int]:
        """
        Détermine la case cible du fantôme (Méthode abstraite).

        Args:
            pacman: Le joueur ciblé.

        Returns:
            Les coordonnées (X, Y) de la cible visée.
        """
        pass


class Blinky(Ghost):

    def __init__(self,
                 start_x: int,
                 start_y: int,
                 maze: list[list[int]],
                 target: tuple[int, int],
                 direction: str,
                 ghost_sprites: dict[str,
                                     list[pygame.surface.Surface]]) -> None:
        """
        Initialise un fantôme avec sa position et ses sprites.

        Args:
            start_x: La coordonnée X de départ sur la grille.
            start_y: La coordonnée Y de départ sur la grille.
            maze: La matrice représentant le labyrinthe.
            target: La cible initiale du fantôme.
            direction: La direction de départ (N, S, E, W).
            ghost_sprites: Les sprites animés du personnage.
        """
        super().__init__(start_x,
                         start_y,
                         maze,
                         target,
                         direction,
                         ghost_sprites)

    def get_target(self, pacman: Player) -> tuple[int, int]:
        """
        Cible directement la position actuelle de Pac-Man.

        Args:
            pacman: L'instance du joueur ciblé.

        Returns:
            La position exacte (X, Y) du joueur.
        """
        return (pacman.x, pacman.y)


class Pinky(Ghost):

    def __init__(self,
                 start_x: int,
                 start_y: int,
                 maze: list[list[int]],
                 target: tuple[int, int],
                 direction: str,
                 ghost_sprites: dict[str,
                                     list[pygame.surface.Surface]]) -> None:
        """
        Initialise un fantôme avec sa position et ses sprites.

        Args:
            start_x: La coordonnée X de départ sur la grille.
            start_y: La coordonnée Y de départ sur la grille.
            maze: La matrice représentant le labyrinthe.
            target: La cible initiale du fantôme.
            direction: La direction de départ (N, S, E, W).
            ghost_sprites: Les sprites animés du personnage.
        """
        super().__init__(start_x,
                         start_y,
                         maze,
                         target,
                         direction,
                         ghost_sprites)

    def get_target(self, pacman: Player) -> tuple[int, int]:
        """
        Anticipe les mouvements en visant 4 cases en avant.

        Args:
            pacman: L'instance du joueur ciblé.

        Returns:
            La case (X, Y) située devant le joueur.
        """
        dir_target = {
            Direction.N: (0, -1),
            Direction.S: (0, 1),
            Direction.E: (1, 0),
            Direction.W: (-1, 0)
        }
        if pacman.direction == Direction.STOP:
            return (pacman.x, pacman.y)
        tar_x, tar_y = dir_target[pacman.direction]
        return (pacman.x + (tar_x * 4), pacman.y + (tar_y * 4))


class Clyde(Ghost):

    def __init__(self,
                 start_x: int,
                 start_y: int,
                 maze: list[list[int]],
                 target: tuple[int, int],
                 direction: str,
                 ghost_sprites: dict[str,
                                     list[pygame.surface.Surface]]) -> None:
        """
        Initialise un fantôme avec sa position et ses sprites.

        Args:
            start_x: La coordonnée X de départ sur la grille.
            start_y: La coordonnée Y de départ sur la grille.
            maze: La matrice représentant le labyrinthe.
            target: La cible initiale du fantôme.
            direction: La direction de départ (N, S, E, W).
            ghost_sprites: Les sprites animés du personnage.
        """
        super().__init__(start_x,
                         start_y,
                         maze,
                         target,
                         direction,
                         ghost_sprites)

    def get_target(self, pacman: Player) -> tuple[int, int]:
        """
        Alterne entre chasse et fuite selon la distance.

        S'approche de Pac-Man, mais retourne dans son coin
        s'il se trouve à moins de 8 cases de lui.

        Args:
            pacman: L'instance du joueur ciblé.

        Returns:
            Les coordonnées (X, Y) de sa cible dynamique.
        """
        dist = abs(pacman.x - self.x) + abs(pacman.y - self.y)
        limit = 8
        if (len(self.maze) * len(self.maze[0])) <= 100:
            limit = 6
        if dist > limit:
            return (pacman.x, pacman.y)
        return (0, len(self.maze) - 1)


class Inky(Ghost):

    def __init__(self,
                 start_x: int,
                 start_y: int,
                 maze: list[list[int]],
                 target: tuple[int, int],
                 direction: str,
                 ghost_sprites: dict[str,
                                     list[pygame.surface.Surface]]) -> None:
        """
        Initialise un fantôme avec sa position et ses sprites.

        Args:
            start_x: La coordonnée X de départ sur la grille.
            start_y: La coordonnée Y de départ sur la grille.
            maze: La matrice représentant le labyrinthe.
            target: La cible initiale du fantôme.
            direction: La direction de départ (N, S, E, W).
            ghost_sprites: Les sprites animés du personnage.
        """
        super().__init__(start_x,
                         start_y,
                         maze,
                         target,
                         direction,
                         ghost_sprites)
        self.target_choice: tuple[int, int] | None = None
        self.timer = 0

    def get_target(self, pacman: Player) -> tuple[int, int]:
        """
        Choisit une cible aléatoire autour de Pac-Man.

        Change de cible automatiquement toutes les 3 secondes
        (soit toutes les 9 cases parcourues).

        Args:
            pacman: L'instance du joueur ciblé.

        Returns:
            Les coordonnées (X, Y) de la cible choisie.
        """
        options = [(pacman.x + 3, pacman.y), (pacman.x - 3, pacman.y),
                   (pacman.x, pacman.y + 3), (pacman.x, pacman.y - 3)]
        if self.target_choice is None or self.timer >= 9:
            target = random.choice(options)
            self.target_choice = target
            self.timer = 0
        else:
            self.timer += 1
        return self.target_choice


class GhostState(ABC):
    """
    Classe de base pour l'architecture en États (State).
    """
    @abstractmethod
    def execute_move(self, ghost: Ghost, pacman: Player) -> None:
        """
        Exécute la logique de déplacement (Méthode abstraite).

        Args:
            ghost: L'instance du fantôme à déplacer.
            pacman: L'instance du joueur ciblé.
        """
        pass


class ChasingState(GhostState):
    """
    État de chasse : le fantôme poursuit sa cible spécifique.
    """
    def execute_move(self, ghost: Ghost, pacman: Player) -> None:
        """
        Sélectionne le meilleur chemin vers la cible de l'IA.

        Args:
            ghost: L'instance du fantôme à déplacer.
            pacman: L'instance du joueur ciblé.
        """
        ghost.target = ghost.get_target(pacman)
        options = ghost._get_valid_moves()
        if len(options) == 1:
            ghost.direction, ghost.x, ghost.y = options[0]
        else:
            dist_options = []
            px, py = ghost.target
            for cell in options:
                dir, x, y = cell
                distance = (px - x)**2 + (py - y)**2
                dist_options.append((dir, x, y, distance))
            dice = random.randint(1, 100)
            if dice <= 75:
                shortest = min(dist_options, key=lambda opt: opt[3])
            else:
                shortest = random.choice(dist_options)
            ghost.direction, ghost.x, ghost.y, _ = shortest


class FrightenedState(GhostState):
    """
    État de fuite : le fantôme erre de manière aléatoire.
    """
    def execute_move(self, ghost: Ghost, pacman: Player) -> None:
        """
        Choisit une direction valide au hasard aux intersections.

        Args:
            ghost: L'instance du fantôme apeuré.
            pacman: L'instance du joueur (non utilisée ici).
        """
        options = ghost._get_valid_moves()
        if len(options) == 1:
            ghost.direction, ghost.x, ghost.y = options[0]
        else:
            ghost.direction, ghost.x, ghost.y = random.choice(options)


class DeadState(GhostState):
    """
    État mort : le fantôme retourne rapidement à sa base.
    """
    def execute_move(self, ghost: Ghost, pacman: Player) -> None:
        """
        Calcule le chemin le plus court vers le point de départ.

        Ressuscite ou se met en attente une fois arrivé.

        Args:
            ghost: L'instance du fantôme vaincu.
            pacman: L'instance du joueur.
        """
        if ghost.x == ghost.start_x and ghost.y == ghost.start_y:
            if pacman.is_powered:
                # Si Pac-Man est toujours puissant, on passe en attente
                ghost.state = WaitingState()
                ghost.direction = "STOP"
            else:
                ghost.state = ChasingState()
                ghost.state.execute_move(ghost, pacman)
            return
        ghost.target = (ghost.start_x, ghost.start_y)
        options = ghost._get_valid_moves()
        if len(options) == 1:
            ghost.direction, ghost.x, ghost.y = options[0]
        else:
            dist_options = []
            for cell in options:
                dir, x, y = cell
                distance = ghost.get_bfs_distance(x,
                                                  y,
                                                  ghost.target[0],
                                                  ghost.target[1])
                dist_options.append((dir, x, y, distance))
            shortest = min(dist_options, key=lambda opt: opt[3])
            ghost.direction, ghost.x, ghost.y, _ = shortest


class WaitingState(GhostState):
    """
    État d'attente : le fantôme attend dans sa base.
    """
    def execute_move(self, ghost: Ghost, pacman: Player) -> None:
        """
        Patiente tant que Pac-Man est super-puissant.

        Repasse en mode chasse dès que l'effet se dissipe.

        Args:
            ghost: L'instance du fantôme en attente.
            pacman: L'instance du joueur pour vérifier l'effet.
        """
        # Tant que Pac-Man est super-puissant, le fantôme reste immobile
        if not pacman.is_powered:
            # Dès que l'effet se termine, le fantôme reprend la chasse !
            ghost.state = ChasingState()
            ghost.direction = ghost.start_direction
            ghost.state.execute_move(ghost, pacman)
