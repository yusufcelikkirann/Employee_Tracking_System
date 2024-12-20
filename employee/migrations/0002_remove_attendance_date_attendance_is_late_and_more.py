# Generated by Django 5.0.2 on 2024-11-22 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='date',
        ),
        migrations.AddField(
            model_name='attendance',
            name='is_late',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='attendance',
            name='late_minutes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='clock_in_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
