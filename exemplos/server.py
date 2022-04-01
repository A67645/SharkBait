import socket
import pickle
from _thread import *
import sys

server = "192.168.1.79"
port = 5555

window_width=1009 #612
window_height=720 #437
shark_x = window_width//2
shark_y = window_height//2

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()        
print("Esperando por jogadores...")

#posiçoes dos jogadores
pos = [(0,0), (100,100)]



def client_thread(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data
            if not data:
                print("Desconectado")
                break
            else:
                #nao esquecer de no outro lado fazer split disto como lista de listas
                reply = pos.pop(player)
                print("Recebido: ", reply)
                print("Enviando: ", reply)
            conn.sendall(str.encode(make_pos(reply)))
        except:
            break        

#num de jogador
currentPlayer = 0         
while True:
    conn, addr = s.accept()
    print("Ligado a: ", addr)
    start_new_thread(client_thread, (conn, currentPlayer))
    currentPlayer += 1 