# Generated by Django 4.1.4 on 2022-12-23 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amb_app', '0020_timeslot_betaald_timeslot_eerste_afspraak_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='extra_info',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
