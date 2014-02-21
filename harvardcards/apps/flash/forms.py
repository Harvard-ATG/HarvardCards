from models import Collection, Field, Deck
from django import forms
import logging

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title', 'description']
        
class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['field_type', 'display', 'label']

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['title']

class DeckImportForm(forms.Form):
    deck_title = forms.CharField(max_length=200, required=True)
    file = forms.FileField(required=True)
