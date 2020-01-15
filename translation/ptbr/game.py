'''
the main game
author:@techwithtim
requirements:see requirements.txt
'''

import subprocess
import sys
import get_pip

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

try:
    print("[GAME] Tentando importar o pygame")
    import pygame
except:
    print("[EXCEPTION] Pygame não foi instalado")

    try:
        print("[GAME] Tentando instalar o pygame via pip")
        import pip
        install("pygame")
        print("[GAME] Pygame foi instalado com sucesso")
    except:
        print("[EXCEPTION] Pip não está instalado no sistema")
        print("[GAME] Tentando instalar o pip")
        get_pip.main()
        print("[GAME] Pip foi instalado com sucesso")
        try:
            print("[GAME] Tentando instalar o pugame ")
            import pip
            install("pygame")
            print("[GAME] Pygame foi instalado com sucesso")
        except:
            print("[ERROR 1] Não foi possível instalar o pygame")


import pygame
import os
import time
from client import Network
import pickle
pygame.font.init()

icon = pygame.image.load(os.path.join("img", "chessicon.png"))
board = pygame.transform.scale(pygame.image.load(os.path.join("img","board_alt.png")), (750, 750))
chessbg = pygame.image.load(os.path.join("img", "chessbg.png"))
rect = (113,113,525,525)

turn = "w"


def menu_screen(win, name):
    global bo, chessbg
    run = True
    offline = False

    while run:
        win.blit(chessbg, (0,0))
        small_font = pygame.font.SysFont("comicsans", 50)
        
        if offline:
            off = small_font.render("Servidor offline, tente mais tarde...", 1, (255, 0, 0))
            win.blit(off, (width / 2 - off.get_width() / 2, 500))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                offline = False
                try:
                    bo = connect()
                    run = False
                    main()
                    break
                except:
                    print("Servidor offline")
                    offline = True


    
def redraw_gameWindow(win, bo, p1, p2, color, ready):
    win.blit(board, (0, 0))
    bo.draw(win, color)

    formatTime1 = str(int(p1//60)) + ":" + str(int(p1%60))
    formatTime2 = str(int(p2 // 60)) + ":" + str(int(p2 % 60))
    if int(p1%60) < 10:
        formatTime1 = formatTime1[:-1] + "0" + formatTime1[-1]
    if int(p2%60) < 10:
        formatTime2 = formatTime2[:-1] + "0" + formatTime2[-1]

    font = pygame.font.SysFont("comicsans", 30)
    try:
        txt = font.render("Tempo de " + bo.p1Name + ": " + str(formatTime2), 1, (255, 255, 255))
        txt2 = font.render("Tempo de " + bo.p2Name + ": " + str(formatTime1), 1, (255,255,255))
    except Exception as e:
        print(e)
    win.blit(txt, (490,10))
    win.blit(txt2, (490, 700))

    txt = font.render("Aperte Q para sair", 1, (255, 255, 255))
    win.blit(txt, (10, 20))

    if color == "s":
        txt3 = font.render("MODO ESPECTADOR", 1, (255, 0, 0))
        win.blit(txt3, (width/2-txt3.get_width()/2, 10))

    if not ready:
        show = "Esperando por Jogador"
        if color == "s":
            show = "Esperando por Jogadores"
        font = pygame.font.SysFont("comicsans", 80)
        txt = font.render(show, 1, (255, 0, 0))
        win.blit(txt, (width/2 - txt.get_width()/2, 300))

    if not color == "s":
        font = pygame.font.SysFont("comicsans", 30)
        if color == "w":
            txt3 = font.render("VOCÊ É O BRANCO", 1, (255, 0, 0))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 10))
        else:
            txt3 = font.render("VOCÊ É O PRETO", 1, (255, 0, 0))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 10))

        if bo.turn == color:
            txt3 = font.render("SEU TURNO", 1, (255, 0, 0))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 700))
        else:
            txt3 = font.render("TURNO DELE", 1, (255, 0, 0))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 700))

    pygame.display.update()


def end_screen(win, text):
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 80)
    txt = font.render(text,1, (255,0,0))
    win.blit(txt, (width / 2 - txt.get_width() / 2, 300))
    pygame.display.update()

    pygame.time.set_timer(pygame.USEREVENT+1, 3000)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                run = False
            elif event.type == pygame.USEREVENT+1:
                run = False


def click(pos):
    """
    :return: pos (x, y) in range 0-7 0-7
    """
    x = pos[0]
    y = pos[1]
    if rect[0] < x < rect[0] + rect[2]:
        if rect[1] < y < rect[1] + rect[3]:
            divX = x - rect[0]
            divY = y - rect[1]
            i = int(divX / (rect[2]/8))
            j = int(divY / (rect[3]/8))
            return i, j

    return -1, -1


def connect():
    global n
    n = Network()
    return n.board


def main():
    global turn, bo, name

    color = bo.start_user
    count = 0

    bo = n.send("update_moves")
    bo = n.send("name " + name)
    clock = pygame.time.Clock()
    run = True

    while run:
        if not color == "s":
            p1Time = bo.time1
            p2Time = bo.time2
            if count == 60:
                bo = n.send("get")
                count = 0
            else:
                count += 1
            clock.tick(30)

        try:
            redraw_gameWindow(win, bo, p1Time, p2Time, color, bo.ready)
        except Exception as e:
            print(e)
            end_screen(win, "O outro jogador saiu")
            run = False
            break

        if not color == "s":
            if p1Time <= 0:
                bo = n.send("winner b")
            elif p2Time <= 0:
                bo = n.send("winner w")

            if bo.check_mate("b"):
                bo = n.send("winner b")
            elif bo.check_mate("w"):
                bo = n.send("winner w")

        if bo.winner == "w":
            end_screen(win, "O branco é o vencedor!")
            run = False
        elif bo.winner == "b":
            end_screen(win, "O preto é o vencedor")
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and color != "s":
                    # quit game
                    if color == "w":
                        bo = n.send("winner b")
                    else:
                        bo = n.send("winner w")

                if event.key == pygame.K_RIGHT:
                    bo = n.send("forward")

                if event.key == pygame.K_LEFT:
                    bo = n.send("back")


            if event.type == pygame.MOUSEBUTTONUP and color != "s":
                if color == bo.turn and bo.ready:
                    pos = pygame.mouse.get_pos()
                    bo = n.send("update moves")
                    i, j = click(pos)
                    bo = n.send("select " + str(i) + " " + str(j) + " " + color)
    
    n.disconnect()
    bo = 0
    menu_screen(win)


name = input("Por favor, digite seu nome: ")
width = 750
height = 750
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jogo de Xadrez")
pygame.display.set_icon(icon)
menu_screen(win, name)
