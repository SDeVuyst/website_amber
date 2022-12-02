from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers import serialize
from django.http import HttpResponse
from django.template import loader

import re

from .models import TimeSlot, Day, Patient

# Index view
def index(request):
    context = { 'user': 'test' } 
    return render(request, 'index.html', context)

def appointment(request):
    # Nieuwe afspraak ingediend
    if request.method == 'POST':
        # Check als data correct is
        # Timeslot zit in de gekozen dag
        
        # make sure to put a "return redirect" statement here
        date = request.POST.get("date", "")
        date_cleaned = re.sub(r"([0-9]{2})\/([0-9]{2})\/([0-9]{4})", r"\3-\1-\2", date)
        timeslot_pk = request.POST.get("timeslot", "")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")

        DayObject = Day.objects.get(date=date_cleaned)
        TimeslotObject = TimeSlot.objects.get(pk=timeslot_pk)
        PatientObject = Patient(first_name=first_name, last_name=last_name)

        # Timeslot zit in de gekozen dag
        if TimeslotObject.day == DayObject:

            # Save patient
            PatientObject.save()        
            # Add patient to timeslot
            TimeslotObject.patient=PatientObject
            TimeslotObject.save()
        
        print("Succes!")
        return redirect('index')

    # User wil nieuwe afspraak maken
    # all days where there is still an open timeslot
    daysSet = set()
    for slot in TimeSlot.objects.filter(available=True):
        daysSet.add(slot.day)

    return render(request, 'appointment.html', {
        'daysSet': daysSet
    })

# Geeft de available timeslots terug voor een gegeven dag
def getTimeSlots(request, date):
    DayObject = Day.objects.get(date=date)
    queryset = TimeSlot.objects.filter(day=DayObject, available=True)

    response = HttpResponse() 
    response['Content-Type'] = "text/javascript" 
    response.write(serialize("json", queryset)) 
    return response  