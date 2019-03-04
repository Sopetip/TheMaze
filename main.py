# coding: utf-8
import pygame

pygame.init()  # on initialise le pygame

Display = pygame.display.set_mode((800, 700))  # taille de l'écran
pygame.display.set_caption('The Maze')  # caption du programme
clock = pygame.time.Clock()  # on init la clock
bgImg = pygame.image.load('resources/main/themaze.png')  # on load les images du jeu
player = pygame.image.load('resources/main/player.png')

# il faut définir les couleurs dont on aura besoin
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

baseCoords = (213, 228)  # C'est un tuple, genre de liste invariable contrairement à PCoords en dessous.
PCoords = [213, 228]  # on définit les coordonnées de base et du player pour plus tard

lvl1 = ['d', 'd', 'r', 'u', 'u', 'r', 'r', 'r', 'r', 'r', 'd', 'l', 'd', 'l', 'u', 'l', 'd', 'd', 'd', 'd', 'l', 'l',
        'l', 'd', 'd', 'r', 'u', 'r', 'd', 'r', 'u', 'r', 'u', 'r', 'd', 'd', 'l']
wrlvl1 = [0, 4, 72]

currentlvl = lvl1
x = PCoords[0]
y = PCoords[1]  # on déclare les variables
path = []

crashed = False
error = False
win = False

start_time = 0


def truncate(n):
    return int(n * 1000) / 1000  # fonction qui fait la troncature


def process_time(time):  # fonction qui prend la valeur du temps en ms et la rend en str de type m:s.ms
    global error
    ms = time
    if ms >= 119000:
        error = True
        return 'Error'
    sec = ms / 1000
    minut = 0
    while sec / 60 > 1:
        minut += 1
        sec = truncate(sec - (minut * 60))
    returned = str(minut) + ':' + str(sec)
    return returned


def reset():  # on reset la taille du path, on relance le timer et on remet le personnage de façon normale
    global error
    path[:] = []  # selectionner tous les objets de la liste et les remplacer par la liste suivante: rien
    error = False


def text_objects(text, font, color):
    text_surface = font.render(text, False, color)
    return text_surface, text_surface.get_rect()


def disp_text_box(x, y, text, color):
    thefont = pygame.font.Font('resources/main/segoeui.ttf', 30)
    text_surf, text_rect = text_objects(text, thefont, color)
    text_rect.center = (x, y)
    Display.blit(text_surf, text_rect)
    pygame.display.update()


def crash(text):
    global x,y,PCoords
    thefont = pygame.font.Font('resources/main/impact.ttf', 65)

    x = PCoords[0]
    y = PCoords[1]
    pygame.time.wait(1)
    move_player(x,y)

    text_surf, text_rect = text_objects(text, thefont, white)
    text_rect.center = (400, 350)

    Display.fill(black)
    Display.blit(text_surf, text_rect)

    pygame.display.update()
    pygame.time.wait(1500)


def check():  # on check si le dernier move du joueur correspond au move demandé par le niveau
    global error, win, start_time, x, y, PCoords
    if len(path) == 0:

        return [None]

    elif len(path) == 1:
        start_time = pygame.time.get_ticks()  # on lance la clock au moment du premier move

    if error:  # on renvoie le player au premier
        crash("BOOM")
        reset()
        return [None]

    i = len(path) - 1

    if path[i] != currentlvl[i]:
        error = True
    if len(path) == len(currentlvl) and not error:
        win = True

    if win:
        crash("YOU WIN")
        reset()
    print(path)


def move_player(x, y):
    Display.blit(player, (x, y))
    # pygame.draw.rect(Display,blue,(x,y,x+25,y+25))


def movedown():  # les 4 fonctions de mouvements qui sont quasiment les mêmes.
    global y  # juste on bouge les coordonnées du player de 50 sur X ou Y
    y += 50
    path.append('d')  # ensuite on append à la fin de la liste 'path' le dernier mouvement exécuté.

    if y > baseCoords[1] + 399:  # on vérifie que le joueur n'a pas atteint les limites
        y = y - 50
        del path[-1]
    if len(path) > 1:
        if path[-2] == 'u':
            del path[-1]
            del path[-1]
    move_player(x, y)
    check()  # on check que le dernier mouvement n'est pas erroné.


def moveup():
    global y
    y -= 50
    path.append('u')

    if y < baseCoords[1]:
        y = y + 50
        del path[-1]
    if len(path) > 1:
        if path[-2] == 'd':
            del path[-1]
            del path[-1]
    move_player(x, y)
    check()


def moveleft():
    global x
    x -= 50
    path.append('l')

    if x < baseCoords[0]:
        x += 50
        del path[-1]
    if len(path) > 1:
        if path[-2] == 'r':
            del path[-1]
            del path[-1]
    move_player(x, y)
    check()


def moveright():
    global x
    x += 50
    path.append('r')

    if x > baseCoords[0] + 399:
        x -= 50
        del path[-1]
    if len(path) > 1:
        if path[-2] == 'l':
            del path[-1]
            del path[-1]
    move_player(x, y)
    check()

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    intro = not intro
        Display.fill(black)
        largeText = pygame.font.Font('resources/main/segoeui.ttf',90)
        TextSurf, TextRect = text_objects("THE MAZE", largeText, white)
        TextRect.center = (400,350)
        Display.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(15)

def game_loop():
    global crashed, start_time, x, y
    start_time = pygame.time.get_ticks()
    while not crashed:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moveleft()
                elif event.key == pygame.K_RIGHT:
                    moveright()
                elif event.key == pygame.K_UP:
                    moveup()
                elif event.key == pygame.K_DOWN:
                    movedown()
                elif event.key == pygame.K_r:
                    crash('BOOM')

        if win:
            pass
        else:
            now_time = pygame.time.get_ticks()
        if len(path) == 0 or error:
            now_time, start_time = 0, 0
            disp_text_box(113, 558, process_time((now_time - start_time)), white)
        else:
            disp_text_box(113, 558, process_time((now_time - start_time)), white)

        Display.blit(bgImg, [0, 0])
        move_player(x, y)

        pygame.display.update()
        pygame.time.wait(1)
        clock.tick(120)

game_intro()
game_loop()
