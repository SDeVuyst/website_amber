# Generated by Django 4.1.3 on 2022-12-01 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amb_app', '0017_alter_timeslot_options_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='timeslot',
            name='One timeslot with same start and end value per day',
        ),
    ]
