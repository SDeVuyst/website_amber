from django.contrib import admin
from .models import Patient, TimeSlot, Day
from django.utils.translation import ngettext
from django.utils.html import format_html
from django.contrib import messages
from django.forms import TextInput, Textarea
from django.db import models
from django.http import Http404

@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    ordering = ['date']
    actions = ['closeDay', 'openDay']
    search_fields = ('date', )
    #2022-12-01 --> how to search
    list_display = ('date', 'view_timeslots')
    date_hierarchy = 'date'
    
    def view_timeslots(self, obj):
        url = (f'/admin/amb_app/timeslot/?q={obj.date}')
        return format_html('<a href="{}">See Timeslots</a>', url)
    view_timeslots.short_description = "Time Slots"


    @admin.action(description='Sluit elk tijdslot van de geselecteerde dagen')
    def closeDay(self, request, queryset):

        timeslotcount = 0   
        for Day in queryset:
            try:
                timeslots = TimeSlot.objects.filter(day=Day)
                timeslots.update(available=False)
                timeslotcount += timeslots.count()
            except:
                raise Http404("Er ging iets mis... Probeer over een paar minuten opnieuw (could not update timeslots to unavailable)")

        # Send message if succesful
        count = queryset.count()
        self.message_user(request, ngettext(
                    f'{count} day ({timeslotcount} timeslots) was successfully closed.',
                    f'{count} days ({timeslotcount} timeslots) were successfully closed.',
                    count
                ), messages.SUCCESS)


    @admin.action(description='Open elk tijdslot van de geselecteerde dagen')
    def openDay(self, request, queryset):

        timeslotcount = 0
        for Day in queryset:
            try:
                timeslots = TimeSlot.objects.filter(day=Day, patient=None)
                timeslots.update(available=True)
                timeslotcount += timeslots.count()
            except:
                raise Http404("Er ging iets mis... Probeer over een paar minuten opnieuw (could not update timeslots to available)")

        # Send message if succesful
        daycount = queryset.count()
        self.message_user(request, ngettext(
                    f'{daycount} day ({timeslotcount} timeslots) was successfully opened.',
                    f'{daycount} days ({timeslotcount} timeslots) were successfully opened.',
                    daycount
                ), messages.SUCCESS)


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }
    list_filter = ('betaald', 'eerste_afspraak', 'available')
    ordering=['day', 'start']
    actions = ['closeTimeSlot', 'openTimeSlot']
    search_fields = ['start', 'end', 'day__date', 'patient__first_name', 'patient__last_name']
    date_hierarchy = 'day__date'

    def isAvailable(self, obj):
        return obj.available
    isAvailable.boolean = True
    isAvailable.short_description = 'available'


    @admin.action(description='Sluit elke geselecteerde tijdslot')
    def closeTimeSlot(self, request, queryset):
        queryset.update(available=False)

        count=queryset.count()
        self.message_user(request, ngettext(
                    f'{count} day  was successfully closed.',
                    f'{count} days were successfully closed.',
                    count
                ), messages.SUCCESS)
        

    @admin.action(description='Open elke geselecteerde tijdslot')
    def openTimeSlot(self, request, queryset):
        queryset.filter(patient=None).update(available=True)

        count=queryset.filter(patient=None).count()
        self.message_user(request, ngettext(
                    f'{count} day  was successfully opened.',
                    f'{count} days were successfully opened.',
                    count
                ), messages.SUCCESS)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    ordering=['first_name', 'last_name']
    list_display = ('full_name', 'view_timeslots')
    search_fields = ['first_name', 'last_name']
    actions = []

    def view_timeslots(self, obj):
        url = (f'/admin/amb_app/timeslot/?q={obj.first_name}+{obj.last_name}')
        return format_html('<a href="{}">See Timeslots</a>', url)
    view_timeslots.short_description = "Time Slots"

    def full_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)
    full_name.short_description = 'Naam'