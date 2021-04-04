import socket
import os
from datetime import datetime
from datetime import date

HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER,PORT)

file = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
file.connect(ADDR)

def write_log(msg):
    text = open("log_text.txt","a")
    text.write(msg +"\n")
    text.close()

def start():
    msg="Log"
    file.send(bytes(msg,FORMAT))
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.today().strftime("%d/%m/%Y")
    connection = True
    while connection:
        msg = file.recv(HEADER).decode(FORMAT)
        write_log(msg)
        command = msg.split(',')
        command2 = command[-1].split()
        if(command2[0] == "Create"):
            new_bucket = os.getcwd() + f'/{command2[-1] }'
            try:
                os.mkdir(new_bucket)
            except OSError:
                print("Error create folder")
        elif(command2[0] == "Delete"):
            bucket = os.getcwd() + f'/{command2[-1] }'
            try:
                os.rmdir(bucket)
            except OSError:
                print("Delete file")
        elif(command[-1]=="Info"):
            bucket1 = os.listdir(os.getcwd())
            bucketname = ""
            for buck in bucket1:
                if os.path.isdir(os.path.join(buck)):
                    bucketname += buck+" "
            msg_files = "cmd:send,src:Log,dst:Gui,status:processed,msg:\"log: " + current_time + " "+ current_date+ ","+ bucketname[:-1]
            write_log(msg_files)
            file.send(msg_files.encode(FORMAT))
            
        
start()

    
