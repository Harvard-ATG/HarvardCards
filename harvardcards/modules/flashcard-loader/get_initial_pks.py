#
# The function returns the current maximum values of primary keys which are needed to
# initialize primary keys for the new collections, decks, etc. Otherwise, the previous
# data will be overwritten.
# It returns the maximum pks in this order: Collection, Deck, Card, Field, Decks_Cards
# Usage:
#   initial_collection_pk, initial_deck_pk, initial_card_pk, initial_field_pk, initial_decks_cards_pk = get_initial_pks()

import os

script_path = os.path.dirname(os.path.abspath(__file__))

def get_initial_pks():
    import os, json

    # dumps the current django data
    filename = 'all_data.json'
    os.chdir(os.path.join(os.pardir, os.pardir, os.pardir))
    os.system("python manage.py dumpdata --indent=4 flash>%s" %filename)

    json_data = open(filename)
    data = json.load(json_data)
    json_data.close()
    # comment out to keep the dumpdata file
    os.remove(filename)
    os.chdir(script_path)

    # function returns the maximum pk of given model's instances
    def get_max_pk(model_name):
        model_name = 'flash.'+ model_name
        model_instances = filter(lambda x: x['model']==model_name, data)
        if len(model_instances) != 0:
            model_max_pk = max(model_instances, key = lambda x: x['pk'])
            return model_max_pk['pk']
        else:
            return 0

    max_collection_pk = get_max_pk('collection')
    max_deck_pk = get_max_pk('deck')
    max_card_pk = get_max_pk('card')
    max_field_pk = get_max_pk('field')
    #max_cards_fields_pk = get_max_pk('cards_fields')
    max_decks_cards_pk =  get_max_pk('decks_cards')
    return max_collection_pk, max_deck_pk, max_card_pk, max_field_pk, max_decks_cards_pk





