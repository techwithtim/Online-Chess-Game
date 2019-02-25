import pygame
import os
import time
from client import Network
import pickle
pygame.font.init()

board = pygame.transform.scale(pygame.image.load(os.path.join("img","board_alt.png")), (750, 750))
rect = (113,113,525,525)

turn = "w"


def menu_screen(win):
    global bo
    run = True

    while run:
        win.fill((128,128,128))
        font = pygame.font.SysFont("comicsans", 80)
        title = font.render("Online Chess!", 1, (0,200,0))
        join = font.render("Click To Join a Game!", 1, (0, 128, 0))
        win.blit(title, (width/2 - title.get_width()/2, 200))
        win.blit(join, (width / 2 - join.get_width() / 2, 400))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    while True:
        try:
            bo = connect()
            break
        except:
            print("Server Offline")

    main()


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
    txt = font.render("Player 2 Time: " + str(formatTime2), 1, (255, 255, 255))
    txt2 = font.render("Player 1 Time: " + str(formatTime1), 1, (255,255,255))
    win.blit(txt, (540,10))
    win.blit(txt2, (540, 700))

    txt = font.render("Press q to Quit", 1, (255, 255, 255))
    win.blit(txt, (10, 20))

    if color == "s":
        txt3 = font.render("SPECTATOR MODE", 1, (255, 0, 0))
        win.blit(txt3, (width/2-txt3.get_width()/2, 10))

    if not ready:
        font = pygame.font.SysFont("comicsans", 80)
        txt = font.render("Waiting for Player", 1, (255, 0, 0))
        win.blit(txt, (width/2 - txt.get_width()/2, 300))

    font = pygame.font.SysFont("comicsans", 30)
    if color == "w":
        txt3 = font.render("YOU ARE WHITE", 1, (255, 0, 0))
        win.blit(txt3, (width / 2 - txt3.get_width() / 2, 10))
    else:
        txt3 = font.render("YOU ARE BLACK", 1, (255, 0, 0))
        win.blit(txt3, (width / 2 - txt3.get_width() / 2, 10))

    if bo.turn == color:
        txt3 = font.render("YOUR TURN", 1, (255, 0, 0))
        win.blit(txt3, (width / 2 - txt3.get_width() / 2, 700))
    else:
        txt3 = font.render("THEIR TURN", 1, (255, 0, 0))
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
    global turn, bo

    color = bo.start_user
    count = 0

    bo = n.send("update_moves")
    clock = pygame.time.Clock()
    run = True

    while run:
        p1Time = bo.time1
        p2Time = bo.time2
        if count == 30:
            bo = n.send("get")
            count = 0
        else:
            count += 1
        clock.tick(30)

        redraw_gameWindow(win, bo, p1Time, p2Time, color, bo.ready)

        if p1Time <= 0:
            bo = n.send("winner b")
        elif p2Time <= 0:
            bo = n.send("winner w")

        if bo.check_mate("b"):
            bo = n.send("winner b")
        elif bo.check_mate("w"):
            bo = n.send("winner w")

        if bo.winner == "w":
            end_screen(win, "White is the Winner!")
            run = False
        elif bo.winner == "b":
            end_screen(win, "Black is the winner")
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

            if event.type == pygame.MOUSEBUTTONUP and color != "s":
                if color == bo.turn and bo.ready:
                    pos = pygame.mouse.get_pos()
                    bo = n.send("update moves")
                    i, j = click(pos)
                    bo = n.send("select " + str(i) + " " + str(j) + " " + color)
    print("failed")
    n.disconnect()
    bo = 0
    menu_screen(win)


width = 750
height = 750
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess Game")
menu_screen(win)