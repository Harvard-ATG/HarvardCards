from django.forms import ModelForm
from django.forms import MultipleChoiceField
from models import Collection, Field
from django import forms
import logging

class CollectionForm(ModelForm):
    class Meta:
        model = Collection
        fields = ['title', 'description']
        
class FieldForm(ModelForm):
    class Meta:
        model = Field
        fields = ['field_type', 'sort_order', 'display']
