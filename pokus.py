import PySimpleGUI as sg
import gui_app as g
from inputs import CELL_MEDIUM, VALID_PROJECTS

#{
#            "COLO205": "RPMI",
#            "Jurkat": "RPMI",
#            "HEK-2P3": "DMEM",
#            "CHO-K1": "RPMI",
#            "HELL": "DMEM/FBS"
#        }


def get_medium():
    linie = values["-C-"]
    medium = CELL_MEDIUM.get(values["-C-"])
    #print(linie, medium)
    return medium

sg.theme("DarkBlue")

layout = [
    [sg.Text("linie: ", size=(15, 1)), sg.InputOptionMenu(values=CELL_MEDIUM.keys(), key="-C-")],
    [sg.Text("medium", size=(15, 1)), sg.Text("", key="-M-")],
    [sg.Button("OK"), sg.Button("Cancel")]
    ]

window = sg.Window("Vyber", layout, finalize=True)
window["-C-"].bind("<Button>", "+RIGHT CLICK+")
window["-M-"].bind("<Button>", "+RIGHT CLICK+")

while True:
    event, values = window.read()
    if event == "Cancel" or event == sg.WINDOW_CLOSED:
        break
    elif event == "-C-":
        pass
    elif event == "-C-" + "+RIGHT CLICK+":
        pass
    elif event == "-M-":
        pass


    elif event == "OK":
        print(get_medium())



    if values["-C-"] == "" and event == "OK":
        print("Nevybrali jste linii")
        sg.PopupOK("Nevybrali jste linii", title="Warning", image=sg.EMOJI_BASE64_FACEPALM, keep_on_top=True)

window.close()