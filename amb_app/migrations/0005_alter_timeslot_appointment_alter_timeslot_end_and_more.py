# Generated by Django 4.1.3 on 2022-11-30 18:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('amb_app', '0004_remove_day_timeslots_timeslot_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='appointment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='amb_app.appointment', verbose_name='Appointment'),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='end',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='start',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
