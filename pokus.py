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
    medium = CELL_MEDIUM.get(values["-C-"])
    return medium

sg.theme("DarkBlue")

def tab1_layout():
    tab1_layout = [[sg.T("")],
               [sg.Text("linie: ", size=(15, 1)), sg.InputOptionMenu(values=CELL_MEDIUM.keys(), key="-C-")],
               [sg.Text("medium", size=(15, 1)), sg.OptionMenu(values=CELL_MEDIUM.values(), key="-M-")]
               ]
    return tab1_layout

tab2_layout = [[sg.T("Phage Display")]]


layout = [[sg.TabGroup([[
                sg.Tab("Cell Culture", layout=tab1_layout()),
                sg.Tab("Phage Display", layout=tab2_layout)
        ]])],
        [sg.Button("OK"), sg.Button("Cancel")]
    ]

window = sg.Window("Vyber", layout, finalize=True)
window.bind('<FocusOut>', '+FOCUS OUT+')

window["-C-"].bind("<Leave>", "+L+")
window["-C-"].bind("<Button>", "+C+")
window["-C-"].bind("<DoubleButton>", "+DB+")
window["-C-"].bind("<Enter>", "+E+")
window["-M-"].bind("<Enter>", "+ENTER+")

while True:
    event, values = window.read()
    if event == "Cancel" or event == sg.WINDOW_CLOSED:
        break
    elif event == "-C-":
        pass
    elif event == "-C-" + "+C+":
        print("první vstup")
    elif event == ("-C-" + "+C+") and event == ("-C-" + "+E+"):
        print("druhý vstup")
    elif event == "-M-" + "+ENTER+":
        window["-M-"].Update(get_medium())
        print("přiřazeno médium")
    elif event == "OK":
        print(get_medium())


    if values["-C-"] == "" and event == "OK":
        print("Nevybrali jste linii")
        sg.PopupOK("Nevybrali jste linii", title="Warning", image=sg.EMOJI_BASE64_FACEPALM, keep_on_top=True)

window.close()