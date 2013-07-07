from django.shortcuts import render

def index(request):
    #return HttpResponse("Hello Werld. This is the Harmony Index.")
    return render(request, 'index.html')
    
def splash(request):
    return render(request, 'splash.html')
    
def main(request):
    return render(request, 'main.html')
    
def create(request):
    return render(request, 'collections/create.html')