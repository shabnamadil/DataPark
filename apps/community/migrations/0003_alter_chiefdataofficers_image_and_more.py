# Generated by Django 4.2.6 on 2023-11-24 06:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_remove_chiefdataofficers_full_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chiefdataofficers',
            name='image',
            field=models.FileField(unique=True, upload_to='CDOs/', verbose_name='Foto'),
        ),
        migrations.AlterField(
            model_name='chiefdataofficers',
            name='linkedin_url',
            field=models.URLField(unique=True, verbose_name='Linkedin profil linki'),
        ),
        migrations.AlterField(
            model_name='chiefdataofficers',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Adı'),
        ),
        migrations.AlterField(
            model_name='chiefdataofficers',
            name='position',
            field=models.CharField(max_length=200, verbose_name='Vəzifə'),
        ),
        migrations.AlterField(
            model_name='chiefdataofficers',
            name='surname',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Soyadı'),
        ),
        migrations.CreateModel(
            name='TalentPool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Əlavə edilmə tarixi')),
                ('published_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Nəşr tarixi')),
                ('status', models.CharField(choices=[('DF', 'Draft'), ('PB', 'Published')], default='DF', max_length=2)),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Adı')),
                ('surname', models.CharField(blank=True, max_length=50, null=True, verbose_name='Soyadı')),
                ('image', models.FileField(unique=True, upload_to='CDOs/', verbose_name='Foto')),
                ('position', models.CharField(max_length=200, verbose_name='Vəzifə')),
                ('company', models.CharField(max_length=200, verbose_name='Çalışdığı şirkətin adı')),
                ('linkedin_url', models.URLField(unique=True, verbose_name='Linkedin profil linki')),
                ('slug', models.SlugField(blank=True, help_text='Bu qismi boş buraxın. Avtomatik doldurulacaq.', max_length=500, null=True, verbose_name='Link adı')),
            ],
            options={
                'verbose_name': 'Talant',
                'verbose_name_plural': 'Talantlar',
                'ordering': ['-published_at'],
                'indexes': [models.Index(fields=['-published_at'], name='community_t_publish_2b187f_idx')],
            },
        ),
    ]
