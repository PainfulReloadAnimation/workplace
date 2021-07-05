import io

import PySimpleGUI as sg
from PIL import Image, ImageTk

def Inject_crt_Object(obj_crt_API):
    # Make the crt variable global for use in multiple functions in the
    # module that might need access to the crt object.
    global crt
    global SCRIPT_TAB
    # Associate the crt variable with the crt object passed in from the
    # Main script.
    crt = obj_crt_API
    SCRIPT_TAB = crt.GetScriptTab()
    SCRIPT_TAB.Screen.Synchronous = True
    return


def get_img_data(f, maxsize=(1000, 650), first=False):
    """Generate image data using PIL
    """
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:  # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)

filename = "C:\\Users\\bca494\\project\\GraphicAddon\\switch.png"
image_elem = sg.Image(data=get_img_data(filename, first=True))


def make_win():
    layout = [[image_elem],
              [sg.Button('Data Points'), sg.Button('Plots'), sg.Button('Exit')]]

    return sg.Window('Graphic Note Taker', layout, location=(800, 600), resizable=True, finalize=True)


def new_window():

    win = make_win()
    while True:  # Event Loop
        window, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            break

    window.close()


