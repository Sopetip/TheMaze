# coding: utf-8
import pygame

pygame.init()  # on initialise le pygame

Display = pygame.display.set_mode((800, 700))  # taille de l'écran
pygame.display.set_caption('The Maze')  # caption du programme
clock = pygame.time.Clock()  # on init la clock
bgImg = pygame.image.load('resources/main/themaze.png')  # on load les images du jeu
player = pygame.image.load('resources/main/player.png')
pygame.display.set_icon(player)

# il faut définir les couleurs dont on aura besoin
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (75, 75, 75)
darkgrey = (25, 25, 25)
darkblue = (0, 0, 90)

levelon = 1  # on déclare les variables
PCoords = [213, 228]  # on définit les coordonnées de base du joueur

lvl1 = ['d', 'd', 'r', 'u', 'u', 'r', 'r', 'r', 'r', 'r', 'd', 'l', 'd', 'l', 'u', 'l', 'd', 'd', 'd', 'd', 'l', 'l',
        'l', 'd', 'd', 'r', 'u', 'r', 'd', 'r', 'u', 'r', 'u', 'r', 'd', 'd', 'l']
wr_lvl1 = 4720

lvl2 = ['d', 'r', 'd', 'd', 'r', 'u', 'r', 'd', 'r', 'u', 'u', 'r', 'r', 'd', 'r', 'd', 'd', 'd', 'd', 'd', 'l', 'u',
        'l', 'd', 'l']
wr_lvl2 = 3836

lvl3 = ['d', 'r', 'r', 'd', 'l', 'd', 'd', 'r', 'd', 'r', 'r', 'u', 'r', 'd', 'd', 'l', 'd']
wr_lvl3 = 5000

wr_lvl = 0  # le world record du current lvl
current_lvl = lvl2
x = PCoords[0]
y = PCoords[1]
path = []  # le chemin parcouru par le joueur

crashed = False
error = False
win = False

start_time = 0
returned = ''
ms = 0


def truncate(n):  # fonction qui fait la troncature d'un float
    return int(n * 1000) / 1000

def test(dx, dy):
    Display.scroll(dx, dy)

def process_time(time):  # fonction qui prend la valeur du temps en ms et la rend en str de type m:s.ms
    global error, returned, ms
    ms = time
    if ms >= 119000:
        error = True
        crash('TEMPS ECOULE', ' ', 2000)
        reset()
    sec = ms / 1000
    minut = 0
    while sec / 60 > 1:
        minut += 1
        sec = truncate(sec - (minut * 60))
    returned = str(minut) + ':' + str(sec)
    return returned


def reset():  # on reset la taille du path, on relance le timer et on remet le personnage de façon normale
    global error, win
    path[:] = []  # selectionner tous les objets de la liste et les remplacer par la liste suivante: rien
    error, win = False, False


def text_objects(text, font, color):  # affiche un message et rend la valeur du message et le rectangle invisible.
    text_surface = font.render(text, False, color)
    return text_surface, text_surface.get_rect()


def disp_text(xpos, ypos, text, color, fontsize):  # fonction pour afficher un texte à l'écran
    fonnt = pygame.font.Font('resources/fonts/segoeui.ttf', fontsize)  # init la police
    show = fonnt.render(text, True, color)  # on affiche le texte
    showsq = show.get_rect()  # on obtient le rectangle (invisible) créé par l'affichage du texte
    showsq.center = (xpos, ypos)  # on le centre au coordonnées x et y
    Display.blit(show, showsq)  # on blit le message et le rectangle
    pygame.display.update()  # on update pour que le message apparaisse


