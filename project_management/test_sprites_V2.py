import pygame
import sys
from constants import SPRITE_ATLAS

pygame.init()
# On agrandit la fenêtre pour avoir un bon plan de travail
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Sandbox : Debugger de Sprites")

try:
    sheet = pygame.image.load("PacMan.gif").convert()
    bg_color = sheet.get_at((0, sheet.get_height() - 1))
    sheet.set_colorkey(bg_color)
except FileNotFoundError:
    print("Erreur : Fichier introuvable.")
    sys.exit()

running = True
keys_list: list[str] = list(SPRITE_ATLAS.keys())
current_index: int = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                current_index = (current_index + 1) % len(keys_list)
            elif event.key == pygame.K_DOWN:
                current_index = (current_index - 1) % len(keys_list)
        elif event.type == pygame.QUIT:
            running = False

    screen.fill((40, 40, 40))

    # 1. On affiche la feuille originale en haut à gauche
    screen.blit(sheet, (10, 10))

    # --- LA ZONE DE CONTRÔLE (À modifier) ---
    # Aligne ces carrés rouges avec les Pac-Man de la première ligne !
    key_name: str = keys_list[current_index]
    start_x, start_y, largeur, hauteur = SPRITE_ATLAS[key_name]
    # ----------------------------------------

    # 2. La boucle de test
    rect_x = 10 + start_x  # Le +10 c'est la marge de l'écran
    rect_y = 10 + start_y

    # On dessine le CADRE ROUGE sur l'image originale (épaisseur 1)
    pygame.draw.rect(screen,
                     (255, 0, 0),
                     (rect_x, rect_y, largeur, hauteur),
                     1)

    # On découpe et on affiche en énorme en dessous pour vérifier
    try:
        # On utilise les vraies coordonnées pour le subsurface
        real_rect_x = start_x
        frame = sheet.subsurface(pygame.Rect(real_rect_x,
                                             start_y,
                                             largeur,
                                             hauteur))
        scaled_frame = pygame.transform.scale(frame, (64, 64))  # Zoom x4

        screen.blit(scaled_frame, (100, 100))
    except ValueError:
        pass  # On ignore si le rectangle sort de l'image pendant tes tests

    # Création de la police d'écriture (à l'extérieur de la boucle c'est mieux,
    # mais pour tester ça passe !)
    font = pygame.font.SysFont("Arial", 24)
    # Rendu du texte avec le nom de la clé (en blanc)
    text_surface = font.render(key_name, True, (255, 255, 255))
    # Affichage au-dessus de ton sprite zoomé
    screen.blit(text_surface, (100, 60))
    pygame.display.flip()

pygame.quit()
