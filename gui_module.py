# https://realpython.com/pysimplegui-python/#getting-started-with-pysimplegui
import PySimpleGUI as sg
import socket
import datetime
import os
from PySimpleGUI.PySimpleGUI import VerticalSeparator

#Connection
HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)

gui = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gui.connect(ADDR)


def start():
    msg="Gui"
    gui.send(msg.encode(FORMAT))
    sg.theme('LightGrey6')
    print('Starting up...')


    sg.ChangeLookAndFeel('LightGreen')      # set the overall color scheme
    column1=[   [sg.Text('Orgullo OS lleva corriendo::', font='Any 12'),sg.Text('', size=(30,1), key='_DATE_')],
                [sg.Text('Gestionar módulo aplicaciones', size=(50,2), justification='center')],
                [sg.Button('Calc', font=('Any 15'), button_color=('white','#3eb548')), sg.Button('Close all', font=('Any 15'), button_color=('white', '#3f56d1')) ],
                [sg.Text('', size=(50,1), justification='center')],
                [sg.HorizontalSeparator(pad=None)],
                [sg.Text('Log de transacciones', size=(50,2))],
                [sg.Output(size=(50,16))],
                [sg.Button('Apagar sistema', button_color=('white', '#e04646'), key='Exit')],
            ]

    frame_layout = [
                    
                    [sg.Listbox(values=('Listbox 1', 'Listbox 2', 'Listbox 3','Listbox 4','Listbox 5'), size=(50,16), enable_events=True, key='_LIST_')]
                ]


    column2=[
                [sg.Text('Gestionar módulo carpetas', size=(50,1), justification='center')],
                [sg.HorizontalSeparator(pad=None)],
                [sg.Frame('root', frame_layout, font='Any 12', title_color='blue')],
                [sg.Submit(), sg.Cancel()]
            ]


    # The GUI layout
    layout =  [ 
                    [sg.Column(column1, size=(500,700)), VerticalSeparator(pad=None), sg.Column(column2, size=(500,700))],

            ]

    # create the "Window"
    window = sg.Window('Orgullo OS', layout=layout, default_element_size=(12,1),font='Any 12')

    start_time = datetime.datetime.now()
    #  The "Event loop" where all events are read and processed (button clicks, etc)
    while True:
        event, values = window.Read(timeout=10)     # read with a timeout of 10 ms
        if event != sg.TIMEOUT_KEY:                 # if got a real event, print the info
            pass
        if event in (None, 'Exit'):
            break
        if event == 'Calc':
            
            msg="cmd:send,src:Gui,dst:App,status:"+"none"+",msg:\"log: " + "124312" + " "+ "030421"+ ",Open"
            print("[MESSAGE] - "+msg)
            gui.send(bytes(msg,FORMAT))

        if event == 'Close all':
            msg="cmd:send,src:Gui,dst:App,status:"+"none"+",msg:\"log: " + "124312" + " "+ "030421"+ ",Close"
            print("[MESSAGE] - "+msg)
            gui.send(bytes(msg,FORMAT))


        # Output the "uptime" statistic to a text field in the window
        window.Element('_DATE_').Update(str(datetime.datetime.now()-start_time))

    # Exiting the program
    window.Close()    # be sure and close the window before trying to exit the program
    print('Completed shutdown')

start()