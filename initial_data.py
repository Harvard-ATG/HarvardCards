import json
import os

json_file = 'arthistoryflash.json'
json_data = open(json_file)
data = json.load(json_data)
json_data.close()

# collection
collection_name= data['collections'][0]['collection_name']
collection_description = "A course on "+ str(collection_name)
collection_pk = 1
outputfile = 'initial_data_collection.json'
output = open(os.path.join(os.path.dirname(__file__),'harvardcards/apps/flash/fixtures/',outputfile),'w')
output.write(json.dumps([{"model":"flash.Collection", "pk":collection_pk, "fields":{"title":collection_name, "description":collection_description}}], output, indent=4))
output.close()

# decks
outputfile = 'initial_data_decks.json'
output = open(os.path.join(os.path.dirname(__file__),'harvardcards/apps/flash/fixtures/',outputfile),'w')

decks = len(data['collections'][0]['decks'])
decks_json = []
for i in range(0, decks):
    deck_title = data['collections'][0]['decks'][i]['deck_name']
    decks_json.append({"model":"flash.Deck", "pk":i+1, "fields":{"title":deck_title, "collection" : collection_pk}})

output.write(json.dumps(decks_json, output, indent=4))
output.close()

# cards
cards = len(data['cards'])
outputfile = 'initial_data_cards.json'
output = open(os.path.join(os.path.dirname(__file__),'harvardcards/apps/flash/fixtures/',outputfile),'w')

cards_json = []
for k in range(0, cards):
    sort_order = k+1
    card_id = data['cards'][k]['_card_id']
    cards_json.append({"model":"flash.Card", "pk":card_id, "fields":{"sort_order": sort_order,"collection" : collection_pk}})
output.write(json.dumps(cards_json, output, indent=4))
output.close()


# fields
cards = len(data['cards'])
outputfile = 'initial_data_fields.json'
output = open(os.path.join(os.path.dirname(__file__),'harvardcards/apps/flash/fixtures/',outputfile),'w')

fields_json = []
pk = 0
for k in range(0, cards):
    num_fields = len(data['cards'][k]['fields'])
    for j in range(0, num_fields):
        field = data['cards'][k]['fields'][j]
        label = field['label']
        field_type = field['type']
        show_label = field['show_label']
        display = field['display']
        sort_order = j+1
        pk = pk +1
        fields_json.append({"model":"flash.Field", "pk":pk, "fields":{"sort_order": sort_order,"collection" : collection_pk, "label": label, "display": display, "show_label":show_label, "field_type":field_type}})

output.write(json.dumps(fields_json, output, indent=4))
output.close()


# cards_fields

outputfile = 'initial_data_cards_fields.json'
output = open(os.path.join(os.path.dirname(__file__),'harvardcards/apps/flash/fixtures/',outputfile),'w')

cards_fields_json = []
pk = 0
for k in range(0, cards):
    num_fields = len(data['cards'][k]['fields'])
    for j in range(0, num_fields):
        field = data['cards'][k]['fields'][j]
        value = field['value']
        card_id = data['cards'][k]['_card_id']
        pk = pk+1
        cards_fields_json.append({"model":"flash.Cards_Fields", "pk":pk, "fields":{"sort_order": j+1, "value": value, "field":pk, "card":card_id}})

output.write(json.dumps(cards_fields_json, output, indent=4))
output.close()

# decks_cards
outputfile = 'initial_data_decks_cards.json'
output = open(os.path.join(os.path.dirname(__file__),'harvardcards/apps/flash/fixtures/',outputfile),'w')

decks = len(data['collections'][0]['decks'])
decks_cards_json = []
m = 0
for i in range(0, decks):
    deck_title = data['collections'][0]['decks'][i]['deck_name']
    deck_cards = data['collections'][0]['decks'][i]['deck_cards']
    num_deck_cards = len(deck_cards)
    for l in range(0, num_deck_cards):
        card_id = deck_cards[l]
        m = m+1
        decks_cards_json.append({"model":"flash.Decks_cards", "pk":m, "fields":{"deck":i+1, "card" :card_id, "sort_order":l+1}})

output.write(json.dumps(decks_cards_json, output, indent=4))
output.close()