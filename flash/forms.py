from models import Collection, Field, Deck, Decks_Cards, Card, Cards_Fields, Users_Collections
from django.forms.extras.widgets import SelectDateWidget
from . import services
from django import forms
from django.forms.util import ErrorList
from django.db import transaction
import logging
import datetime
import json
import tempfile
import os

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title', 'card_template', 'published'] #'private'
    def __init__(self, *args, **kwargs):
        card_template_query_set = None
        if 'query_set' in kwargs:
            card_template_query_set = kwargs.get('query_set', None)
            del kwargs['query_set']

        super(CollectionForm, self).__init__(*args, **kwargs)

        if card_template_query_set is not None:
            self.fields['card_template'].queryset = card_template_query_set

    def clean_deck_order(self):
        """
        Cleans and validates the JSON POSTed in the deck_order field.
        This field describes how decks should be sorted in the collection.
        Errors are manually added to the errorlist because this is a custom field.
        """
        field = 'deck_order'
        deck_data = []
        errstr = ''
        errors = ErrorList() 

        if field in self.data:
            deck_order = json.loads(self.data[field])
            if 'data' in deck_order:
                deck_data = deck_order['data']

        for d in deck_data:
            if ('deck_id' in d and 'sort_order' in d):
                try:
                    int(d['sort_order'])
                except ValueError:
                    errstr = "deck %s has invalid sort value: %s" % (d['deck_id'], d['sort_order'])
                    errors.append(errstr)
            else:
                errstr = "deck_id and sort_order required" 
                errors.append(errstr)
                break

        if errors:
            self._errors.setdefault(field, errors)
            raise forms.ValidationError("Deck order field has errors")

        self.cleaned_data['deck_order'] = deck_data

    def clean(self):
        """Overrides the form clean() so that it also cleans the hidden deck_order field."""
        self.clean_deck_order()
        return super(CollectionForm, self).clean()

    @transaction.commit_on_success
    def save_deck_order(self, deck_order):
        """Saves the new ordering."""
        for d in deck_order:
            deck = Deck.objects.get(pk=d['deck_id'])
            deck.sort_order = d['sort_order']
            deck.save()

    def save(self):
        """Overrides the form save() so that the deck ordering is saved as well."""
        if self.cleaned_data['deck_order']:
            self.save_deck_order(self.cleaned_data['deck_order'])
        return super(CollectionForm, self).save()

class CollectionShareForm(forms.Form):
    #role = forms.ChoiceField(choices=Users_Collections.ROLES, initial=Users_Collections.OBSERVER)
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
            if card_field.field_type in ('I','A') and field_name in self.data:
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
                path = services.handle_uploaded_media_file(self.files[field_name], self._get_field_type(field_name))
                field_list.append({"field_id":int(field_id), "value": path})

        if len(field_list) > 0:
            services.update_card_fields(self.card, field_list)
            
    def _get_field_type(self, find_field_name):
        for card_field in self.card_fields:
            field_name = self.field_prefix + str(card_field.id)
            if find_field_name == field_name:
                return card_field.field_type
        return None

    def _check_file_errors(self):
        for field_name in self.files:
            field_type = self._get_field_type(field_name)
            if "I" == field_type:
                is_valid_type, errstr = services.valid_image_file_type(self.files[field_name])
                if not is_valid_type:
                    self.errors[field_name] = "Invalid image file. Must be a valid image type (i.e jpg, png, gif, etc). Error: %s" % errstr
            elif "A" == field_type:
                with tempfile.NamedTemporaryFile(mode='r+', suffix='.mp3') as tf:
                    file_contents = self.files[field_name].read()
                    tf.write(file_contents)
                    tf.seek(0)
                    is_valid_type, errstr = services.valid_audio_file_type(tf.name)
                    errstr = ""
                    if not is_valid_type:
                        self.errors[field_name] = "Invalid audio file. Must be a valid mp3. Error: %s" % errstr


