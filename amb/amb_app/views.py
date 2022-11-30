from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from .models import TimeSlot

# Index view
def index(request):
    context = { 'user': 'test' } 
    return render(request, 'index.html', context)
