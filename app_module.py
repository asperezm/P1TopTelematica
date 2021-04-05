import socket
import os, signal
import subprocess
import random
import time
from datetime import datetime
from datetime import date

HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
print('APP_MODULE')
ADDR = (SERVER,PORT)

app = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
app.connect(ADDR)

def start():
    msg="App"
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.today().strftime("%d/%m/%Y")
    app.send(bytes(msg,FORMAT))
    connection = True

    while connection:
        msg = app.recv(HEADER).decode(FORMAT)
        
        command = msg.split(',')
        
        if(command[3]!="status:Error"):
            if(command[-1]=="Open"):
                num = random.randrange(1,4)
                if(num==1 or num==2):
                    status="processed"
                elif(num == 3):
                    status="busy"

                try:
                    process = subprocess.Popen('notepad.exe')
                    pid = str(process.pid)
                    msg_log="cmd:send,src:App,dst:Log,status:"+status+",msg:\"log: " + current_time + " "+ current_date+ ",Opened " + pid
                    msg_gui="cmd:send,src:App,dst:Gui,status:"+status+",msg:\"log: " + current_time + " "+ current_date+ ",Opened " + pid
                    app.send(bytes(msg_log,FORMAT))
                    app.send(bytes(msg_gui,FORMAT))
                except Exception as e:
                    msg_log="cmd:send,src:App,dst:Log,status:Error->" + str(e) + ",msg:\"log: " + current_time + " "+ current_date
                    app.send(bytes(msg_log,FORMAT))
            
            elif((command[-1]).split()[0]=="Close"):
                num = random.randrange(1,4)
                if(num==1 or num==2):
                    status="processed"
                elif(num == 3):
                    status="busy"

                try:
                    pid = int((command[-1]).split()[-1])
                    os.kill(pid, signal.SIGTERM)
                    msg_log="cmd:send,src:App,dst:Log,status:"+status+",msg:\"log: " + current_time + " "+ current_date+ ",Closed " + str(pid)
                    app.send(bytes(msg,FORMAT))
                except Exception as e:
                    msg_log="cmd:send,src:App,dst:Log,status:Error->" + str(e) + ",msg:\"log: " + current_time + " "+ current_date
                    app.send(bytes(msg,FORMAT))

        else:
            msg="cmd:send,src:App,dst:Log,status:Error,msg:\"log: " + current_time + " "+ current_date
            app.send(bytes(msg,FORMAT))

start()

