import PySimpleGUI as sg
gif1 = "My Project.gif"
gifs = [gif1]

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Some text on Row 1')],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Image(background_color = "white", key = "animation")],
            [sg.Button('Ok'), sg.Button('Cancel')],
          ]


# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
image = window["animation"]
while True:
    event, values = window.read(timeout = 100)
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    image.update_animation(gif1, 100)
    #print('You entered ', values[0])

window.close()
