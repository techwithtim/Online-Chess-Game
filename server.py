import socket
from _thread import *
from board import Board
import pickle
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "93.115.27.58"
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen()
print("Waiting for a connection")

connections = 0

games = {0:Board(8, 8)}


def threaded_client(conn, game):
    global pos, games, currentId, connections

    bo = games[game]

    if connections % 2 == 0:
        currentId = "w"
    else:
        currentId = "b"

    bo.start_user = currentId

    # Pickle the object and send it to the server
    data_string = pickle.dumps(bo)

    if currentId == "b":
        bo.ready = True
        bo.startTime = time.time()

    conn.send(data_string)
    connections += 1

    while True:
        if game not in games:
            break

        try:
            d = conn.recv(8192 * 2)
            data = d.decode("utf-8")
            if not d:
                break
            else:

                if data.count("select") > 0:
                    all = data.split(" ")
                    col = int(all[1])
                    row = int(all[2])
                    color = all[3]
                    bo.select(col, row, color)

                if data == "winner b":
                    bo.winner = "b"
                    print("[GAME] Player b won in game", game)
                if data == "winner w":
                    bo.winner = "w"
                    print("[GAME] Player w won in game", game)

                if data == "update moves":
                    bo.update_moves()

                #print("Recieved board from", currentId, "in game", game)

                if bo.ready:
                    if bo.turn == "w":
                        bo.time1 = 900 - (time.time() - bo.startTime) - bo.storedTime1
                    else:
                        bo.time2 = 900 - (time.time() - bo.startTime) - bo.storedTime2

                sendData = pickle.dumps(bo)
                #print("Sending board to player", currentId, "in game", game)

            conn.sendall(sendData)

        except Exception as e:
            print(e)
            break
    
    connections -= 1
    try:
        del games[game]
        print("[GAME] Game", game, "ended")
    except:
        pass
    print("[DISCONNECT] Player left game", game)
    conn.close()


while True:
    conn, addr = s.accept()

    if connections %2 ==0:
        games[connections//2] = Board(8,8)

    print("[CONNECT] Connected to: ", addr)
    print("[DATA] Number of Connections:", connections+1)
    print("[DATA] Number of Games:", len(games))

    start_new_thread(threaded_client, (conn,len(games)-1))
