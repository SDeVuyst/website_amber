from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from .models import TimeSlot, Day

# Index view
def index(request):
    context = { 'user': 'test' } 
    return render(request, 'index.html', context)

def appointment(request):
    
    if request.method == 'POST':
            # Your code for POST
            # make sure to put a "return redirect" statement here
        pass

    # all days where there is still an open timeslot
    daysSet = set()
    for slot in TimeSlot.objects.filter(available=True):
        daysSet.add(slot.day)

    return render(request, 'appointment.html', {
        'daysSet': daysSet
    })