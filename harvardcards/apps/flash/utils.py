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

def parse_deck_template_file(card_template, file_contents, mappings=None, custom=False):
    """Parses a spreadsheet into a list of cards."""
    fields = card_template.fields.all().order_by('sort_order')
    nfields = len(fields)
    workbook = xlrd.open_workbook(file_contents=file_contents)
    sheet = workbook.sheet_by_index(0)
    cards = []
    for row_index in range(sheet.nrows):
        if custom:
            rows_to_skip = [0, 1, 2]
        else:
            rows_to_skip = [0]
        if row_index in rows_to_skip:
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
    """
    Checks if the uploaded spreadsheet has the same template as the collection.
    """
    workbook = xlrd.open_workbook(file_contents=file_contents)
    sheet = workbook.sheet_by_index(0)

    fields = card_template.fields.all().order_by('sort_order')
    nfields = len(fields)

    if nfields != sheet.ncols:
        return False

    for col_index in range(sheet.ncols):
        val = sheet.cell(0, col_index).value
        if val != str(fields[col_index]):
            return False
    return True


def correct_custom_format(file_contents):
    """
    Checks if the uploaded spreadsheet follows the correct format.
    """
    workbook = xlrd.open_workbook(file_contents=file_contents)
    sheet = workbook.sheet_by_index(0)

    for col_index in range(sheet.ncols):
        val = sheet.cell(1, col_index).value
        if val not in ['Front', 'Back']:
            return False
        val = sheet.cell(2, col_index).value
        if val not in ['Audio', 'Image', 'Text', 'Video']:
            return False
    return True


def get_card_template(file_contents):
    """
    Returns the card template parsed from the uploaded spreadsheet.
    """
    workbook = xlrd.open_workbook(file_contents=file_contents)
    sheet = workbook.sheet_by_index(0)
    fields = []
    for col_index in range(sheet.ncols):
        field = {
                "label": sheet.cell(0, col_index).value,
                "side": sheet.cell(1, col_index).value,
                "type": sheet.cell(2, col_index).value
                }
        fields.append(field)
    return fields

def get_file_names(card_template, file_contents, custom=False):
    """
    Returns the file names that appear in the uploaded spreadsheet.
    """
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
    if custom:
        start_row = 3
    else:
        start_row = 1
    for row_index in range(start_row, sheet.nrows):
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
    file_output = workbook
    #file_output = output.getvalue()
    output.close()

    return file_output



def generate_random_id(size=10, chars=string.ascii_uppercase + string.digits):
	"""
	Returns a random id with the given size and from the given set of characters.
	Adapted from http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
	"""
	return ''.join(random.choice(chars) for _ in range(size))

def create_custom_template_file():
    """
    Creates a sample custom template spreadsheet.
    """
    output = StringIO.StringIO()
    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('sheet1')
    rows = [['Image', 'Artist','Date', 'Title', 'Materials', 'Location', 'Audio'],
            ['Front', 'Front', 'Front', 'Back', 'Back', 'Back', 'Front'],
            ['Image', 'Text', 'Text', 'Text', 'Text', 'Text', 'Audio'],
            ['','Some artist','','','','','sound.mp3'],
            ['pisa_tower.jpeg', '','','','','','']]

    for i in range(len(rows)):
        row = rows[i]
        for j in range(len(row)):
            worksheet.write(i, j, label=row[j])

    workbook.save(output)
    file_output = output.getvalue()
    output.close()

    return file_output
