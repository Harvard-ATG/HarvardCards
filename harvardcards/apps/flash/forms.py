from models import Collection, Field, Deck, Decks_Cards, Card, Cards_Fields, Users_Collections
from django.forms.extras.widgets import SelectDateWidget
from . import services
from django import forms
import logging, datetime

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title', 'card_template', 'private']

class CollectionShareForm(forms.Form):
    role = forms.ChoiceField(choices=Users_Collections.ROLES, initial=Users_Collections.OBSERVER)
    expired_in = forms.DateField(widget=SelectDateWidget(), initial=datetime.datetime.now()+datetime.timedelta(days=365))

class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['field_type', 'display', 'label']

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['title']

class DeckImportForm(forms.Form):
    file = forms.FileField(required=False)

class CardEditForm(forms.Form):
    card_color = forms.ChoiceField(choices=Card.COLOR_CHOICES, initial=Card.DEFAULT_COLOR, required=True)
    card = None
    deck = None
    card_fields = []
    field_prefix = 'field_'

    def __init__(self, *args, **kwargs):
        """Initializes the form."""

        self.card_fields = kwargs.pop('card_fields', []) # custom: defines fields in this form

        super(CardEditForm, self).__init__(*args, **kwargs)

        # add the fields to the form
        for card_field in self.card_fields:
            field_name = self.field_prefix + str(card_field.id)
            self.fields[field_name] = forms.CharField(required=False)
            if card_field.field_type == 'I' and field_name in self.data:
                del self.data[field_name] # REMOVE from data because handled separately from normal fields

        # initialize model objects
        self.deck = Deck.objects.get(id=self.data['deck_id'])
        if self.data['card_id']:
            self.card = Card.objects.get(id=self.data['card_id'])
        else:
            self.card = services.create_card_in_deck(self.deck)

        #print "data", self.data, "fields", self.fields, "files", self.files

    def is_valid(self):
        self._check_file_errors()
        return super(CardEditForm, self).is_valid()

    def save(self):
        """Saves the card with all of its fields and attributes."""
        self._save_card_fields()
        self._save_card_files()
        self._save_card_data()

    def get_card(self):
        """Returns Card instance."""
        return self.card

    def get_deck(self):
        """Returns Deck instance."""
        return self.deck

    def _save_card_fields(self):
        field_list = []
        for field_name, field_value in self.data.items():
            is_field = field_name.startswith(self.field_prefix)
            if not is_field:
                continue
            field_id = field_name.replace(self.field_prefix, '')
            if not field_id.isdigit():
                continue
            field_list.append({"field_id": int(field_id), "value": field_value})

        if len(field_list) > 0:
            services.update_card_fields(self.card, field_list)

    def _save_card_data(self):
        self.card.color = self.cleaned_data['card_color']
        self.card.save()

    def _save_card_files(self):
        field_list = []
        for field_name, field_value in self.files.items():
            is_field = field_name.startswith(self.field_prefix)
            if not is_field:
                continue
            field_id = field_name.replace(self.field_prefix, '')
            if not field_id.isdigit():
                continue
            if self.files[field_name].size > 0:
                path = services.handle_uploaded_img_file(self.files[field_name], self.deck.id, self.deck.collection.id)
                field_list.append({"field_id":int(field_id), "value": path})

        if len(field_list) > 0:
            services.update_card_fields(self.card, field_list)

    def _check_file_errors(self):
        for f in self.files:
            is_valid_type = services.valid_uploaded_file(self.files[f], 'I')
            if not is_valid_type:
                self.errors[f] = "File image type is not supported. Must be JPG or PNG."
