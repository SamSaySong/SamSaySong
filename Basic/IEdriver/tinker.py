import PySimpleGUI as sg

"https://pysimplegui.readthedocs.io/en/latest/#checkbox-element-cbox-cb-check"


sg.theme('LightBlue5')
sg.popup('Hello From PySimpleGUI!', 'This is the shortest GUI program ever!')
# Define the window's contents
layout = [
          [sg.Text("What's your name?")],
          [sg.Input(key='-INPUT-')],
          [sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Input(), sg.FileBrowse()],
          [sg.Button('Ok'), sg.Button('Quit'),sg.Button('HI')]
          ]
# Create the window
window = sg.Window('Window Title', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    if event == 'Ok':
        text = sg.popup_get_text('Please enter')
        sg.popup('Results', 'The value returned from popup_get_folder', text)
    # Output a message to the window
        window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")
    if event == 'HI':
        window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Mlem")
    sg.MenuBar
# Finish up by removing from the screen
window.close()