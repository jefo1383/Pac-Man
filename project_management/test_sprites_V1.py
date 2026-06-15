import pygame
import sys

pygame.init()
# On agrandit la fenêtre pour avoir un bon plan de travail
screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption("Sandbox : Debugger de Sprites")

try:
    sheet = pygame.image.load("PacMan.gif").convert()
    bg_color = sheet.get_at((0, sheet.get_height() - 1))
    print(f"{bg_color}")
    sheet.set_colorkey(bg_color)
except FileNotFoundError:
    print("Erreur : Fichier introuvable.")
    sys.exit()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((40, 40, 40))

    # 1. On affiche la feuille originale en haut à gauche
    screen.blit(sheet, (10, 10))

    # --- LA ZONE DE CONTRÔLE (À modifier) ---
    # Aligne ces carrés rouges avec les Pac-Man de la première ligne !
    start_x = 55     # Essaie de le décaler (ex: 1, 2, 3...)
    start_y = 24    # Essaie de le descendre (ex: 1, 2, 3...)
    largeur = 18    # Parfois les sprites font 13x13 ou 14x14 !
    hauteur = 18
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

    pygame.display.flip()

pygame.quit()
