# Generated by Django 4.1.3 on 2022-11-30 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amb_app', '0010_alter_timeslot_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='amb_app.patient', verbose_name='Patient'),
        ),
    ]
