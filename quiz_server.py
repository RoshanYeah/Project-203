import socket
from threading import Thread

nicknames = []
list_of_clients = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = '127.0.0.1'
PORT = 8000

server_socket.bind((IP, PORT))
server_socket.listen()

print('Server has started...')

def clientthread(conn, nick):
    conn.send("Welcome to this quizroom!".encode('utf-8'))
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                print(message)
                broadcast(message,conn)
            else:
                remove(conn)
                removeNickname(nick)
        except:
            continue

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message.encode('utf-8'))
            except:
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def removeNickname(nick):
    if nick in nicknames:
        nicknames.remove(nick)

while True:
    conn, nick = server_socket.accept()
    client_thread = Thread(target=clientthread, args=(conn, nick))
    client_thread.start()
