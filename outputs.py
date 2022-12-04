import logging
from pathlib import Path

from docxtpl import DocxTemplate

from calc import enumerate_keys
from calc import merge_page_data
from calc import prepare_rows
from calc import split_to_page_size

WORD_OUTPUT_NAME = 'generated_labels'
OUTPUT_FOLDER = 'output'

log = logging.getLogger(__name__)


def to_console(data):
    """Print labels to console.

    Only for testing purposes.
    """
    from textwrap import dedent
    from string import Template

    log.info('outputting to console')

    template = Template(dedent("""
    ┌──────────────────────────────┐
    │${raw1_txt}│                   
    │${raw2_txt}│
    │${raw3_txt}│
    │${raw4_txt}│
    │${raw5_txt}│
    └──────────────────────────────┘
    """))

    for item in data:
        raw1 = f'{item["assay_no"]}: poř. číslo/{item["total_aliquotes"]}'
        raw2 = f'{item["project"]}'
        raw3 = f'{item["cell_line"]}'
        raw4 = f'in {item["medium"]}/10%DMSO'
        raw5 = f'{item["conc"]}x10e6 c/ml    {item["date"]}'

        sub = {
            'raw1_txt'  : f'{raw1:^30}',
            'raw2_txt'  : f'{raw2:^30}',
            'raw3_txt'  : f'{raw3:^30}',
            'raw4_txt'  : f'{raw4:^30}',
            'raw5_txt'  : f'{raw5:^30}',
            }

        filled = template.substitute(sub)
        print(filled)


def to_word(data, template):
    """Output the label data to word files."""
    log.info('output to word started')

    # prepare output folder
    Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

    # reformat the dicts for replace
    data = prepare_rows(data)

    # prepare paginated data
    page_splitted_data = split_to_page_size(data)

    # for each page
    for page_num, page_data in enumerate(page_splitted_data, start=1):
        # open new template for each page
        doc = DocxTemplate(template)

        # prepare the numbers for replacing
        replace_ready = enumerate_keys(page_data)
        context = merge_page_data(replace_ready)
        # make the replacement
        log.debug(f'replacing page {page_num}')
        doc.render(context=context)

        # save to new file
        filename = f'{page_num:02}_{WORD_OUTPUT_NAME}.docx'
        log.debug(f'saving to file {filename}')
        doc.save(Path(OUTPUT_FOLDER) / filename)

    log.info('output to word finished')
