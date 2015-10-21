from django.http import HttpResponse
from django.shortcuts import render, redirect

def splash(request):
    return render(request, 'splash.html')
    
def main(request):
    return render(request, 'main.html')

def help(request):
    return render(request, 'help.html')
