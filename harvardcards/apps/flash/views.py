from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf

from models import Collection
from forms import CollectionForm

def index(request):
    #return HttpResponse("Hello Werld. This is the HarvardCards Index.")
    return render(request, 'index.html')
    
def splash(request):
    return render(request, 'splash.html')
    
def main(request):
    return render(request, 'main.html')
    
def create(request):
    # this is only POSTed when creating -- editing will be done on the fly
    if request.method == 'POST':
#        for key in request.POST:
#            value = request.POST[key]
#            message += ' '+key+'=>'+value
        f = CollectionForm(request.POST)
        collection = f.save()
        
        # get collection id
        
        # use collection_id to create appropriate fields
        
        
        return redirect(index)
    else:
        return render(request, 'collections/create.html')
    
