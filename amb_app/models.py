from django.db import models
from django import forms
from django.utils.html import format_html
from datetime import datetime


class Patient(models.Model):

    first_name = models.CharField(max_length=30)
    last_name  = models.CharField(max_length=30)
    email = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Day(models.Model):
    date = models.DateField(unique=True)

    def __str__(self):
        return str(self.date.strftime("%d/%m/%Y"))

    # Maak default timeslots voor elke nieuwe dag
    def save(self, *args, **kwargs):

        super(Day, self).save(*args, **kwargs)

        TIMETABLE = [
            ('09:00:00', '10:00:00'),
            ('10:00:00', '11:00:00'),
            ('11:00:00', '12:00:00'),
            ('13:00:00', '14:00:00'),
            ('14:00:00', '15:00:00'),
            ('15:00:00', '16:00:00'),
            ('16:00:00', '17:00:00'),
        ]

        for times in TIMETABLE:
            slot = TimeSlot(start=times[0], end=times[1], available=True, patient=None, day=self, eerste_afspraak=False)
            slot.save()
    
    

class TimeSlot(models.Model):

    day = models.ForeignKey(Day, on_delete=models.CASCADE, verbose_name='Day')
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)
    available = models.BooleanField(default=True)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, verbose_name='Patient', null=True, blank=True) 
    eerste_afspraak = models.BooleanField(default=False)
    extra_info = models.TextField(null=True, blank=True, max_length=500)
    betaald = models.BooleanField(default=False)

    class Meta:
        ordering = ['day', 'start', 'end']

        constraints = [
            models.UniqueConstraint(
                fields=['day', 'start', 'end'],
                name='One timeslot with same start and end value per day'
            )
        ]


    def save(self, *args, **kwargs):
        # iemand heeft afspraak, deze timeslot is niet meer beschikbaar
        if (self.patient):
            self.available = False

        super(TimeSlot, self).save(*args, **kwargs)


    def __str__(self):

        if self.available:
            return f'{self.day}: {self.start.strftime("%H:%M")} - {self.end.strftime("%H:%M")} is beschikbaar'
        else:
            if self.patient:
                return f'{self.day}: {self.patient} heeft een afspraak om {self.start.strftime("%H:%M")}'
            else:
                return f'{self.day}: {self.start.strftime("%H:%M")} - {self.end.strftime("%H:%M")} is gesloten'