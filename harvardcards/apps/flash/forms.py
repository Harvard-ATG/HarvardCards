from django.forms import ModelForm
from django.forms import MultipleChoiceField
from models import Collection, Field
from django import forms
import logging

class CollectionForm(ModelForm):
    # this is wrong, putting this here implies that I want the field_data to not validate if the fields dont already exist
    #field_data = ModelMultipleChoiceField(queryset=Field.objects.all())    
    # what I want is a list, one that will run through and validate all incoming objects in the list as valid fields
    # this may be a formset field?
    #field_data = MultipleChoiceField()
    
    class Meta:
        model = Collection
        fields = ['title', 'description']
        
class FieldForm(ModelForm):
    class Meta:
        model = Field
        fields = ['field_type', 'sort_order', 'display']
