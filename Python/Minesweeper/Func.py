import pygame
import sys
import random

pygame.init()

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (200, 200, 200)
ROUGE = (255, 0, 0)

police = pygame.font.Font(None, 36)

def afficher_texte(fenetre, texte, police, couleur, x, y):
    texte_surface = police.render(texte, True, couleur)
    texte_rectangle = texte_surface.get_rect(center=(x, y))
    fenetre.blit(texte_surface, texte_rectangle)

def choix_mode(fenetre, police, largeur_fenetre):
    while True:
        fenetre.fill(BLANC)
        afficher_texte(fenetre, "Select Mode", police, NOIR, largeur_fenetre // 2, 100)

        rectangle_easy = pygame.Rect(largeur_fenetre // 2 - 100, 200, 200, 50)
        rectangle_noraml = pygame.Rect(largeur_fenetre // 2 - 100, 300, 200, 50)
        rectangle_hard = pygame.Rect(largeur_fenetre // 2 - 100, 400, 200, 50)
         
        pygame.draw.rect(fenetre, GRIS, rectangle_easy)
        pygame.draw.rect(fenetre, GRIS, rectangle_noraml)
        pygame.draw.rect(fenetre, GRIS, rectangle_hard)

        afficher_texte(fenetre, "Easy", police, NOIR, largeur_fenetre // 2, 225)
        afficher_texte(fenetre, "Normal", police, NOIR, largeur_fenetre // 2, 325)
        afficher_texte(fenetre, "Hard", police, NOIR, largeur_fenetre // 2, 425)

        pygame.display.update()

        for click in pygame.event.get():
            if click.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif click.type == pygame.MOUSEBUTTONDOWN:
                if click.button == 1:
                    x, y = pygame.mouse.get_pos()
                    if rectangle_easy.collidepoint(x, y):
                        return "easy"
                    elif rectangle_noraml.collidepoint(x, y):
                        return "normal"
                    elif rectangle_hard.collidepoint(x, y):
                        return "hard"


def creation_grille(lignes, colonnes):
    grille = [[0] * colonnes for _ in range(lignes)]
    return grille

def place_mines(grille, nb_mines):
    lignes = len(grille)
    colonnes = len(grille[0])
    mines_placées = 0
    while mines_placées < nb_mines:
        ligne = random.randint(0, lignes - 1)
        colonne = random.randint(0, colonnes - 1)
        if grille[ligne][colonne] != "X":
            grille[ligne][colonne] = "X"
            mines_placées += 1

def nombre_mines_autour(grille, ligne, colonne):
    compteur = 0
    lignes = len(grille)
    colonnes = len(grille[0])
    for i in range(ligne-1,ligne+2):
        for j in range(colonne-1,colonne+2):
            if 0 <= i < lignes and 0 <= j < colonnes and grille[i][j] == "X":
                compteur += 1
    return compteur

def ajout_nombre_mines_autour_grille(grille):
    lignes = len(grille)
    colonnes = len(grille[0])
    for i in range(lignes):
        for j in range(colonnes):
            if grille[i][j] != "X":
                compteur = nombre_mines_autour(grille,i,j)
                grille[i][j] = compteur

def afficher_grille(fenetre,grille,largeur_case,hauteur_case,révélé):
    lignes = len(grille)
    colonnes = len(grille[0])
    for i in range(lignes):
        for j in range(colonnes):
            rectangle = pygame.Rect(j * largeur_case, i * hauteur_case, largeur_case, hauteur_case)
            pygame.draw.rect(fenetre, NOIR, rectangle, 1)
            if révélé[i][j]:
                if grille[i][j] == "X":
                    pygame.draw.circle(fenetre, ROUGE, (j * largeur_case + largeur_case // 2, i * hauteur_case + hauteur_case // 2), 10)
                else:
                    text = police.render(str(grille[i][j]), True, NOIR)
                    text_rect = text.get_rect(center=(j * largeur_case + largeur_case // 2, i * hauteur_case + hauteur_case // 2))
                    fenetre.blit(text, text_rect)
            elif grille[i][j] == "M":  # Display marked cells
                pygame.draw.rect(fenetre, GRIS, rectangle)
                pygame.draw.line(fenetre, NOIR, (j * largeur_case, i * hauteur_case), ((j + 1) * largeur_case, (i + 1) * hauteur_case), 3)
                pygame.draw.line(fenetre, NOIR, ((j + 1) * largeur_case, i * hauteur_case), (j * largeur_case, (i + 1) * hauteur_case), 3)


def reveler_case(grille, révélé, ligne, colonne):
    if révélé[ligne][colonne]:
        return
    révélé[ligne][colonne] = True
    if grille[ligne][colonne] == 0:
        lignes = len(grille)
        colonnes = len(grille[0])
        for i in range(ligne - 1, ligne + 2):
            for j in range(colonne - 1, colonne + 2):
                if 0 <= i < lignes and 0 <= j < colonnes:
                    reveler_case(grille, révélé, i, j)

def fenetre_jeu_perdu(fenetre, largeur_fenetre, hauteur_fenetre, message):
    while True:
        fenetre.fill(BLANC)
        afficher_texte(fenetre, message, police, NOIR, largeur_fenetre // 2, hauteur_fenetre // 2 - 50)

        rentangle_restart = pygame.Rect(largeur_fenetre // 2 - 100, hauteur_fenetre // 2, 200, 50)
        pygame.draw.rect(fenetre, GRIS, rentangle_restart)
        afficher_texte(fenetre, "Restart", police, NOIR, largeur_fenetre // 2, hauteur_fenetre // 2 + 25)

        pygame.display.update()

        for click in pygame.event.get():
            if click.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif click.type == pygame.MOUSEBUTTONDOWN:
                if click.button == 1:
                    x, y = pygame.mouse.get_pos()
                    if rentangle_restart.collidepoint(x, y):
                        return True

def marquer_case(grille, révélé, grille_originale, ligne, colonnes, clique_gauche=False):
    if révélé[ligne][colonnes]: 
        return
    if clique_gauche:
        if grille[ligne][colonnes]!= "M":
            grille[ligne][colonnes] = "M"
    else:
        if grille[ligne][colonnes]!= "M":
            grille[ligne][colonnes] = "M"
        else:
            grille[ligne][colonnes] = grille_originale[ligne][colonnes] #reprend la case de depart


def jeu_gagné(grille, révélé, nb_mines):
    ligne = len(grille)
    colonne = len(grille[0])
    cases_non_révélées = sum(sum(1 for j in range(colonne) if not révélé[i][j]) for i in range(ligne))
    mines_marquées = sum(1 for i in range(ligne) for j in range(colonne) if grille[i][j] == "M")
    return cases_non_révélées == mines_marquées == nb_mines
