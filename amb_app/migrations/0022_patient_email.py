# Generated by Django 4.1.4 on 2022-12-24 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amb_app', '0021_alter_timeslot_extra_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='email',
            field=models.CharField(default=2, max_length=50),
            preserve_default=False,
        ),
    ]
