from datetime import date

from django import forms

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    

    class Meta:
        model = Appointment
        fields = ('date', 'time_slot', 'patient_first_name', 'patient_last_name')
        widgets = {
            'date': forms.DateTimeInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control'
                })
        }

    def clean_date(self):
        day = self.cleaned_data['date']

        if day <= date.today():
            raise forms.ValidationError('Date should be upcoming (tomorrow or later)', code='invalid')
        if day.isoweekday() in (0, 6):
            raise forms.ValidationError('Date should be a workday', code='invalid')

        return day