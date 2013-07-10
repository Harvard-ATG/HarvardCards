from django.forms import ModelForm
from models import Collection

class CollectionForm(ModelForm):
    class Meta:
        model = Collection
        fields = ['title', 'description']
