from django.urls import re_path, path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('appointment', views.appointment, name='appointment'),
    re_path(r'^timeslots/(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})$', views.getTimeSlots, name='getTimeSlots')
    # path('timeslots', views.getTimeSlots, name='timeslots')
]

