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
                process = subprocess.Popen('notepad.exe')
                pid = str(process.pid)

                status="processed"

                msg="cmd:send,src:App,dst:Log,status:"+status+",msg:\"log: " + current_time + " "+ current_date+ ",Open"
                msggui="cmd:send,src:App,dst:Gui,status:"+status+",msg:\"log: " + current_time + " "+ current_date+ ",Open " + pid
                app.send(bytes(msg,FORMAT))
                app.send(bytes(msggui,FORMAT))
            
            elif((command[-1]).split()[0]=="Close"):
                os.kill(int((command[-1]).split()[-1]), signal.SIGTERM)

                num = random.randrange(1,4)
                if(num==1 or num==2):
                    status="processed"
                elif(num == 3):
                    status="busy"
                else:
                    status="Error"

                msg="cmd:send,src:App,dst:Log,status:"+status+",msg:\"log: " + current_time + " "+ current_date+ ",Close"
                app.send(bytes(msg,FORMAT))

            elif(command[-1]=="Info"):
                num = random.randrange(1,4)
                if(num==1 or num==2):
                    status="processed"
                elif(num == 3):
                    status="busy"
                else:
                    status="Error"

                msg="cmd:send,src:App,dst:Log,status:"+status+",msg:\"log: " + current_time + " "+ current_date+ ",Close"
                app.send(bytes(msg,FORMAT))

        else:
            subprocess.call("close.bat")
            msg="cmd:send,src:App,dst:Log,status:Error,msg:\"log: " + current_time + " "+ current_date+ ",Error"
            app.send(bytes(msg,FORMAT))

start()

