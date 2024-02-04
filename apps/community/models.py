from django.db import models
from django.utils.text import slugify
from django.utils import timezone

from .utils.manager import (
    PublishedCDOManager,
    PublishedTalentPoolManager,
    ActiveTalentLevelManager,
    ActiveTalentPositionManager,
    ActiveTalentSectorManager
    )


class Base(models.Model):

    class Status(models.TextChoices):
            DRAFT = 'DF', 'Draft'
            PUBLİSHED = 'PB', 'Published'
    
    created_at = models.DateTimeField('Əlavə edilmə tarixi', auto_now_add=True)
    published_at = models.DateTimeField('Nəşr tarixi', default=timezone.now)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    active = models.BooleanField(default=True)

    class Meta:
        abstract=True


class ChiefDataOfficers(Base):
    name = models.CharField('Adı', max_length=50, null=True, blank=True)
    surname = models.CharField('Soyadı', max_length=50, null=True, blank=True)
    image = models.FileField('Foto', unique=True, upload_to='CDOs/')
    position = models.CharField('Vəzifə', max_length=200)
    company = models.CharField('Çalışdığı şirkətin adı', max_length=200)
    linkedin_url = models.URLField('Linkedin profil linki', unique=True)
    slug=models.SlugField(
                        ("Link adı"),
                        null=True, blank=True,
                        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
                        max_length=500
                        )   
    objects = models.Manager()
    published = PublishedCDOManager()

    class Meta:
        verbose_name = 'Şirkət rəhbəri'
        verbose_name_plural = 'Şirkət rəhbərləri'
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at'])
        ]
    
    @property
    def full_name(self):
         return f'{self.name} {self.surname}' 

    def __str__(self) -> str:
        return f'{self.name} {self.surname}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name+self.surname)
        super().save(*args, **kwargs)


class TalentPool(Base):
    JOB_TYPE_CHOICES = (
        (1, "Open"),
        (2, "Closed")
    )

    name = models.CharField('Adı', max_length=50)
    surname = models.CharField('Soyadı', max_length=50)
    image = models.FileField('Foto', unique=True, upload_to='CDOs/')
    company = models.CharField('Çalışdığı şirkətin adı', max_length=200)
    work_location = models.CharField('Çalışdığı şəhər', max_length=250, null=True, blank=True)
    linkedin_url = models.URLField('Linkedin profil linki', unique=True)
    sector = models.ForeignKey('community.TalentSector', verbose_name='Sektor', on_delete=models.CASCADE, related_name='talent_pool', null=True, blank=True)
    position = models.ForeignKey('community.TalentPosition', verbose_name='Vəzifə', on_delete=models.CASCADE, related_name='talent_pool', null=True, blank=True)
    level = models.ForeignKey('community.TalentLevel', verbose_name='gördüyü işin səviyyəsi', on_delete=models.CASCADE, related_name='talent_pool', null=True, blank=True)
    job_type = models.IntegerField('İşin tipi', choices=JOB_TYPE_CHOICES, default=1)
    objects = models.Manager()
    slug=models.SlugField(
                        ("Link adı"),
                        null=True, blank=True,
                        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
                        max_length=500
                        )   
    published = PublishedTalentPoolManager()

    class Meta:
        verbose_name = 'Talant'
        verbose_name_plural = 'Talantlar'
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at'])
        ]
    
    @property
    def full_name(self):
         return f'{self.name} {self.surname}' 

    def __str__(self) -> str:
        return f'{self.name} {self.surname}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.full_name)
        super().save(*args, **kwargs)


class TalentSector(Base):
    sector_name = models.CharField('Sector adı', max_length=50)
    slug=models.SlugField(
                        ("Link adı"),
                        null=True, blank=True,
                        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
                        max_length=500
                        )   
    activated = ActiveTalentSectorManager()

    class Meta:
        verbose_name = 'Talant sektoru'
        verbose_name_plural = 'Talant sektorları'
        ordering = ['sector_name']

    def __str__(self) -> str:
        return self.sector_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.sector_name)
        super().save(*args, **kwargs)


class TalentPosition(Base):
    position_name = models.CharField('Vəzifə', max_length=50)
    slug=models.SlugField(
                        ("Link adı"),
                        null=True, blank=True,
                        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
                        max_length=500
                        )   
    activated = ActiveTalentPositionManager()

    class Meta:
        verbose_name = 'Talantın vəzifəsi'
        verbose_name_plural = 'Talant vəzifələri'
        ordering = ['position_name']

    def __str__(self) -> str:
        return self.position_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.position_name)
        super().save(*args, **kwargs)


class TalentLevel(Base):
    level_name = models.CharField('Səviyyə', max_length=50)
    slug=models.SlugField(
                        ("Link adı"),
                        null=True, blank=True,
                        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
                        max_length=500
                        )   
    activated = ActiveTalentLevelManager()

    class Meta:
        verbose_name = 'Talant işinin səviyyəsi'
        verbose_name_plural = 'Talant işinin səviyyələri'
        ordering = ['level_name']

    def __str__(self) -> str:
        return self.level_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.level_name)
        super().save(*args, **kwargs)




