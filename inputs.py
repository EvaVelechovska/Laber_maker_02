"""Inputs.

Take input and return data in format of list[dict]


Example of output:
[
    {
    'assay_no': 'Eve_123', "aliquote": '20',
    'project': 'No. 23',
    'cell_line': 'COLO205'
    'conc': 'x10e6 cell/ml',
    'medium': 'RPMI/10%DMSO',
    'date': '23.1.2010',
    },
    {
    'assay_no': 'Eve_123', "aliquote": '2/20',
    'project': 'No. 23',
    'cell_line': 'COLO205'
    'conc': 'x10e6 cell/ml',
    'medium': 'RPMI/10%DMSO',
    'date': '23.1.2010',
    },
    {...},
    {...},
]

"""
import csv
import logging
from database_app import project_database_con, cell_culture_database_con, bac_database_con, phage_database_con, dev_database_con

log = logging.getLogger(__name__)

# All
VALID_PROJECTS = project_database_con()

# Bacteria
VALID_BAC = ["E.Coli XL1", "E.Coli RV21", "B"]

# Cell Culture
VALID_CELL_LINES = ["COLO205", "Jurkat", "HELL", "HEK-293", "CHO-K1"]
VALID_MEDIUM = ["DMEM", "RPMI"]
CELL_MEDIUM = {
    "COLO205"   : "RPMI",
    "Jurkat"    : "RPMI",
    "HEK-2P3"   : "DMEM",
    "CHO-K1"    : "RPMI",
    "HELL"      : "DMEM/FBS"
}


def better_input(question, value_type, valid_options=None):
    """Validate input based on the passed value type.

    Upon error continuously prompt user for correct answer.
    """

    while True:
        try:
            answer = value_type(input(f'{question}{valid_options if valid_options is not None else ""}: '))

            if valid_options and answer not in valid_options:
                raise ValueError('neni z povolených hodnot')

            if not answer:
                raise ValueError('Nepovolujeme prázné hodnoty a nuly.')

        except ValueError:
            print('Špatně zadaná hodnota')

        else:
            return answer


def user_input():
    """Take input from user.

    Exmaple input:
    'assay_no': 'Eve_123',
    "total_aliquotes": 20,
    'project': 'No. 23',
    'cell_line': 'COLO205'
    'conc': '10x10e6 cell/ml',
    'medium': 'RPMI/10%DMSO',
    'date': '23.1.2010',
        -- další? [a/n]:
    """

    entries = []
    while True:
        item = {
            'assay_no'      : better_input('assay_no', str),
            'total_aliquotes'     : better_input('total_aliquotes', int),
            'project'       : better_input('project', str, valid_options=VALID_PROJECTS),
            'cell_line'     : better_input('cell line', str, valid_options=CELL_MEDIUM.keys()),
            'conc'          : better_input('conc', int),
            #'medium'        : better_input('medium', str, valid_options=VALID_MEDIUM),
            'date'          : better_input('date', str),
        }
        item["medium"] = CELL_MEDIUM.get(item["cell_line"], "")
        entries.append(item)

        next_q = input('-- další? [a/n]: ')
        if next_q == 'n':
            return entries


def csv_input(file_path):
    pass
    """Load data from csv."""
    log.info('loading data from csv file')
    with open(file_path, encoding='UTF-8') as file:
        reader = csv.DictReader(file, quoting=csv.QUOTE_NONNUMERIC)
        data = list(reader)
    for item in data:
        VALID_PROJECTS.append(item)
        #item["unit"] = VALID_FORMS.get(item["form"], "")
    # TODO: validate data, remove and notify about the unvalid
    return data
