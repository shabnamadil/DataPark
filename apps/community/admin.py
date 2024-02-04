from django.contrib import admin
from .models import ChiefDataOfficers, TalentPool, TalentSector, TalentPosition, TalentLevel
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse


@admin.action(description="Mark selected aritcles as published")
def make_published(self, request, queryset):
    queryset.update(status="PB")

@admin.action(description="Mark selected aritcles as draft")
def make_draft(self, request, queryset):
    queryset.update(status="DF")

@admin.action(description="Mark selected items as active")
def make_active(self, request, queryset):
    queryset.update(active=True)

@admin.action(description="Mark selected items as inactive")
def make_inactive(self, request, queryset):
    queryset.update(active=False)


@admin.register(ChiefDataOfficers)
class CdoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'company', 'get_image', 'position',  'status')
    ordering = ('-published_at', 'name', 'surname')
    search_fields = ('name', 'surname', 'position', 'company')
    list_filter = ('published_at', 'status', 'position')
    date_hierarchy = 'published_at'
    list_per_page = 20
    actions =[make_published, make_draft]
    readonly_fields = ['slug']
    exclude = ['active']

    def get_image(self, obj):
        image = obj.image.url if obj.image else None
        raw_html = f'<img style="width:150px;height:auto;" src="{image}">'
        return format_html(raw_html)
    get_image.short_description = "Foto"


@admin.register(TalentPool)
class TalentPoolAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'level', 'company', 'get_image', 'job_type', 'status')
    ordering = ('-published_at', 'name', 'surname')
    search_fields = ('name', 'surname', 'position', 'company', 'level', 'job_type')
    list_filter = ('published_at', 'status', 'position', 'level', 'company', 'job_type')
    date_hierarchy = 'published_at'
    list_per_page = 20
    actions =[make_published, make_draft]
    readonly_fields = ['slug']
    exclude = ['active']

    def get_image(self, obj):
        image = obj.image.url if obj.image else None
        raw_html = f'<img style="width:150px;height:auto;" src="{image}">'
        return format_html(raw_html)
    get_image.short_description = "Foto"


@admin.register(TalentSector)
class TalentSectorAdmin(admin.ModelAdmin):
    list_display = ('sector_name', 'active')
    ordering = ('sector_name',)
    search_fields = ('sector_name', )
    list_filter = ('sector_name', 'active')
    list_per_page = 20
    readonly_fields = ['slug']
    actions =[make_active, make_inactive]
    exclude = ['status']
    

@admin.register(TalentPosition)
class TalentPositionAdmin(admin.ModelAdmin):
    list_display = ('position_name', 'active')
    ordering = ('position_name',)
    search_fields = ('position_name', )
    list_filter = ('position_name', 'active')
    list_per_page = 20
    readonly_fields = ['slug']
    actions =[make_active, make_inactive]
    exclude = ['status']


@admin.register(TalentLevel)
class TalentLevelAdmin(admin.ModelAdmin):
    list_display = ('level_name', 'active')
    ordering = ('level_name',)
    search_fields = ('level_name', )
    list_filter = ('level_name', 'active')
    list_per_page = 20
    readonly_fields = ['slug']
    actions =[make_active, make_inactive]
    exclude = ['status']