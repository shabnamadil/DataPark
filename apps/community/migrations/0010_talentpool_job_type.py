# Generated by Django 4.2.6 on 2023-11-24 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0009_talentpool_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='talentpool',
            name='job_type',
            field=models.CharField(choices=[(1, 'Open'), (2, 'Closed')], default=1, max_length=200, verbose_name='işin tipi'),
        ),
    ]