def crash(text, text2, time):  # On affiche un message au mileu de l'écran.
    global x, y, PCoords
    thefont = pygame.font.Font('resources/fonts/impact.ttf', 65)
    font2 = pygame.font.Font('resources/fonts/segoeui.ttf', 32)
    x = PCoords[0]
    y = PCoords[1]
    pygame.time.wait(1)
    move_player(x, y)  # on reinitialise la place du joueur car crash veut dire que le joueur a soit gagné soit perdu

    text_surf, text_rect = text_objects(text, thefont, white)  # on obtient le text et le rectangle invisible
    text_rect.center = (400, 350)  # on centre

    text_surf1, text_rect1 = text_objects(text2, font2, white)
    text_rect1.center = (400, 550)

    Display.fill(black)  # on cache le jeu, pour afficher le message
    Display.blit(text_surf, text_rect)
    Display.blit(text_surf1, text_rect1)

    pygame.display.update()
    pygame.time.wait(time)  # on attends un peu pour que le message soit lisible


def check():  # on check si le dernier move du joueur correspond au move demandé par le niveau
    global error, win, start_time, x, y, PCoords, returned
    if len(path) == 0:  # on ne check pas si le joueur n'a pas bougé
        return [None]
    elif len(path) == 1:
        start_time = pygame.time.get_ticks()  # on lance la clock au moment du premier move

    i = len(path) - 1  # la liste commence à 0 pas à 1
    if path[i] != current_lvl[i]:  # le path est la suite de tous les mouvements du joueur
        error = True  # si le dernier mouvement est erroné il perd
    if len(path) == len(current_lvl) and not error:  # si le joueur a parcouru le labyrinthe sans échec, il gagne
        win = True

    if error:
        crash("BOOM", ' ', 250)  # on affiche le texte
        reset()
        return [None]

    if win:
        if ms <= wr_lvl2:
            crash("NOUVEAU RECORD", returned, 4000)
        else:
            crash("Gagné!", returned, 1000)

        won()
        reset()
    # print(path)


def move_player(xpos, ypos):
    Display.blit(player, (xpos, ypos))  # on blit le joueur à x et y
    # pygame.draw.rect(Display,blue,(x,y,x+25,y+25))


def move_down():  # les 4 fonctions de mouvements qui sont quasiment les mêmes.
    global y  # juste on bouge les coordonnées du player de 50 sur X ou Y
    y += 50
    path.append('d')  # ensuite on ajoute à la fin de la liste 'path' le dernier mouvement exécuté.

    if y > PCoords[1] + 399:  # on vérifie que le joueur n'a pas atteint les limites
        y = y - 50  # on retourne en arrière si c'est le cas
        del path[-1]
    if len(path) > 1:
        if path[-2] == 'u':  # si le joueur veut retourner sur ses pas il peu
            del path[-1]
            del path[-1]
    move_player(x, y)
    check()  # on check que le dernier mouvement n'est pas erroné.


def move_up():
    global y
    y -= 50
    path.append('u')

    if y < PCoords[1]:
        y = y + 50
        del path[-1]
    if len(path) > 1:
        if path[-2] == 'd':
            del path[-1]
            del path[-1]
    move_player(x, y)
    check()


def move_left():
    global x
    x -= 50
    path.append('l')

    if x < PCoords[0]:
        x += 50
        del path[-1]
    if len(path) > 1:
        if path[-2] == 'r':
            del path[-1]
            del path[-1]
    move_player(x, y)
    check()


def move_right():
    global x
    x += 50
    path.append('r')

    if x > PCoords[0] + 399:
        x -= 50
        del path[-1]
    if len(path) > 1:
        if path[-2] == 'l':
            del path[-1]
            del path[-1]
    move_player(x, y)
    check()


