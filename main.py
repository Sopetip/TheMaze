# coding: utf-8
import pygame
import serial

arduino_on = False

try:  # on vérifie que l'arduino est branchée sur le port 7, todo: une ligne de code qui try tous les ports
    arduino_on = True
    ser1 = serial.Serial('COM7', 9600)
except serial.SerialException:
    arduino_on = False
pygame.init()  # on initialise le pygame

Display = pygame.display.set_mode((800, 700))  # taille de l'écran
pygame.display.set_caption('The Maze')  # caption du programme
clock = pygame.time.Clock()  # on init la clock
bgImg = pygame.image.load('resources/main/themaze.png')  # on load les images du jeu
player = pygame.image.load('resources/main/player.png')
level1_player = player
level2_player = pygame.image.load('resources/main/player2.png')
level3_player = pygame.image.load('resources/main/player3.png')
slamthetargets = pygame.mixer.music.load('resources/audio/SlamTheTargets.wav')
pygame.display.set_icon(player)
# pygame.mixer.music.play(-1)

# il faut définir les couleurs dont on aura besoin
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (75, 75, 75)
darkgrey = (25, 25, 25)
darkblue = (0, 0, 90)
darkgreen = (0, 90, 0)
darkred = (90, 0, 0)

level_on = 1  # on déclare les variables
arcade_on = False
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


def send_info(value=''):  # Envoyer les infos à l'arduino
    if len(current_lvl) != len(path):  # le début de ce code permet de déterminer quelle est la flèche à envoyer.
        val = current_lvl[len(path)]
    else:  # double fonction : permet aussi d'envoyer une valeur spécifique si besoin.
        return [None]
    if value == '':
        value = val
    else:
        pass
    ser1.write(value.encode())  # on write sur le sérial de l'arduino le message de 1 charactère.
    pygame.time.wait(1)  # on attends 1 pour pas lagger le jeu.


def test(dx, dy):  # todo le level qui scroll
    Display.scroll(dx, dy)  # ne marche pas du tout lol


def process_time(time):  # fonction qui prend la valeur du temps en ms et la rend en str de type m:s.ms
    global error, returned, ms
    ms = time
    if ms >= 119000:  # en fait si ms dépasse ce temps l'arrondissement des valeurs bugge donc c'est la limite
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


def text_objects(text, font, color):  # affiche un message et rend la valeur du message et le rectangle invisible.
    text_surface = font.render(text, False, color)
    return text_surface, text_surface.get_rect()


def disp_text(xpos, ypos, text, color=white, fontsize=18,
              font_family='resources/fonts/segoeui.ttf'):  # fonction pour afficher un texte à l'écran
    font1 = pygame.font.Font(font_family, fontsize)  # init la police
    show = font1.render(text, True, color)  # on affiche le texte
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


def reset():  # on reset la taille du path et on reset les valeurs.
    global error, win
    path[:] = []  # selectionner tous les objets de la liste et les remplacer par la liste suivante: rien
    error, win = False, False


def check():  # on check si le dernier move du joueur correspond au move demandé par le niveau
    global error, win, start_time, x, y, PCoords, returned

    send_info() if arduino_on else truncate(200)  # cette ligne permet juste de racourcir le code, truncate ne fait rien

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
        crash("BOOM", ' ', 250)  # on crashe "boom", vous avez perdu.
        reset()
        if arduino_on:
            send_info('o')
        return [None]

    if win:
        if ms <= wr_lvl2:
            crash("NOUVEAU RECORD", returned, 4000)
        else:
            crash("Gagné!", returned, 1000)
        reset()
        arcade() if arcade_on else won()

    # print(path)


def move_player(xpos, ypos):
    Display.blit(player, (xpos, ypos))  # on blit le joueur à x et y


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


