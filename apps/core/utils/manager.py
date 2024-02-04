from django.db import models
from apps.core import models as mod


class PublishedNewsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=mod.News.Status.PUBLİSHED)


class PublishedNewsCommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=mod.News_comment.Status.PUBLİSHED)
    

class PublishedEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=mod.Event.Status.PUBLİSHED)


class PublishedEventCommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=mod.Event_comment.Status.PUBLİSHED)