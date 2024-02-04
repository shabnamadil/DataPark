from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from apps.users.models import User
from django.urls import reverse

from .utils.manager import (
    PublishedEventManager,
    PublishedEventCommentManager,
    PublishedNewsCommentManager,
    PublishedNewsManager
    )


class Base(models.Model):

    class Status(models.TextChoices):
            DRAFT = 'DF', 'Draft'
            PUBLİSHED = 'PB', 'Published'
    
    created_at = models.DateTimeField('Əlavə edilmə tarixi', auto_now_add=True)
    updated_at = models.DateTimeField('Yenilənmə tarixi', auto_now=True)
    published_at = models.DateTimeField('Nəşr tarixi', default=timezone.now)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    class Meta:
        abstract=True

    @property
    def published_date(self):
        return self.published_at.strftime('%d.%m.%Y')


class IPs(models.Model):
    view_ip = models.GenericIPAddressField('IP ünvanı', editable=False)

    class Meta:
        verbose_name = ('IP ünvanı')
        verbose_name_plural = ('IP ünvanları')

    def __str__(self) -> str:
        return self.view_ip
    

class News(Base):
    news_title = models.CharField(('Xəbər başlığı'), max_length=150, unique=True)
    news_content = RichTextUploadingField('Xəbər mətni', null=True, blank=True)
    news_image = models.ImageField('Xəbər fotosu', upload_to='news/')
    slug=models.SlugField(
                        ("Link adı"),
                        null=True, blank=True,
                        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
                        max_length=500    
                    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news', null=True, blank=True)
    viewed_ips = models.ManyToManyField(IPs, related_name="news", verbose_name='Xəbərlərin görüntüləndiyi IP ünvanları', editable=False)
    objects = models.Manager()
    published = PublishedNewsManager()

    class Meta:
        verbose_name = ('Xəbər')
        verbose_name_plural = ('Xəbərlər')
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at'])
        ]

    @property
    def news_count(self):
        return len(News.published.all())
    
    @property
    def view_count(self):
        return self.viewed_ips.count() if self.viewed_ips else 0
    
    def get_absolute_url(self):
        return reverse('news-detail', args=[self.id])

    def __str__(self) -> str:
        return self.news_title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.news_title)
        super().save(*args, **kwargs)


class News_comment(Base):
    comment_text = models.TextField('Xəbər rəyi', max_length=250)
    comment_slug = models.SlugField(
                            ("Link adı"),
                            null=True, blank=True,
                            help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
                            max_length=500)  
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='news_comments')
    active = models.BooleanField(default=True)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_comments', null=True, blank=True)
    liked = models.ManyToManyField(User, related_name='news_liked_comments', verbose_name='Bəyənənlər', editable=False)
    disliked = models.ManyToManyField(User, related_name='news_disliked_comments', verbose_name='Bəyənməyənlər', editable=False)
    objects = models.Manager()
    published = PublishedNewsCommentManager()

    class Meta:
          verbose_name = ('Xəbər rəyi')
          verbose_name_plural = ('Xəbər rəyləri')
          ordering = ['-published_at']
          indexes = [
            models.Index(fields=['-published_at'])
        ]

    @property
    def liked_count(self):
        return self.liked.count() if self.liked else 0
    
    @property
    def disliked_count(self):
        return self.disliked.count() if self.disliked else 0

    def __str__(self) -> str:
        return self.comment_text[:50]  + '...' if len(self.comment_text) > 50 else self.comment_text
    
    def save(self, *args, **kwargs):
        if not self.comment_slug:
            self.comment_slug=slugify(self.comment_text)
        if self.active:
            self.status = self.Status.PUBLİSHED
        else:
            self.status = self.Status.DRAFT
        super().save(*args, **kwargs)


class Event(Base):
    event_title = models.CharField('Hadisə başlığı', max_length=250, unique=True)
    event_content = RichTextUploadingField('Hadisənin kontenti')
    event_photo = models.ImageField(upload_to='events/', unique=True)
    event_location = models.CharField('Hadisənin məkanı', max_length=150)
    event_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events', null=True, blank=True)
    event_slug = models.SlugField(
                            ("Link adı"),
                            null=True, blank=True,
                            help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
                            max_length=500) 
    viewed_ips = models.ManyToManyField(IPs, related_name="events", verbose_name='Hadisələrin görüntüləndiyi IP ünvanları', editable=False)
    objects = models.Manager()
    published = PublishedEventManager()

    class Meta:
          verbose_name = ('Hadisə')
          verbose_name_plural = ('Hadisələr')
          ordering = ['-published_at']
          indexes = [
            models.Index(fields=['-published_at'])
        ]
          
    def __str__(self):
        return self.event_title
    
    @property
    def event_count(self):
        return len(Event.published.all())
    
    @property
    def view_count(self):
        return self.viewed_ips.count() if self.viewed_ips else 0
    
    # def get_absolute_url(self):
    #     return reverse('event_detail', args=[self.event_slug])
    
    def save(self, *args, **kwargs):
        if not self.event_slug:
            self.event_slug=slugify(self.event_title)
        super().save(*args, **kwargs)


class Event_comment(Base):
    comment_text = models.TextField('Hadisəyə yazılmış rəy', max_length=250)
    comment_slug = models.SlugField(
                            ("Link adı"),
                            null=True, blank=True,
                            help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
                            max_length=500)  
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_comments')
    active = models.BooleanField(default=True)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_comments', null=True, blank=True)
    liked = models.ManyToManyField(User, related_name='event_liked_comments', verbose_name='Bəyənənlər', editable=False)
    disliked = models.ManyToManyField(User, related_name='event_disliked_comments', verbose_name='Bəyənməyənlər', editable=False)
    objects = models.Manager()
    published = PublishedEventCommentManager()

    class Meta:
          verbose_name = ('Hadisə rəyi')
          verbose_name_plural = ('Hadisə rəyləri')
          ordering = ['-published_at']
          indexes = [
            models.Index(fields=['-published_at'])
        ]

    def __str__(self) -> str:
        return self.comment_text[:50]  + '...' if len(self.comment_text) > 50 else self.comment_text
    
    @property
    def liked_count(self):
        return self.liked.count() if self.liked else 0
    
    @property
    def disliked_count(self):
        return self.disliked.count() if self.disliked else 0

    def save(self, *args, **kwargs):
        if not self.comment_slug:
            self.comment_slug=slugify(self.comment_text)
        if self.active:
            self.status = self.Status.PUBLİSHED
        else:
            self.status = self.Status.DRAFT
        super().save(*args, **kwargs)