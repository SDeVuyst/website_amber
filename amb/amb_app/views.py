from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from .forms import AppointmentForm


# Index view
def index(request):
    context = { 'user': 'test' } 
    return render(request, 'index.html', context)

# Appointment view
def appointment(request): 

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = AppointmentForm()
    return render(request, 'appointment.html', {'form': form})
