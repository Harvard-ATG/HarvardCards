"""
This module conatins helper functions and utilities.
"""

from harvardcards.apps.flash.models import Collection, Deck
from harvardcards.apps.flash import queries
import string
import random

# For treating strings like files
import StringIO

# For excel reading/writing
import xlrd, xlwt

def parse_deck_template_file(card_template, file_contents, mappings=None):
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
            val = sheet.cell(row_index, col_index).value

            if mappings is not None:
                if fields[col_index].get_field_type() ==  'I':
                    val = mappings['Image'].get(val, '')
                if fields[col_index].get_field_type() ==  'A':
                    val = mappings['Audio'].get(val, '')
            card.append({
                "field_id": fields[col_index].id,
                "value": val,
            })
        cards.append(card)

    return cards

def template_matches_file(card_template, file_contents):
    fields = card_template.fields.all().order_by('sort_order')
    nfields = len(fields)
    workbook = xlrd.open_workbook(file_contents=file_contents)
    sheet = workbook.sheet_by_index(0)

    for col_index in range(nfields):
        val = sheet.cell(0, col_index).value
        if val != str(fields[col_index]):
            return False
    return True



def get_file_names(card_template, file_contents):
    fields = card_template.fields.all().order_by('sort_order')
    nfields = len(fields)
    columns_to_parse = []
    col_index_to_parse = []
    for field in fields:
        if field.get_field_type() in ['A','I']:
            columns_to_parse.append(str(field))
    workbook = xlrd.open_workbook(file_contents=file_contents)
    sheet = workbook.sheet_by_index(0)

    for col_index in range(nfields):
        val = sheet.cell(0, col_index).value
        if val in columns_to_parse:
            col_index_to_parse.append(col_index)

    files = []
    for row_index in range(1, sheet.nrows):
        for col_index in col_index_to_parse:
            val = sheet.cell(row_index, col_index).value
            if val not in files and val != '':
                files.append(val)

    return files

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

def generate_random_id(size=10, chars=string.ascii_uppercase + string.digits):
	'''
	Returns a random id with the given size and from the given set of characters.
	Adapted from http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
	'''
	return ''.join(random.choice(chars) for _ in range(size))

