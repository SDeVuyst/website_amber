from django.contrib import admin
from .models import Patient, TimeSlot, Day
from django.utils.translation import ngettext
from django.contrib import messages


class DayAdmin(admin.ModelAdmin):
    ordering=['date']
    actions = ['closeDay', 'openDay']

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



class TimeSlotAdmin(admin.ModelAdmin):
    ordering=['day', 'start']
    actions = ['closeTimeSlot', 'openTimeSlot']

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



class PatientAdmin(admin.ModelAdmin):
    ordering=['first_name', 'last_name']
    actions = []


admin.site.register(Day, DayAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(TimeSlot, TimeSlotAdmin)

