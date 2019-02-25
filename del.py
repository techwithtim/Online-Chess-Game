import socket
from _thread import *
from board import Board
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "157.230.230.181"
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


def threaded_client(conn):
    global currentId, pos, bo

    variable = bo
    # Pickle the object and send it to the server
    data_string = pickle.dumps(variable)

    conn.send(data_string)
    currentId = "b"

    while True:
        try:
            d = conn.recv(8192 * 8)
            data = d.decode("utf-8")
            if not d:
                break
            else:

                if data.count("select") > 0:
                    all = data.split(" ")
                    col = all[0]
                    row = all[1]
                    color = all[2]

                if data == "update moves":
                    bo.update_moves()

                bo.select(col, row, color)
                print("Recieved ", data)

                sendData = pickle.dumps(bo)
                print("Sending ", sendData)

            conn.sendall(sendData)

        except Exception as e:
            print(e)
            break

    print("Connection Closed")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ")

    start_new_thread(threaded_client, (conn,))
