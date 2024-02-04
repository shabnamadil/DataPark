from django.db import models
from apps.community import models as mod 


class PublishedCDOManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=mod.ChiefDataOfficers.Status.PUBLİSHED)
    

class PublishedTalentPoolManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=mod.TalentPool.Status.PUBLİSHED)


class ActiveTalentLevelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class ActiveTalentPositionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class ActiveTalentSectorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)