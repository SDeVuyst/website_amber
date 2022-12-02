from django.contrib import admin
from .models import Patient, TimeSlot, Day
from django.utils.translation import ngettext
from django.utils.html import mark_safe, format_html
from django.contrib import messages
from django import forms


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    ordering = ['date']
    actions = ['closeDay', 'openDay']
    # TODO fix date search in different format
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
            timeslots = TimeSlot.objects.filter(day=Day)
            timeslots.update(available=False)
            timeslotcount += timeslots.count()

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
            timeslots = TimeSlot.objects.filter(day=Day)
            timeslots.update(available=True)
            timeslotcount += timeslots.count()

        # Send message if succesful
        daycount = queryset.count()
        self.message_user(request, ngettext(
                    f'{daycount} day ({timeslotcount} timeslots) was successfully opened.',
                    f'{daycount} days ({timeslotcount} timeslots) were successfully opened.',
                    daycount
                ), messages.SUCCESS)

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    ordering=['day', 'start']
    actions = ['closeTimeSlot', 'openTimeSlot']
    # TODO fix date search in different format
    search_fields = ['start', 'end', 'day__date', 'patient__first_name', 'patient__last_name']
    date_hierarchy = 'day__date'

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
    actions = []

    #TODO nu is bij naam, maar moet met ojject zelf zijn
    def view_timeslots(self, obj):
        url = (f'/admin/amb_app/timeslot/?q={obj.first_name}+{obj.last_name}')
        return format_html('<a href="{}">See Timeslots</a>', url)
    view_timeslots.short_description = "Time Slots"

    def full_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)
    full_name.short_description = 'Naam'