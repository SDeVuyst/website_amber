# Generated by Django 4.1.3 on 2022-11-30 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amb_app', '0005_alter_timeslot_appointment_alter_timeslot_end_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='date',
        ),
    ]
