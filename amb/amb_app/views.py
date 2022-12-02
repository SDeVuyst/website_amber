from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers import serialize
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

def getTimeSlots(request, date):
    print(date)
    DayObject = Day.objects.get(date=date)
    queryset = TimeSlot.objects.filter(day=DayObject, available=True)

    response = HttpResponse() 
    response['Content-Type'] = "text/javascript" 
    response.write(serialize("json", queryset)) 
    return response  