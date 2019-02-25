import socket
from _thread import *
from board import Board
import pickle
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = ""
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

bo = Board(8, 8)

currentId = "w"
connections = 0


def threaded_client(conn):
    global currentId, pos, bo, currentId, connections

    variable = bo
    bo.start_user = currentId

    if connections > 2:
        bo.start_user = "s"
    # Pickle the object and send it to the server
    data_string = pickle.dumps(variable)

    if currentId == "b":
        bo.ready = True
        bo.startTime = time.time()
    conn.send(data_string)
    currentId = "b"
    connections += 1

    while True:
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
                if data == "winner w":
                    bo.winner = "w"

                if data == "update moves":
                    bo.update_moves()

                print("Recieved ", data)

                if bo.ready:
                    if bo.turn == "w":
                        bo.time1 = 900 - (time.time() - bo.startTime) - bo.storedTime1
                    else:
                        bo.time2 = 900 - (time.time() - bo.startTime) - bo.storedTime2

                sendData = pickle.dumps(bo)
                print("Sending ", bo)

            conn.sendall(sendData)

        except Exception as e:
            print(e)
            break
    connections -= 1
    if connections < 2:
        bo = Board(8, 8)
        currentId = "w"
    print("Connection Closed")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ")

    start_new_thread(threaded_client, (conn,))
