import PySimpleGUI as sg
import pickle

def make_startwin():
    layout = [[sg.Text('Open .npy File'), sg.Text('      ', k='-OUTPUT-')],
              [sg.Input(""), sg.FileBrowse(k='loaded')],
              [sg.Text(size=(25, 1), k='-OUTPUT1-')],
              [sg.Button('Submit')],
              [sg.Button('Data Points'), sg.Button('Plots'), sg.Button('Exit')]]
    return sg.Window('Graphic Note Taker', layout, location=(800,600), resizable=True, finalize=True)
def make_statwin():
    layout = [[sg.Text('Insert Data Points')],
              [sg.Input(key='-IN-', enable_events=True)],
              [sg.Text(size=(25,1), k='-OUTPUT-')],
              [sg.Button('Save'), sg.Button('Popup'), sg.Button('Exit')]]
    return sg.Window('Second Window', layout, finalize=True)
window1, window2 = make_startwin(), None        # start off with 1 window open
while True:             # Event Loop
    window, event, values = sg.read_all_windows()

    if event == sg.WIN_CLOSED or event == 'Exit':
        window.close()
        if window == window2:       # if closing win 2, mark as closed
            window2 = None
        elif window == window1:     # if closing win 1, exit program
            break
    elif event == 'Submit':
        print(values["loaded"])
        data = values["loaded"]
        window['-OUTPUT1-'].update(f'You entered {data}')
    elif event == 'Plots':
        sg.popup('This is a BLOCKING popup','all windows remain inactive while popup active')
    elif event == 'Data Points' and not window2:
        window2 = make_statwin()
    elif event == '-IN-':
        window['-OUTPUT-'].update(f'You entered {values["-IN-"]}')
    elif event == 'Save':
        a_file = open("data.pkl", "wb")
        pickle.dump(values["-IN-"], a_file)
        a_file.close()
window.close()