def button(msg, xx, yy, w, h, oncolor, offcolor, action=None, args=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(Display, white, (xx, yy, w, h))

    # Fonction qui fait un bouton au coordonnées xx et yy de width w et height h, de couleur offcolor sauf si la souris
    # est au dessus du bouton, alors la couleur est oncolor. Si l'utilisateur clique, on effectue la fonction action,
    # et on y associe l'argument args sauf si il n'y a pas d'arguments pour cette fonction.

    if (xx + w) > mouse[0] > xx and (yy + h) > mouse[1] > yy:
        pygame.draw.rect(Display, oncolor, (xx + 2, yy + 2, (w - 4), (h - 4)))
        if click[0] == 1 and action is not None:
            if args is None:
                action()
            else:
                action(args)
    else:
        pygame.draw.rect(Display, offcolor, (xx + 2, yy + 2, (w - 4), (h - 4)))

    disp_text((xx + w / 2), (yy + h / 2), msg, white, 15)  # on affiche ce texte centré dans le bouton.
    pygame.display.update()


def next_level(boule):  # on prend en argument une booléenne
    global current_lvl, wr_lvl, levelon
    if boule:  # si vrai, on passe au niveau suivant
        if levelon == 1:
            current_lvl = lvl2
            wr_lvl = wr_lvl2
            levelon = 2
        elif levelon == 2:
            current_lvl = lvl3
            wr_lvl = wr_lvl3
            levelon = 3
        elif levelon == 3:
            crash("FIN", "Vous avez fini le jeu!\n Merci d'avoir joué!", 10000)
            pygame.quit()
            quit()

    game_loop()


def won():  # Menu de fin de niveau. choix de recommencer ou continuer au niveau suivant.
    global win

    while True:

        win = not win
        reset()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_f:
            # win = not win

        largeText = pygame.font.Font('resources/fonts/impact.ttf', 90)
        TextSurf, TextRect = text_objects("Gagné!", largeText, white)
        TextRect.center = (400, 150)

        smoltext = pygame.font.Font('resources/fonts/segoeui.ttf', 18)
        subSurf, subRect = text_objects("Passer au niveau suivant ou recommencer?", smoltext, white)
        subRect.center = (400, 300)

        Display.fill(black)

        Display.blit(TextSurf, TextRect)
        Display.blit(subSurf, subRect)
        button("Continuer", 100, 425, 175, 100, grey, darkgrey, next_level, True)
        button("Recommencer", 500, 425, 175, 100, grey, darkgrey, next_level, False)
        pygame.display.update()


def game_intro():
    global current_lvl, wr_lvl
    intro = True
    current_lvl = lvl1
    wr_lvl = wr_lvl1

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    intro = not intro

        largeText = pygame.font.Font('resources/fonts/arcade.ttf', 90)
        TextSurf, TextRect = text_objects("THE MAZE", largeText, white)
        TextRect.center = (400, 150)

        smoltext = pygame.font.Font('resources/fonts/segoeui.ttf', 18)
        subSurf, subRect = text_objects("Projet d'ISN de Hélie Lévy, Keenan Jacq et Théo de Angelis", smoltext,
                                        white)
        subRect.center = (400, 300)

        Display.fill(darkgrey)
        Display.blit(TextSurf, TextRect)
        Display.blit(subSurf, subRect)
        disp_text(400, 350, 'Appuyez sur F pour continuer', white, 18)

        button("Normal", 100, 425, 175, 100, grey, darkgrey, game_loop)

        button("Arcade", 500, 425, 175, 100, grey, darkgrey, game_loop)


def game_loop():
    global crashed, start_time, x, y, now_time
    start_time = pygame.time.get_ticks()
    while not crashed:

        for event in pygame.event.get():  # On obtient les inputs du joueur
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left()
                elif event.key == pygame.K_RIGHT:
                    move_right()
                elif event.key == pygame.K_UP:
                    move_up()
                elif event.key == pygame.K_DOWN:
                    move_down()
                elif event.key == pygame.K_f:
                    test(25,25)

        if win:
            won()
            return [None]
        else:
            now_time = pygame.time.get_ticks()

        if len(path) == 0 or error:
            now_time, start_time = 0, 0
            disp_text(113, 558, process_time((now_time - start_time)), white, 30)
        else:
            disp_text(113, 558, process_time((now_time - start_time)), white, 30)

        Display.blit(bgImg, [0, 0])
        move_player(x, y)

        pygame.display.update()
        pygame.time.wait(1)
        clock.tick(180)


game_intro()
game_loop()
