import PySimpleGUI as sg
import socket
import os
from PySimpleGUI.PySimpleGUI import VerticalSeparator
import time
from datetime import datetime
from datetime import date

#Connection
HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
print('GUI_MODULE')
ADDR = (SERVER,PORT)

gui = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gui.connect(ADDR)

def process_customizer(processes):
    custom_processes = []
    for process in processes:
        s = "[{pid}] notepad.exe".format(pid = process)
        custom_processes.append(s)
    
    return custom_processes

def start():
    msg="Gui"
    gui.send(msg.encode(FORMAT))

    sg.theme('LightGrey6')

    files3 = [" "]
    processes = []
    
    sg.ChangeLookAndFeel('LightGreen')      # set the overall color scheme
    column1 = [ 
                [sg.Text('Orgullo OS lleva corriendo::', font='Any 12'),sg.Text('', size=(30,1), key='_DATE_')],
                [sg.Text('Gestionar módulo aplicaciones', size=(50,2), justification='center')],
                [   
                    sg.Button('Abrir', font=('Any 15'), button_color=('white','#3eb548')),
                    sg.Button('Cerrar', font=('Any 15'), button_color=('white', '#3f56d1')), 
                    sg.Button('Actualizar_proc', font=('Any 15'), button_color=('white', '#e04646'))
                ],
                [sg.Text('', size=(50,1), justification='center')],
                [sg.HorizontalSeparator(pad=None)],
                [sg.Text('Procesos', size=(50,1))],
                [sg.Listbox(values=(processes), size=(50,10), enable_events=True, key='-PROC-')],
                [sg.HorizontalSeparator(pad=None)],
                [sg.Text('Log de transacciones', size=(50,1))],
                [sg.Output(size=(50,10))],
                [sg.Text('', size=(50,1))],
                [sg.HorizontalSeparator(pad=None)],
                [sg.Button('Apagar sistema', button_color=('white', '#e04646'), key='Exit')]
            ]

    
    frame_layout = [
                    [sg.Listbox(values=(files3), size=(50,16), enable_events=True, key='-LIST-')]
                ]


    column2 = [
                [sg.Text('Gestionar módulo carpetas', size=(50,1), justification='center')],
                [sg.HorizontalSeparator(pad=None)],
                [sg.Frame('root', frame_layout, font='Any 12', title_color='blue')],
                [sg.Button('Eliminar', button_color=('white', '#e04646'), font=('Any 15')), sg.Button('Actualizar', button_color=('white', 'black'), font=('Any 15'))],
                [sg.Text('Crear directorio', size=(50,2), justification='center')],
                [sg.HorizontalSeparator(pad=None)],
                [sg.Text('Ingrese el nombre del directorio', size=(50,1))],
                [sg.Input(key='-DIRNAME-', size=(50,1), tooltip='Nombre del directiorio')],
                [sg.Button('Crear', font=('Any 15'), button_color=('white', '#3f56d1'))]
            ]


    # The GUI layout
    layout =  [
                    [sg.Column(column1, size=(500,700)), VerticalSeparator(pad=None), sg.Column(column2, size=(500,700))],

            ]

    # create the "Window"
    window = sg.Window('Orgullo OS', layout=layout, default_element_size=(12,1),font='Any 12')

    start_time = datetime.now()

    
    #  The "Event loop" where all events are read and processed (button clicks, etc)
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.today().strftime("%d/%m/%Y")

        event, values = window.Read(timeout=10)     # read with a timeout of 10 ms
        if event != sg.TIMEOUT_KEY:                 # if got a real event, print the info
            pass
        
        if event in (None, 'Exit'):
            break

        if event == 'Abrir':
            msg="cmd:send,src:Gui,dst:App,status:"+"none"+",msg:\"log: " + current_time + " "+ current_date + ",Open"
            print("[MESSAGE] - "+msg)
            gui.send(bytes(msg,FORMAT))
            p = gui.recv(HEADER).decode(FORMAT)
            pid = (p.split(',')[-1]).split()[-1]
            processes.append(pid)
            window.Element('-PROC-').update(values=(process_customizer(processes)))

        if event == 'Cerrar':
            processes_list = values['-PROC-']
            process = (processes_list[0].split(']')[0])[1:]

            if processes_list:
                msg="cmd:send,src:Gui,dst:Log,status:"+"processed"+",msg:\"log: " + current_time + " "+ current_date + ",Close " + process
                msgapp="cmd:send,src:Gui,dst:App,status:"+"processed"+",msg:\"log: " + current_time + " "+ current_date + ",Close " + process
                processes.remove(process)
                gui.send(msg.encode(FORMAT))
                gui.send(msgapp.encode(FORMAT))
                print("[MESSAGE] close process - "+msg)
                window.Element('-PROC-').update(values=(process_customizer(processes)))

        if event == 'Actualizar_proc':
            window.Element('-PROC-').update(values=(process_customizer(processes)))

        if event == 'Actualizar':
            msg="cmd:send,src:Gui,dst:Log,status:"+"none"+",msg:\"log: " + current_time + " "+ current_date + ",Info"
            gui.send(msg.encode(FORMAT))
            files = gui.recv(HEADER).decode(FORMAT)
            files2 = files.split(',')
            files3 = files2[-1].split()
            print("[MESSAGE] - "+msg)
            window.Element('-LIST-').update(values=(files3))

        if event == 'Crear':
            namedir = values['-DIRNAME-']
            msg="cmd:send,src:Gui,dst:Log,status:"+"processed"+",msg:\"log: " + current_time + " "+ current_date + ",Create "+namedir
            print("[MESSAGE] - "+msg)
            gui.send(bytes(msg,FORMAT))
            window.Element('-LIST-').update(values=(files3))

        if event == 'Eliminar':
            namedir = values['-LIST-']
            print(namedir)
            msg="cmd:send,src:Gui,dst:Log,status:"+"processed"+",msg:\"log: " + current_time + " "+ current_date + ",Delete "+namedir[0]
            gui.send(msg.encode(FORMAT))
            print("[MESSAGE] - "+msg)
            window.Element('-LIST-').update(values=(files3))

        
        # Output the "uptime" statistic to a text field in the window
        window.Element('_DATE_').Update(str(datetime.now()-start_time))


    # Exiting the program
    window.Close()    # be sure and close the window before trying to exit the program
    print('Completed shutdown')

start()