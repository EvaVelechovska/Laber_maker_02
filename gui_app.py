import logging
import PySimpleGUI as sg
from inputs import CELL_MEDIUM, VALID_PROJECTS, VALID_CELL_LINES

log = logging.getLogger(__name__)

log = logging.getLogger(__name__)


class GUIApp:

    def __init__(self):
        self.in_files = []
        self.user_labels = []
        self.event_to_action = {
            "-DELETE-"  : self.delete,
            "-ADD-"     : self.add,
            "-EXPORT-"  : self.export,
            "-SAVE-"    : self.save,


        }
        self.table_header_to_key = {
            "Název": "Název",

        }

    def __enter__(self):
        self.window = self.create_window()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.window.close()

    def __eat_events__(self):
        """Eats falsely fired events
        NOTE: https://github.com/PySimpleGUI/PySimpleGUI/issues/4268
        """
        while True:
            event, values = self.window.read(timeout=0)
            if event == '__TIMEOUT__':
                break
        return

    def run(self):
        while True:
            event, values = self.window.read()
            log.debug((event, values))

            if event == sg.WIN_CLOSED or event == "Close":  # always,  always give a way out!
                break

            # do actions
            try:
                self.event_to_action[event](values)
                self.__eat_events__()

            except KeyError:
                log.exception('unknown event')

    def create_window(self):
        sg.theme("Darkblue")


        def tool_bar_menu():
            menuBar_Layout = [
                ['&File', ['&Open     Ctrl-O', '&Save       Ctrl-S', 'E&xit']],
                ['&Edit', ['back']],
                ['&Toolbar', ['---', 'Command &1::Command_Key', 'Command &2', '---', 'Command &3', 'Command &4']],
                ['&Help', ['&About...']]
            ]
            return menuBar_Layout
        size = (30, 1)
        size2 = (15, 1)
        size3 = (10, 30)
        layout = [  [sg.Menu(tool_bar_menu())],
                    [sg.Frame("Enter values", size=(420, 300), layout=[
                      [sg.Text("Assay no.: ", size=size), sg.InputText(key="-ASSAY_NO-", size=size2)],
                      [sg.Text("Amount of aligoutes: ", size=size), sg.Input(key="-TOTAL_ALIQUOTES-", size=size2)],
                      [sg.Text("Project: ", size=size), sg.OptionMenu(VALID_PROJECTS, key="-PROJECT-", size=size2)],
                      [sg.Text("Cell line: ", size=size), sg.OptionMenu(CELL_MEDIUM.keys(), key="-CELL_LINE-", size=size2)],
                      [sg.Text("Medium: ", size=size), sg.InputText(key="-MEDIUM-", size=size2)],
                      [sg.Text("concentration: [x10e6 cells/ml]", size=size), sg.InputText(key="-CONC-", size=size2)],
                      [sg.Text("date: ", size=size), sg.InputText(key="-DATE-", size=size2),
                       sg.CalendarButton("chose", target="-DATE-", format="%d.%m.20%y", close_when_date_chosen=True, button_color=("Grey"))],
                      [sg.Text("")],
                      [sg.Push(), sg.Button("Add", button_color=("Grey"), key="-ADD-"),
                       sg.Button("Delete", button_color=("Grey"), key="-DELETE-"),
                       sg.Button("Pokus", key="-POKUS-")]
                        ]),
                    sg.Frame("Entered values", size=(420, 300), layout=[
                        [sg.Column(key="-COLUMN-",layout=[
                            [sg.Multiline(size=size3, no_scrollbar=True, pad=(0, 0), key="-LIST_ASSAY-"),
                             sg.Multiline(size=(5, 30), no_scrollbar=True, pad=(0, 0), key="-LIST_ALIQ-"),
                            sg.Multiline(size=size3, no_scrollbar=True, pad=(0, 0), key="-LIST_PROJECT-"),
                             sg.Multiline(size=size3, no_scrollbar=True, pad=(0, 0), key="-LIST_CELL_LINE-"),
                             sg.Multiline(size=size3, no_scrollbar=True, do_not_clear=True, pad=(0, 0), key="-LIST_MEDIUM-"),
                             sg.Multiline(size=size3, no_scrollbar=True, do_not_clear=True, pad=(0, 0), key="-LIST_CONC-"),
                             sg.Multiline(size=size3, no_scrollbar=True, do_not_clear=True, pad=(0, 0), key="-LIST_DATE-")]
                        ])]])
                    ],
                    [sg.Push(), sg.Button("Export", key="-EXPORT-"), sg.Button("Save", key="-SAVE-"), sg.Button("Close")]
                  ]

        return sg.Window("Zadejte", layout, auto_size_text=True,finalize=True)


    def delete(self, values):
        self.window["-ASSAY_NO-"].Update("")
        self.window["-TOTAL_ALIQUOTES-"].Update("")
        self.window["-PROJECT-"].Update("")
        self.window["-CELL_LINE-"].Update("")
        self.window["-MEDIUM-"].Update("")
        self.window["-CONC-"].Update("")
        self.window["-DATE-"].Update("")

    def add(self, values):
        total_aliquotes = int(values["-TOTAL_ALIQUOTES-"])
        batch_no = 0
        for cislo in range(total_aliquotes):
            batch_no += 1

            self.window["-LIST_ASSAY-"].print(values["-ASSAY_NO-"])
            self.window["-LIST_ALIQ-"].print(f'{batch_no}/{values["-TOTAL_ALIQUOTES-"]}')
            self.window["-LIST_PROJECT-"].print(values["-PROJECT-"])
            self.window["-LIST_CELL_LINE-"].print(values["-CELL_LINE-"])
            self.window["-LIST_MEDIUM-"].print(values["-MEDIUM-"])
            self.window["-LIST_CONC-"].print(values["-CONC-"])
            self.window["-LIST_DATE-"].print(values["-DATE-"])


    def export(self, values):
        print("exportuji: ", self.window["-COLUMN-"])

    def save(self, values):
        print("ukládám: ", self.window["-COLUMN-"])

def gui_main():
    log.info('starting gui app')

    with GUIApp() as gui:
        gui.run()

    return 0
