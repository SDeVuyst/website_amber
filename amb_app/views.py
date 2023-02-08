from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse, Http404
from django.core import mail
from django.conf import settings
from django.contrib import messages
from django.template.loader import get_template
from datetime import datetime

import re
import sys

from .models import TimeSlot, Day, Patient

# Index view
def index(request):
    return render(request, 'index.html')

def appointment(request):
    # Nieuwe afspraak ingediend
    if request.method == 'POST':
        # Check als data correct is
        # Timeslot zit in de gekozen dag
        
        try: 
            date = request.POST.get("date", "")
            date_cleaned = re.sub(r"([0-9]{2})\/([0-9]{2})\/([0-9]{4})", r"\3-\1-\2", date)
            timeslot_pk = request.POST.get("timeslot", "")
            first_name = request.POST.get("first_name", "")
            last_name = request.POST.get("last_name", "")
            email_patient = request.POST.get("email", "")
            eerste_gesprek = request.POST.get("eerste_gesprek", "") == 'eerste_gesprek'
            extra_info = request.POST.get("extra_info", "")
        except:
            raise Http404("Er ging iets mis... Probeer over een paar minuten opnieuw (wrong data from postget)")

        try:
            DayObject = Day.objects.get(date=date_cleaned)
            TimeslotObject = TimeSlot.objects.get(pk=timeslot_pk)
            PatientObject = Patient(first_name=first_name, last_name=last_name, email=email_patient)
        except:
            raise Http404("Er ging iets mis... Probeer over een paar minuten opnieuw (Objects not found)")

        # Timeslot zit in de gekozen dag
        if TimeslotObject.day == DayObject:
            if TimeslotObject.patient != None:
                raise Http404("Er ging iets mis... Probeer over een paar minuten opnieuw (Deze afspraak is al ingenomen)")

            try:
                # Save patient
                PatientObject.save()        

                # Add patient to timeslot
                TimeslotObject.patient=PatientObject
                TimeslotObject.extra_info=extra_info
                TimeslotObject.eerste_afspraak=eerste_gesprek
                TimeslotObject.save()
            except:
                raise Http404("Er ging iets mis... Probeer over een paar minuten opnieuw (Patient & timeslot not saved)")

            messages.success(request, 'Bedankt voor je afspraak!')

            send_mail(email_patient, first_name, last_name, DayObject.date, TimeslotObject.start, TimeslotObject.end)
            
        else:
            raise Http404("Er ging iets mis... Probeer over een paar minuten opnieuw (Timeslot is not in day)")

    # REQUEST METHOD == GET
    # User wil nieuwe afspraak maken
    # all days where there is still an open timeslot
    daysSet = set()
    try:
        for slot in TimeSlot.objects.filter(available=True, day__date__gt=datetime.today()):
            daysSet.add(slot.day)
    except:
        raise Http404("Er ging iets mis... Probeer over een paar minuten opnieuw (could not fetch timeslots from appointment)")

    return render(request, 'appointment.html', {
        'daysSet': daysSet
    })


# Geeft de available timeslots terug voor een gegeven dag
def getTimeSlots(request, date):
    try:
        DayObject = Day.objects.get(date=date)
        queryset = TimeSlot.objects.filter(day=DayObject, available=True)

        response = HttpResponse() 
        response['Content-Type'] = "text/javascript" 
        response.write(serialize("json", queryset)) 
    except:
        raise Http404("Er ging iets mis... Probeer over een paar minuten opnieuw (could not fetch timeslots for day)")

    return response  


def send_mail(send_to, first_name, last_name, date, start, end):
    try:
        message = get_template("mail.html").render({
            'first_name': first_name,
            'last_name': last_name,
            'date': date,
            'start': start,
            'end': end
        })
    
        with mail.get_connection() as connection:
            EmailObject = mail.EmailMessage(
                'Bedankt voor je afspraak!',
                message,
                settings.EMAIL_HOST_USER, 
                [send_to],
                connection=connection,
            )
            
            EmailObject.content_subtype = "html"
            EmailObject.send()
            
    except Exception as e:
        print(e, file=sys.stderr)
        return