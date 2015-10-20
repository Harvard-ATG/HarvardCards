#
# The script creates the json files which can be directly imported into HarvardCards Django App.
# It looks for the json file in the folder specified by the variable "path_files_folder"
# Usage:
#   ./initial_data.py [json_file]
# Note: For now, you can execute ./initial_data.py and the script will use the arthistoryflash.json file.


import json
import os
import sys
from get_initial_pks import get_initial_pks

path_files_folder = 'flashcard-exporter/data/'
path_folder_full = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.pardir, path_files_folder)

# if filename not specified use arthistoryflash.json
if len(sys.argv) < 2:
    json_file = 'arthistoryflash.json'
elif len(sys.argv) == 2:
    json_file = sys.argv[1]
    if not json_file.endswith('.json'):
        print "Invalid filename."
        sys.exit()
else:
    print "Invalid arguments."
    sys.exit()

json_data = open(os.path.join(path_folder_full, json_file))
data = json.load(json_data)
json_data.close()

# initialize file order
global file_order
file_order = 0

# where to save the json files
path_fixtures = 'fixtures/'

# creates json file
def output_create(model_name, json_dump):
    global file_order
    file_order = file_order + 1
    outputfile = str(file_order) + '_initial_data_' + model_name + '.json'
    output= open(os.path.join(os.path.dirname(__file__),path_fixtures,outputfile),'w')
    output.write(json.dumps(json_dump, output, indent=4))
    print  'Successfully created '+str(outputfile)
    output.close()


# initial pks
initial_collection_pk, initial_deck_pk, initial_card_pk, initial_field_pk, initial_decks_cards_pk = get_initial_pks()

# collection
collection_pk = initial_collection_pk + 1
collection_name= data['collections'][0]['collection_name']
collection_description = "A course on "+ str(collection_name)
collection_json = [{
                    "model":"flash.Collection",
                    "pk":collection_pk,
                    "fields":
                        {
                         "title":collection_name,
                         "description":collection_description
                        }
                   }]
output_create('collection', collection_json)


# decks
initial_deck_pk = 1 + initial_deck_pk
# number of decks
decks = len(data['collections'][0]['decks'])
decks_json = []
for i in range(0, decks):
    deck_title = data['collections'][0]['decks'][i]['deck_name']
    decks_json.append({
                       "model":"flash.Deck",
                       "pk":i+initial_deck_pk,
                       "fields":
                           {
                            "title":deck_title,
                            "collection" : collection_pk
                           }
    })
output_create('decks', decks_json)


# map the card ids to natural numbers
card_mapping = dict()

# cards
initial_card_pk = 1 + initial_card_pk
cards = len(data['cards'])
cards_json = []
for k in range(0, cards):
    card_pk = k + initial_card_pk
    sort_order = k+1
    card_id = data['cards'][k]['_card_id']
    card_mapping[card_id] = card_pk
    cards_json.append({
                       "model":"flash.Card",
                       "pk":card_pk,
                       "fields":
                           {
                            "sort_order": sort_order,
                            "collection" : collection_pk
                           }
    })
output_create('cards', cards_json)


# fields and cards fields
fields_json = []
cards_fields_json = []
initial_pk = 1 + initial_field_pk
pk = 0
for k in range(0, cards):
    num_fields = len(data['cards'][k]['fields'])
    for j in range(0, num_fields):
        field = data['cards'][k]['fields'][j]
        label = field['label']
        field_type = field['type']
        show_label = field['show_label']
        display = field['display']

        value = field['value']
        card_id = data['cards'][k]['_card_id']
        card = card_mapping[card_id]
        sort_order = j+1
        field_pk = pk +initial_pk
        pk = pk+1
        fields_json.append({
                            "model":"flash.Field",
                            "pk":field_pk,
                            "fields":
                                {
                                 "sort_order": sort_order,
                                 "collection" : collection_pk,
                                 "label": label,
                                 "display": display,
                                 "show_label":show_label,
                                 "field_type":field_type
                                }
        })
        cards_fields_json.append({
                                "model":"flash.Cards_Fields",
                                "pk":field_pk,
                                "fields":
                                      {
                                       "sort_order": sort_order,
                                       "value": value,
                                       "field":field_pk,
                                       "card":card
                                      }
        })

output_create('fields', fields_json)
output_create('cards_fields', cards_fields_json)


# decks_cards

decks = len(data['collections'][0]['decks'])
decks_cards_json = []
pk = 0
initial_pk = 1 + initial_decks_cards_pk
for i in range(0, decks):
    deck_title = data['collections'][0]['decks'][i]['deck_name']
    deck_cards = data['collections'][0]['decks'][i]['deck_cards']
    num_deck_cards = len(deck_cards)
    for l in range(0, num_deck_cards):
        card_id = deck_cards[l]
        card = card_mapping[card_id]
        dc_pk = pk+initial_pk
        pk = pk+1
        deck_pk = i+initial_deck_pk
        card_sort = l+1
        decks_cards_json.append({
                                 "model":"flash.Decks_cards",
                                 "pk":dc_pk,
                                 "fields":
                                     {
                                      "deck":deck_pk,
                                      "card" :card,
                                      "sort_order":card_sort
                                     }
        })
output_create('decks_cards', decks_cards_json)