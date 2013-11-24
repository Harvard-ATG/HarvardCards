import os

def loaddata(file):
    if os.path.splitext(file)[1] == '.json':
        print file
        os.system("python manage.py loaddata %s" % file)

files = []
files.append(os.path.join(os.path.dirname(__file__),'harvardcards/apps/flash/fixtures/','initial_data_collection.json'))
files.append(os.path.join(os.path.dirname(__file__),'harvardcards/apps/flash/fixtures/','initial_data_decks.json'))
files.append(os.path.join(os.path.dirname(__file__),'harvardcards/apps/flash/fixtures/','initial_data_cards.json'))
files.append(os.path.join(os.path.dirname(__file__),'harvardcards/apps/flash/fixtures/','initial_data_fields.json'))
files.append(os.path.join(os.path.dirname(__file__),'harvardcards/apps/flash/fixtures/','initial_data_cards_fields.json'))
files.append(os.path.join(os.path.dirname(__file__),'harvardcards/apps/flash/fixtures/','initial_data_decks_cards.json'))
map(loaddata, files)