from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Index view
def index(request):
    context = { 'user': 'test' } 
    return render(request, 'index.html', context)