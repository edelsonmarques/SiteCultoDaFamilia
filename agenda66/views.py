import os
from django.shortcuts import render
from django.http import HttpResponse
from enums.pages_names import pages_names

def home(request):
    
    return render(request, 'home.html', {'pages_names': pages_names})
