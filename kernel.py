#Revisar __init__ para crear instancias de los módulos
import gui as sg
import socket
import threading
import subprocess
import random
import time

HEADER = 1024
PORT = 5050
FORMAT = "utf-8"
HOST = socket.gethostbyname(socket.gethostname())
ADDR = (HOST, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

App = False
GUI = False
Log = False
connection = {}

def handle_client(conn, addr):
    global App, GUI, Log
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            msg = conn.recv(HEADER).decode(FORMAT)
        except:
            print("ERROR NO MESAGGE")

        if App == False or GUI == False or Log== False:
            if msg.startswith("App") and App == False:
                App=True
                print("APP CONNECTED")
                connection["App"]= conn
            elif msg.startswith("Gui") and GUI== False:
                GUI=True
                print("GUI CONNECTED")
                connection["Gui"]= conn
            elif msg.startswith("Log") and Log==False:
                Log=True
                print("LOGS CONNECTED")
                connection["Log"]= conn
        
        else:
            command = msg.split(',')
            if(command[3]=="status:processed"):
                if(command[2]=="dst:App"):
                    dest = connection["App"]
                    msg_send = msg.encode(FORMAT)
                    dest.send(msg_send)
                else:
                    dest = connection["Log"]
                    msg_send = msg.encode(FORMAT)
                    dest.send(msg_send)
            elif(command[3]=="status:busy"):
                busy = random.randrange(1,3)
                time.sleep(busy)
                if(command[2]=="dst:App"):
                    dest = connection["App"]
                    msg_send = msg.encode(FORMAT)
                    dest.send(msg_send)
                else:
                    dest = connection["Log"]
                    msg_send = msg.encode(FORMAT)
                    dest.send(msg_send)
            else:
                if(command[2]=="dst:App"):
                    dest = connection["App"]
                    msg_send = msg.encode(FORMAT)
                    dest.send(msg_send)
                else:
                    dest = connection["Log"]
                    msg_send = msg.encode(FORMAT)
                    dest.send(msg_send)

def start():
    server.listen()
    subprocess.call("start.bat")
    print(f"server is listenning on {HOST}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

    
print("Server is starting")
start()


#w = sg()