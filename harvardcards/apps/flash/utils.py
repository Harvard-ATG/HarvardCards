"""
This module conatins helper functions and utilities.
"""

from harvardcards.apps.flash.models import Collection, Deck
from harvardcards.apps.flash import queries

# For treating strings like files
import StringIO

# For excel reading/writing
import xlrd, xlwt

def parse_deck_template_file(card_template, file_contents):
    """Parses a spreadsheet into a list of cards."""
    fields = card_template.fields.all().order_by('sort_order')
    nfields = len(fields)

    workbook = xlrd.open_workbook(file_contents=file_contents)
    sheet = workbook.sheet_by_index(0)

    cards = []
    for row_index in range(sheet.nrows):
        if row_index == 0:
            continue # Skip header row
        card = []
        for col_index in range(nfields):
            card.append({
                "field": fields[col_index],
                "value": sheet.cell(row_index, col_index).value,
            })
        cards.append(card)

    return cards

def create_deck_template_file(card_template):
    """Creates a spreadsheet template for populating a deck of cards."""
    card_template_fields = card_template.fields.all().order_by('sort_order')

    output = StringIO.StringIO()
    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('sheet1')

    row = 0
    for idx, field in enumerate(card_template_fields):
        worksheet.write(row, idx, label=field.label)

    workbook.save(output)
    file_output = output.getvalue()
    output.close()

    return file_output

def create_deck_file(deck_id):
    """Creates a spreadsheet containing a deck of cards."""
    deck = Deck.objects.get(id=deck_id)

    output = StringIO.StringIO()
    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('sheet1')
    card_list = queries.getDeckCardsList(deck_id)

    row = 0
    for card in card_list:
        if row == 0:
            for idx, field in enumerate(card['fields']):
                worksheet.write(row, idx, label=field['label'])
        row = row + 1
        for idx, field in enumerate(card['fields']):
            worksheet.write(row, idx, label=field['value'])

    workbook.save(output)
    file_output = output.getvalue()
    output.close()

    return file_output

