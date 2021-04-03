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
msg="GUI"
gui.send(msg.encode(FORMAT))


sg.theme('LightGrey6')
print('Starting up...')


sg.ChangeLookAndFeel('LightGreen')      # set the overall color scheme
column1=[   [sg.Text('Orgullo OS has been running for:', font='Helvetica 11'),sg.Text('', size=(30,1), key='_DATE_')],
            [sg.Button('Comunication')],
            [sg.Text('', size=(30,1), key='_TEXT_')],
            [sg.Input('Single Line Input', do_not_clear=True, enable_events=True, size=(30,1))],
            [sg.Multiline('Multiline Input', do_not_clear=True, size=(40,4), enable_events=True)],
            # [sg.MultilineOutput('Multiline Output', size=(40,8),  key='_MULTIOUT_', font='Courier 12')],
            [sg.Output(font='Calibri 11', size=(60,8))],
            [sg.Checkbox('Checkbox 1', enable_events=True, key='_CB1_'), sg.Checkbox('Checkbox 2', default=True, enable_events=True, key='_CB2_')],
            [sg.Combo(values=['Combo 1', 'Combo 2', 'Combo 3'], default_value='Combo 2', key='_COMBO_',enable_events=True, readonly=False, tooltip='Combo box', disabled=False, size=(12,1))],
            [sg.Listbox(values=('Listbox 1', 'Listbox 2', 'Listbox 3','Listbox 4','Listbox 5'), size=(10,3), enable_events=True, key='_LIST_')],
            [sg.Slider((1,100), default_value=80, key='_SLIDER_', visible=True, enable_events=True)]
        ]

frame_layout = [
                  [sg.T('Text inside of a frame')],
                  [sg.CB('Check 1'), sg.CB('Check 2')],
               ]

frame_layout2 = [
                  [sg.T('Text inside of a frame')],
                  [sg.CB('Check 1'), sg.CB('Check 2')],
               ]

column2=[
            [sg.Spin(values=(1,2,3),initial_value=2, size=(4,1))],
            [sg.OK(), sg.Button('Exit', button_color=('white', 'red'))],
            [sg.Frame('', frame_layout, font='Any 12', title_color='blue')],
            [sg.Submit(), sg.Cancel()]
        ]



column3=[
            [sg.Spin(values=(1,2,3),initial_value=2, size=(4,1))],
            [sg.OK(), sg.Button('Exit', button_color=('white', 'red'))],
            [sg.Frame('', frame_layout2, font='Any 12', title_color='blue')],
            [sg.Submit(), sg.Cancel()]
        ]

# The GUI layout
layout =  [ 
                [sg.Column(column1, size=(500,700), scrollable=True), VerticalSeparator(pad=None), sg.Column(column2, size=(500,700)), VerticalSeparator(pad=None), sg.Column(column3, size=(500,700))],

          ]

# create the "Window"
window = sg.Window('My PySimpleGUIWeb Window', layout=layout, default_element_size=(12,1),font='Helvetica 18', size=(1500,700))

start_time = datetime.datetime.now()
#  The "Event loop" where all events are read and processed (button clicks, etc)
while True:
    event, values = window.Read(timeout=10)     # read with a timeout of 10 ms
    if event != sg.TIMEOUT_KEY:                 # if got a real event, print the info
        print(event, values)
        # also output the information into a scrolling box in the window
        # window.Element('_MULTIOUT_').Update(str(event) + '\n' + str(values), append=True)
    # if the "Exit" button is clicked or window is closed then exit the event loop
    if event in (None, 'Exit'):
        break
    if event == 'Comunication':
       print("mensaje para la vuelta")


    # Output the "uptime" statistic to a text field in the window
    window.Element('_DATE_').Update(str(datetime.datetime.now()-start_time))

# Exiting the program
window.Close()    # be sure and close the window before trying to exit the program
print('Completed shutdown')