def button(msg, xx, yy, w, h, oncolor, offcolor, action=None, args=None, border_color=white):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(Display, border_color, (xx, yy, w, h))

    # Fonction qui fait un bouton au coordonnées xx et yy de width w et height h, de couleur offcolor sauf si la souris
    # est au dessus du bouton, alors la couleur est oncolor. Si l'utilisateur clique, on effectue la fonction action,
    # et on y associe l'argument args sauf si il n'y a pas d'arguments pour cette fonction.
    # on dessine aussi des carrés autour du bouton, avec des couleurs spécifiques.

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
    global current_lvl, wr_lvl, level_on, player
    # cette fonction sert à determiner que faire à la fin d'un niveau.

    if boule:  # si vrai, on passe au niveau suivant

        if level_on == 1:
            current_lvl = lvl2
            wr_lvl = wr_lvl2
            level_on = 2
            player = level2_player
        # on définit alors pour le niveau qui vient, quel est le chemin à suivre, quel est le record de temps, et quelle
        # icône de joueur on veut.

        elif level_on == 2:
            current_lvl = lvl3
            wr_lvl = wr_lvl3
            level_on = 3
            player = level3_player


        elif level_on == 3:
            crash("FIN", "Vous avez fini le jeu!"
                         " Merci d'avoir joué!", 10000)
            pygame.quit()
            quit()

    game_loop()


def arcade_level(lvl):  # presque pareil mais pour l'arcade (le choix des niveaux)
    global current_lvl, wr_lvl, player

    if lvl == 1:
        current_lvl = lvl1
        wr_lvl = wr_lvl1
        player = level1_player

    elif lvl == 2:
        current_lvl = lvl2
        wr_lvl = wr_lvl2
        player = level2_player

    elif lvl == 3:
        current_lvl = lvl3
        wr_lvl = wr_lvl3
        player = level3_player

    game_loop()


def won():  # Menu de fin de niveau. choix de recommencer ou continuer au niveau suivant.
    global win
    send_info('m') if arduino_on else truncate(200)
    while True:
        if arduino_on:
            send_info('g')
            send_info('0')
        win = not win
        reset()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_f:

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


def arcade():
    global current_lvl, wr_lvl, arcade_on
    menu = True
    arcade_on = True
    current_lvl = lvl1
    wr_lvl = wr_lvl1
    send_info('m') if arduino_on else truncate(200)

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        largeText = pygame.font.Font('resources/fonts/arcade.ttf', 90)
        TextSurf, TextRect = text_objects("ARCADE", largeText, white)
        TextRect.center = (400, 150)

        Display.fill(darkgrey)
        Display.blit(TextSurf, TextRect)

        button("Niveau 1", 350, 300, 100, 40, blue, darkblue, arcade_level, 1)
        button("Niveau 2", 350, 350, 100, 40, red, darkred, arcade_level, 2)
        button("Niveau 3", 350, 400, 100, 40, green, darkgreen, arcade_level, 3)
        button("Retour", 600, 600, 100, 60, grey, darkgrey, game_intro)


def game_intro():
    global current_lvl, wr_lvl, arcade_on
    intro = True  # on reset toutes les valeurs qui aurait pû être modifiées (si il rentre dans le menu arcade puis sort)
    arcade_on = False
    current_lvl = lvl1
    wr_lvl = wr_lvl1

    while intro:
        send_info('m') if arduino_on else truncate(200)  # si on est dans le menu, l'arduino affiche "go!"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

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

        # Ces 15 lignes au dessus servent à afficher les messages écrit sur le menu principal.

        button("Normal", 100, 425, 175, 100, grey, darkgrey, game_loop)

        button("Arcade", 500, 425, 175, 100, grey, darkgrey, arcade)
        # on donne au joueur le choix: soit un mode avec tous les niveaux d'affilée, ou un mode où il peut choisir son
        # propre niveau.


def game_loop():
    global crashed, start_time, x, y, now_time
    start_time = pygame.time.get_ticks()  # on lance le timer
    check()
    while not crashed:
        for event in pygame.event.get():  # On obtient les inputs du joueur
            if event.type == pygame.QUIT:
                pygame.quit()  # si il appuie sur la croix, le jeu se ferme.

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
                    test(25, 25)

        now_time = pygame.time.get_ticks()  # on arrête le timer.

        if len(path) == 0 or error:  # on relance à 0 si le joueur se trompe ou décide de faire machine arrière.
            now_time, start_time = 0, 0
            disp_text(113, 558, process_time((now_time - start_time)), white, 30)
        else:
            disp_text(113, 558, process_time((now_time - start_time)), white, 30)

        Display.blit(bgImg, [0, 0])  # on blit le background.
        move_player(x, y)  # on bouge le joueur à ses coordonnées.

        pygame.display.update()
        pygame.time.wait(1)
        clock.tick(180)


game_intro()  # on lance le jeu.
