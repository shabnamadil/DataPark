# Generated by Django 4.2.6 on 2023-11-24 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0011_alter_talentpool_job_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talentpool',
            name='job_type',
            field=models.CharField(choices=[(1, 'Open'), (2, 'Closed')], default='Open', max_length=200, verbose_name='İşin tipi'),
        ),
    ]
