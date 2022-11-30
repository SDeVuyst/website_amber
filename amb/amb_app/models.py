from django.db import models
from django import forms

class Appointment(models.Model):
    class Meta:
        unique_together = ('date', 'time_slot')

    TIMESLOT_LIST = (
        (0, '09:00 - 09:30'),
        (1, '10:00 - 10:30'),
        (2, '11:00 - 11:30'),
        (3, '12:00 - 12:30'),
        (4, '13:00 - 13:30'),
        (5, '14:00 - 14:30'),
        (6, '15:00 - 15:30'),
        (7, '16:00 - 16:30'),
        (8, '17:00 - 17:30'),
    )

    date = models.DateField()
    time_slot = models.IntegerField(choices=TIMESLOT_LIST)
    patient_first_name = models.CharField(max_length=30)
    patient_last_name  = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.patient_first_name} {self.patient_last_name} heeft een afspraak om {self.time} op {self.date}'

    @property
    def time(self):
        return self.TIMESLOT_LIST[self.time_slot][1]