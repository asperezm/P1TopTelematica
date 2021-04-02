# https://realpython.com/pysimplegui-python/#getting-started-with-pysimplegui
import PySimpleGUI as gui

gui.theme('DarkAmber')

layout = [  [gui.Text('Some text on Row 1')],
            [gui.Text('Enter something on Row 2'), gui.InputText()],
            [gui.Button('Test'), gui.Cancel()]
         ]


window = gui.Window('Graphic User Interface', layout)

while True:             
    event, values = window.read()
    if event in (gui.WIN_CLOSED, 'Cancel'):
        break
    if event == 'Test':
        print('test')

window.close()