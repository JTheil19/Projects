import pygame
import sys
import Func as f

pygame.init()

fenetre_largeur = 800
fenetre_hauteur = 600
fenetre = pygame.display.set_mode((fenetre_largeur, fenetre_hauteur))
pygame.display.set_caption("Démineur")

police = pygame.font.Font(None, 36)

grille_originale = None

def main():
    global grille_originale #permets de modifier la variable en dehors de la fonction

    mode = f.choix_mode(fenetre, police, fenetre_largeur)
    print("mode selectioné:", mode)

    if mode == "easy":
        lignes=9
        colonne=9
        nb_mines=10
    elif mode == "normal":
        lignes=16
        colonne=16
        nb_mines=40
    elif mode == "hard":
        lignes=16
        colonne=30
        nb_mines=99
    else:
        return

    largeur_case = fenetre_largeur // colonne
    hauteur_case = fenetre_hauteur // lignes

    grille = f.creation_grille(lignes, colonne)
    f.place_mines(grille, nb_mines)
    f.ajout_nombre_mines_autour_grille(grille)

    grille_originale = []
    for rangée in grille:
        grille_originale.append(rangée[:])

    revélé = []
    for j in range(lignes):
        ligne = [False] * colonne
        revélé.append(ligne)

    jeu_perdu = False
    while True:
        fenetre.fill(f.BLANC)
        f.afficher_grille(fenetre, grille, largeur_case, hauteur_case, revélé)
        
        if jeu_perdu:
            if all(revélé[i][j] or grille[i][j] == "X" for i in range(lignes) for j in range(colonne)):
                message = "Vous avez gagné!"
            else:
                message = "Vous avez perdu!"
            
            if f.fenetre_jeu_perdu(fenetre, fenetre_largeur, fenetre_hauteur, message):
                main()

        pygame.display.update()

        for click in pygame.event.get():
            if click.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif click.type == pygame.MOUSEBUTTONDOWN:
                if click.button == 1: #clique gauche
                    x, y = click.pos
                    colonne = x // largeur_case
                    ligne = y // hauteur_case
                    if not revélé[ligne][colonne]:
                        if grille[ligne][colonne] == "X":
                            jeu_perdu = True
                        else:
                            f.reveler_case(grille, revélé, ligne, colonne)
                elif click.button == 3: #clique droit
                    x, y = click.pos
                    colonne = x // largeur_case
                    ligne = y // hauteur_case
                    if not revélé[ligne][colonne]:
                        f.marquer_case(grille, revélé,grille_originale, ligne, colonne) 

            if f.jeu_gagné(grille, revélé, nb_mines):
                message = "Vous avez gagné!"
                if f.fenetre_jeu_perdu(fenetre, fenetre_largeur, fenetre_hauteur, message):
                    main()


if __name__ == "__main__":
    main()
