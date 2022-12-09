import logging
import PySimpleGUI as sg
from inputs import CELL_MEDIUM, VALID_PROJECTS, VALID_BAC

log = logging.getLogger(__name__)

log = logging.getLogger(__name__)


class GUIApp:

    def __init__(self):
        self.in_files = []
        self.user_labels = []
        self.event_to_action = {
            "-DELETE_BAC-"  : self.delete_bac,
            "-DELETE_CC-"   : self.delete_cc,
            "-DELETE_DEV-"  : self.delete_dev,
            "-DELETE_PH-"    : self.delete_phage,
            "-DELETE_PR-"    : self.delete_prot,

            "-ADD_BAC-"     : self.add_bac,
            "-ADD_CC-"      : self.add_cc,
            "-ADD_DEV-"     : self.add_dev,
            "-ADD_PH-"      : self.add_phage,
            "-ADD_PR-"      : self.add_prot,

            "-EXPORT-"      : self.export,
            "-SAVE-"        : self.save,
            "-CELL_LINE-"   : self.add_medium,

        }
        self.table_header_to_key = {
            "Název": "Název",

        }

    def __repr__(self):
        return ({self})

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

        def bac_tab():
            size = (30, 1)
            size2 = (15, 1)
            size3 = (10, 30)
            Bac_layout = [[sg.T("bac")],
                          [sg.Frame("Enter values", size=(420, 300), layout=[
                              [sg.Text("Assay no.: ", size=size), sg.InputText(key="-ASSAY_NO_BAC-", size=size2)],
                              [sg.Text("Amount of aligoutes: ", size=size),sg.Input(key="-TOTAL_ALIQUOTES_BAC-", size=size2)],
                              [sg.Text("Solution: ", size=size), sg.Input(key="-SOL-", size=size2)],
                              [sg.Text("Project: ", size=size), sg.OptionMenu(VALID_PROJECTS, key="-PROJECT_BAC-", size=size2)],
                              [sg.Text("Bacteria: ", size=size), sg.OptionMenu(VALID_BAC, key="-BAC-", size=size2)],
                              [sg.Text("concentration: ", size=size), sg.InputText(key="-CONC_BAC-", size=size2)],
                              [sg.Text("date: ", size=size), sg.InputText(key="-DATE_BAC-", size=size2),
                               sg.CalendarButton("chose", target="-DATE_BAC-", format="%d.%m.20%y",
                                                 close_when_date_chosen=True, button_color=("Grey"))],
                              [sg.Text("")],
                              [sg.Push(), sg.Button("Add", button_color=("Grey"), key="-ADD_BAC-"),
                               sg.Button("Delete", button_color=("Grey"), key="-DELETE_BAC-"),
                               ]
                          ]),
                           sg.Frame("Entered values", size=(500, 300), layout=[
                               [sg.Column(key="-COLUMN-", layout=[
                                   [sg.Multiline(size=size3, no_scrollbar=True, pad=(0, 0), key="-LIST_ASSAY_BAC-"),
                                    sg.Multiline(size=size3, no_scrollbar=True, do_not_clear=True, pad=(0, 0), key="-LIST_SOL-"),
                                    sg.Multiline(size=(5, 30), no_scrollbar=True, pad=(0, 0), key="-LIST_ALIQ_BAC-"),
                                    sg.Multiline(size=size3, no_scrollbar=True, pad=(0, 0), key="-LIST_PROJECT_BAC-"),
                                    sg.Multiline(size=size3, no_scrollbar=True, pad=(0, 0), key="-LIST_BAC-"),
                                    sg.Multiline(size=(5, 30), no_scrollbar=True, do_not_clear=True, pad=(0, 0), key="-LIST_CONC_BAC-"),
                                    sg.Multiline(size=size3, no_scrollbar=True, do_not_clear=True, pad=(0, 0), key="-LIST_DATE_BAC-")]
                               ])]])
                           ]
                          ]
            return Bac_layout

        def cc_tab():
            size = (30, 1)
            size2 = (15, 1)
            size3 = (10, 30)
            CC_layout = [[sg.T("CC")],
                         [sg.Frame("Enter values", size=(420, 300), layout=[
                             [sg.Text("Assay no.: ", size=size), sg.InputText(key="-ASSAY_NO_CC-", size=size2)],
                             [sg.Text("Amount of aligoutes: ", size=size),
                              sg.Input(key="-TOTAL_ALIQUOTES_CC-", size=size2)],
                             [sg.Text("Project: ", size=size),
                              sg.OptionMenu(VALID_PROJECTS, key="-PROJECT_CC-", size=size2)],
                             [sg.Text("Cell line: ", size=size),
                              sg.OptionMenu(CELL_MEDIUM.keys(), key="-CELL_LINE-", size=size2)],
                             [sg.Text("Medium: ", size=size),
                              sg.OptionMenu(CELL_MEDIUM.values(), key="-MEDIUM_CC-", size=size2)],
                             [sg.Text("concentration: [x10e6 cells/ml]", size=size),
                              sg.InputText(key="-CONC_CC-", size=size2)],
                             [sg.Text("date: ", size=size), sg.InputText(key="-DATE_CC-", size=size2),
                              sg.CalendarButton("chose", target="-DATE_CC-", format="%d.%m.20%y",
                                                close_when_date_chosen=True, button_color=("Grey"))],
                             [sg.Text("")],
                             [sg.Push(), sg.Button("Add", button_color=("Grey"), key="-ADD_CC-"),
                              sg.Button("Delete", button_color=("Grey"), key="-DELETE_CC-")]
                         ]),
                          sg.Frame("Entered values", size=(500, 300), layout=[
                              [sg.Column(key="-COLUMN-", layout=[
                                  [sg.Multiline(size=size3, no_scrollbar=True, pad=(0, 0), key="-LIST_ASSAY_CC-"),
                                   sg.Multiline(size=(5, 30), no_scrollbar=True, pad=(0, 0), key="-LIST_ALIQ_CC-"),
                                   sg.Multiline(size=size3, no_scrollbar=True, pad=(0, 0), key="-LIST_PROJECT_CC-"),
                                   sg.Multiline(size=size3, no_scrollbar=True, pad=(0, 0), key="-LIST_CELL_LINE-"),
                                   sg.Multiline(size=size3, no_scrollbar=True, do_not_clear=True, pad=(0, 0),
                                                key="-LIST_MEDIUM_CC-"),
                                   sg.Multiline(size=(5, 30), no_scrollbar=True, do_not_clear=True, pad=(0, 0),
                                                key="-LIST_CONC_CC-"),
                                   sg.Multiline(size=size3, no_scrollbar=True, do_not_clear=True, pad=(0, 0),
                                                key="-LIST_DATE_CC-")]
                              ])]])
                          ]
                         ]
            return CC_layout

        def dev_tab():
            size = (30, 1)
            size2 = (15, 1)
            size3 = (10, 30)
            Dev_layout = [[sg.T("Dev")],
                          [sg.Frame("Enter values", size=(420, 300), layout=[
                              [sg.Text("Assay no.: ", size=size), sg.InputText(key="-ASSAY_NO_DEV-", size=size2)],
                              [sg.Text("Amount of aligoutes: ", size=size),
                               sg.Input(key="-TOTAL_ALIQUOTES_DEV-", size=size2)],
                              [sg.Text("Project: ", size=size),
                               sg.OptionMenu(VALID_PROJECTS, key="-PROJECT_DEV-", size=size2)],
                              [sg.Text("concentration: ", size=size), sg.InputText(key="-CONC_DEV-", size=size2)],
                              [sg.Text("date: ", size=size), sg.InputText(key="-DATE_DEV-", size=size2),
                               sg.CalendarButton("chose", target="-DATE_DEV-", format="%d.%m.20%y",
                                                 close_when_date_chosen=True, button_color=("Grey"))],
                              [sg.Text("")],
                              [sg.Push(), sg.Button("Add", button_color=("Grey"), key="-ADD_DEV-"),
                               sg.Button("Delete", button_color=("Grey"), key="-DELETE_DEV-"), ]
                          ]),
                           sg.Frame("Entered values", size=(500, 300), layout=[
                               [sg.Column(key="-COLUMN_DEV-", layout=[
                                   [sg.Multiline(size=size3, no_scrollbar=True, pad=(0, 0), key="-LIST_ASSAY_DEV-"),
                                    sg.Multiline(size=(5, 30), no_scrollbar=True, pad=(0, 0), key="-LIST_ALIQ_DEV-"),
                                    sg.Multiline(size=size3, no_scrollbar=True, pad=(0, 0), key="-LIST_PROJECT_DEV-"),
                                    sg.Multiline(size=(5, 30), no_scrollbar=True, do_not_clear=True, pad=(0, 0),
                                                 key="-LIST_CONC_DEV-"),
                                    sg.Multiline(size=size3, no_scrollbar=True, do_not_clear=True, pad=(0, 0),
                                                 key="-LIST_DATE_DEV-")]
                               ])]])
                           ]
                          ]
            return Dev_layout

        def phage_tab():
            size = (30, 1)
            size2 = (15, 1)
            size3 = (10, 30)
            Phage_layout = [[sg.T("")],
                            [sg.Frame("Enter values", size=(420, 300), layout=[
                                [sg.Text("Assay no.: ", size=size), sg.InputText(key="-ASSAY_NO_PH-", size=size2)],
                                [sg.Text("Amount of aligoutes: ", size=size),
                                 sg.Input(key="-TOTAL_ALIQUOTES_PH-", size=size2)],
                                [sg.Text("Project: ", size=size),
                                 sg.OptionMenu(VALID_PROJECTS, key="-PROJECT_PH-", size=size2)],
                                [sg.Text("concentration: ", size=size), sg.InputText(key="-CONC_PH-", size=size2)],
                                [sg.Text("date: ", size=size), sg.InputText(key="-DATE_PH-", size=size2),
                                 sg.CalendarButton("chose", target="-DATE_PH-", format="%d.%m.20%y",
                                                   close_when_date_chosen=True, button_color=("Grey"))],
                                [sg.Text("")],
                                [sg.Push(), sg.Button("Add", button_color=("Grey"), key="-ADD_PH-"),
                                 sg.Button("Delete", button_color=("Grey"), key="-DELETE_PH-"), ]
                            ]),
                             sg.Frame("Entered values", size=(500, 300), layout=[
                                 [sg.Column(key="-COLUMN_PH-", layout=[
                                     [sg.Multiline(size=size3, no_scrollbar=True, pad=(0, 0), key="-LIST_ASSAY_PH-"),
                                      sg.Multiline(size=(5, 30), no_scrollbar=True, pad=(0, 0), key="-LIST_ALIQ_PH-"),
                                      sg.Multiline(size=size3, no_scrollbar=True, pad=(0, 0), key="-LIST_PROJECT_PH-"),
                                      sg.Multiline(size=(5, 30), no_scrollbar=True, do_not_clear=True, pad=(0, 0),
                                                   key="-LIST_CONC_PH-"),
                                      sg.Multiline(size=size3, no_scrollbar=True, do_not_clear=True, pad=(0, 0),
                                                   key="-LIST_DATE_PH-")]
                                 ])]])
                             ]
                            ]
            return Phage_layout

        def protein_tab():
            size = (30, 1)
            size2 = (15, 1)
            size3 = (10, 30)
            Protein_layout = [[sg.T("")],
                              [sg.Frame("Enter values", size=(420, 300), layout=[
                                  [sg.Text("Assay no.: ", size=size), sg.InputText(key="-ASSAY_NO_PR-", size=size2)],
                                  [sg.Text("Amount of aligoutes: ", size=size),
                                   sg.Input(key="-TOTAL_ALIQUOTES_PR-", size=size2)],
                                  [sg.Text("Project: ", size=size),
                                   sg.OptionMenu(VALID_PROJECTS, key="-PROJECT_PR-", size=size2)],
                                  [sg.Text("concentration: ", size=size), sg.InputText(key="-CONC_PR-", size=size2)],
                                  [sg.Text("date: ", size=size), sg.InputText(key="-DATE_PR-", size=size2),
                                   sg.CalendarButton("chose", target="-DATE_PR-", format="%d.%m.20%y",
                                                     close_when_date_chosen=True, button_color=("Grey"))],
                                  [sg.Text("")],
                                  [sg.Push(), sg.Button("Add", button_color=("Grey"), key="-ADD_PR-"),
                                   sg.Button("Delete", button_color=("Grey"), key="-DELETE_PR-"), ]
                              ]),
                               sg.Frame("Entered values", size=(500, 300), layout=[
                                   [sg.Column(key="-COLUMN_PR-", layout=[
                                       [sg.Multiline(size=size3, no_scrollbar=True, pad=(0, 0), key="-LIST_ASSAY_PR-"),
                                        sg.Multiline(size=(5, 30), no_scrollbar=True, pad=(0, 0), key="-LIST_ALIQ_PR-"),
                                        sg.Multiline(size=size3, no_scrollbar=True, pad=(0, 0), key="-LIST_PROJECT_PR-"),
                                        sg.Multiline(size=(5, 30), no_scrollbar=True, do_not_clear=True, pad=(0, 0),
                                                     key="-LIST_CONC_PR-"),
                                        sg.Multiline(size=size3, no_scrollbar=True, do_not_clear=True, pad=(0, 0),
                                                     key="-LIST_DATE_PR-")]
                                   ])]])
                               ]
                              ]
            return Protein_layout

        layout = [[sg.Menu(tool_bar_menu())],
                  [sg.TabGroup([[sg.Tab("Bacterial", layout=bac_tab()),
                                sg.Tab("Cell Culture", layout=cc_tab()),
                                sg.Tab("Development", layout=dev_tab()),
                                sg.Tab("Phage", layout=phage_tab()),
                                sg.Tab("Protein", layout=protein_tab())]]
                               )],
                  [sg.Push(), sg.Button("Clear"), sg.Button("Export", key="-EXPORT-"), sg.Button("Save", key="-SAVE-"), sg.Button("Close")]
                  ]

        return sg.Window("Zadejte", layout, auto_size_text=True, finalize=True)

    def add_medium(self, values):
        data = (CELL_MEDIUM.get("cell_line", "")),
        print(data)
        self.window["-MEDIUM-"].Update(values["CELL_MEDIUM"])

    # mazací funkce
    def delete_bac(self, values):
        self.window["-ASSAY_NO_BAC-"].Update("")
        self.window["-SOL-"].Update("")
        self.window["-TOTAL_ALIQUOTES_BAC-"].Update("")
        self.window["-PROJECT_BAC-"].Update("")
        self.window["-BAC-"].Update("")
        self.window["-CONC_BAC-"].Update("")
        self.window["-DATE_BAC-"].Update("")

    def delete_cc(self, values):
        self.window["-ASSAY_NO_CC-"].Update("")
        self.window["-TOTAL_ALIQUOTES_CC-"].Update("")
        self.window["-PROJECT_CC-"].Update("")
        self.window["-CELL_LINE-"].Update("")
        self.window["-MEDIUM_CC-"].Update("")
        self.window["-CONC_CC-"].Update("")
        self.window["-DATE_CC-"].Update("")

    def delete_dev(self, values):
        self.window["-ASSAY_NO_DEV-"].Update("")
        self.window["-TOTAL_ALIQUOTES_DEV-"].Update("")
        self.window["-PROJECT_DEV-"].Update("")
        self.window["-CONC_DEV-"].Update("")
        self.window["-DATE_DEV-"].Update("")

    def delete_phage(self, values):
        self.window["-ASSAY_NO_PH-"].Update("")
        self.window["-TOTAL_ALIQUOTES_PH-"].Update("")
        self.window["-PROJECT_PH-"].Update("")
        self.window["-CONC_PH-"].Update("")
        self.window["-DATE_PH-"].Update("")

    def delete_prot(self, values):
        self.window["-ASSAY_NO_PR-"].Update("")
        self.window["-TOTAL_ALIQUOTES_PR-"].Update("")
        self.window["-PROJECT_PR-"].Update("")
        self.window["-CONC_PR-"].Update("")
        self.window["-DATE_PR-"].Update("")


    # přidávací funkce
    def add_bac(self, values):
        total_aliquotes = int(values["-TOTAL_ALIQUOTES_BAC-"])
        batch_no = 0
        for cislo in range(total_aliquotes):
            batch_no += 1
            self.window["-LIST_ASSAY_BAC-"].print(values["-ASSAY_NO_BAC-"])
            self.window["-LIST_SOL-"].print(values["-SOL-"])
            self.window["-LIST_ALIQ_BAC-"].print(f'{batch_no}/{values["-TOTAL_ALIQUOTES_BAC-"]}')
            self.window["-LIST_PROJECT_BAC-"].print(values["-PROJECT_BAC-"])
            self.window["-LIST_BAC-"].print(values["-BAC-"])
            self.window["-LIST_CONC_BAC-"].print(values["-CONC_BAC-"])
            self.window["-LIST_DATE_BAC-"].print(values["-DATE_BAC-"])

    def add_cc(self, values):
        total_aliquotes = int(values["-TOTAL_ALIQUOTES_CC-"])
        batch_no = 0
        for cislo in range(total_aliquotes):
            batch_no += 1
            self.window["-LIST_ASSAY_CC-"].print(values["-ASSAY_NO_CC-"])
            self.window["-LIST_ALIQ_CC-"].print(f'{batch_no}/{values["-TOTAL_ALIQUOTES_CC-"]}')
            self.window["-LIST_PROJECT_CC-"].print(values["-PROJECT_CC-"])
            self.window["-LIST_CELL_LINE-"].print(values["-CELL_LINE-"])
            self.window["-LIST_MEDIUM_CC-"].print(values["-MEDIUM_CC-"])
            self.window["-LIST_CONC_CC-"].print(values["-CONC_CC-"])
            self.window["-LIST_DATE_CC-"].print(values["-DATE_CC-"])

    def add_dev(self, values):
        total_aliquotes = int(values["-TOTAL_ALIQUOTES_DEV-"])
        batch_no = 0
        for cislo in range(total_aliquotes):
            batch_no += 1
            self.window["-LIST_ASSAY_DEV-"].print(values["-ASSAY_NO_DEV-"])
            self.window["-LIST_ALIQ_DEV-"].print(f'{batch_no}/{values["-TOTAL_ALIQUOTES_DEV-"]}')
            self.window["-LIST_PROJECT_CC-"].print(values["-PROJECT_CC-"])
            self.window["-LIST_CONC_DEV-"].print(values["-CONC_DEV-"])
            self.window["-LIST_DATE_DEV-"].print(values["-DATE_DEV-"])

    def add_phage(self, values):
        total_aliquotes = int(values["-TOTAL_ALIQUOTES_PH-"])
        batch_no = 0
        for cislo in range(total_aliquotes):
            batch_no += 1
            self.window["-LIST_ASSAY_PH-"].print(values["-ASSAY_NO_PH-"])
            self.window["-LIST_ALIQ_PH-"].print(f'{batch_no}/{values["-TOTAL_ALIQUOTES_PH-"]}')
            self.window["-LIST_PROJECT_PH-"].print(values["-PROJECT_PH-"])
            self.window["-LIST_CONC_PH-"].print(values["-CONC_PH-"])
            self.window["-LIST_DATE_PH-"].print(values["-DATE_PH-"])

    def add_prot(self, values):
        total_aliquotes = int(values["-TOTAL_ALIQUOTES_PR-"])
        batch_no = 0
        for cislo in range(total_aliquotes):
            batch_no += 1
            self.window["-LIST_ASSAY_PR-"].print(values["-ASSAY_NO_PR-"])
            self.window["-LIST_ALIQ_PR-"].print(f'{batch_no}/{values["-TOTAL_ALIQUOTES_PR-"]}')
            self.window["-LIST_PROJECT_PR-"].print(values["-PROJECT_PR-"])
            self.window["-LIST_CONC_PR-"].print(values["-CONC_PR-"])
            self.window["-LIST_DATE_PR-"].print(values["-DATE_PR-"])

    def add_control(self, values, event):
        if values["-ASSAY_NO-"] == "" and event == "add":
            sg.PopupOK("Warning")

    # tlačítkové funkce
    def export(self, values):
        print("exportuji: ", self.window["-COLUMN-"])

    def save(self, values):
        print("ukládám: ", self.window["-COLUMN-"])


def gui_main():
    log.info('starting gui app')

    with GUIApp() as gui:
        gui.run()

    return 0
