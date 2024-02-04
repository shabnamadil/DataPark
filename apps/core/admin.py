from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode

from .utils.filters import (
    ViewCountListFilter,
    LikedCountListFiilter,
    DislikedCountListFilter
)

from apps.core.models import (
    News, 
    News_comment, 
    IPs,
    Event, 
    Event_comment
)



@admin.action(description="Mark selected aritcles as published")
def make_published(self, request, queryset):
    queryset.update(status="PB")

@admin.action(description="Mark selected aritcles as draft")
def make_draft(self, request, queryset):
    queryset.update(status="DF")

@admin.action(description="Mark selected comments as active")
def make_active(self, request, queryset):
    queryset.update(active=True, status="PB")

@admin.action(description="Mark selected comments as inactive")
def make_inactive(self, request, queryset):
    queryset.update(active=False, status="DF")



@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('news_title', 'show_comments_count', 'news_for_author', 'view_count', 'status')
    ordering = ('-updated_at', 'news_title', 'author__username')
    search_fields = ('news_title', 'author__username')
    list_filter = ('published_at', 'status', ViewCountListFilter)
    date_hierarchy = 'published_at'
    list_per_page = 20
    autocomplete_fields = ('author', )
    actions =[make_published, make_draft]
    readonly_fields = ['slug', 'view_count', 'viewed_ips']

    def show_comments_count(self, obj):
        result = News_comment.objects.filter(news=obj).count()
        return result
    show_comments_count.short_description = 'RƏYLƏRİN SAYI'

    def news_for_author(self, obj):
        author = obj.author
        if author:
            url = (
                reverse("admin:core_news_changelist")
                + "?"
                + urlencode({"author__id": f"{obj.author.id}"})
            )
            return format_html('<a href="{}">{}</a>', url, author)
    news_for_author.short_description = "MÜƏLLİF"


@admin.register(News_comment)
class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ('comment_text_truncated',  'comment_for_author', 'comment_for_news', 'active', 'liked_count' , 'disliked_count')
    readonly_fields = ['comment_slug', 'liked', 'disliked', 'liked_count', 'disliked_count']
    ordering = ('-published_at', 'comment_author__username', 'news__news_title')
    search_fields = ('comment_text', 'comment_author__username', 'news__news_title')
    list_filter = ('active', 'published_at', LikedCountListFiilter, DislikedCountListFilter)
    date_hierarchy = 'published_at'
    list_per_page = 20
    autocomplete_fields = ('comment_author', 'news')
    fields = ('published_at', 'comment_text', 'news', 'comment_author', 'active', 'comment_slug', 'liked', 'disliked')
    actions =[make_active, make_inactive]

    def comment_for_author(self, obj):
        author = obj.comment_author
        if author:
            url = (
                reverse("admin:core_news_comment_changelist")
                + "?"
                + urlencode({"comment_author__id": f"{obj.comment_author.id}"})
            )
            return format_html('<a href="{}">{}</a>', url, author)
    comment_for_author.short_description = "MÜƏLLİF"

    def comment_for_news(self, obj):
        news = obj.news
        if news:
            url = (
                reverse("admin:core_news_comment_changelist")
                + "?"
                + urlencode({"news__id": f"{obj.news.id}"})
            )
            return format_html('<a href="{}">{}</a>', url, news)
    comment_for_news.short_description = "Xəbər"

    def comment_text_truncated(self, obj):
        return obj.comment_text[:25] + '...' if len(obj.comment_text) > 25 else obj.comment_text
    comment_text_truncated.short_description = 'Comment Text'


@admin.register(IPs)
class IPsAdmin(admin.ModelAdmin):
   list_per_page = 20
   readonly_fields = ('view_ip', )

       
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'event_location', 'event_for_author', 'status', 'show_event_comments_count', 'view_count')
    ordering = ('-updated_at', 'event_title', 'event_author__username')
    search_fields = ('event_title', 'event_location', 'event_author')
    list_filter = ('published_at', 'status', ViewCountListFilter)
    date_hierarchy = 'published_at'
    list_per_page = 20
    autocomplete_fields = ('event_author', )
    actions =["make_published", "make_draft"]
    readonly_fields = ['event_slug', 'view_count', 'viewed_ips']
    actions = [make_published, make_draft]

    def show_event_comments_count(self, obj):
        result = Event_comment.objects.filter(event=obj).count()
        return result
    show_event_comments_count.short_description = 'RƏYLƏRİN SAYI'

    def event_for_author(self, obj):
        author = obj.event_author
        if author:
            url = (
                reverse("admin:core_event_changelist")
                + "?"
                + urlencode({"event_author__id": f"{obj.event_author.id}"})
            )
            return format_html('<a href="{}">{}</a>', url, author)
    event_for_author.short_description = "MÜƏLLİF"


@admin.register(Event_comment)
class EventCommentAdmin(admin.ModelAdmin):
    list_display = ('comment_text_truncated', 'comment_for_author', 'comment_for_events', 'active', 'liked_count', 'disliked_count')
    readonly_fields = ['comment_slug', 'liked', 'disliked', 'liked_count', 'disliked_count']
    ordering = ('-published_at', 'comment_author__username', 'event__event_title')
    search_fields = ('comment_text', 'comment_author__username', 'event__event_title')
    list_filter = ('active', 'published_at', LikedCountListFiilter, DislikedCountListFilter)
    date_hierarchy = 'published_at'
    list_per_page = 20
    autocomplete_fields = ('comment_author', 'event')
    fields = ('published_at', 'comment_text', 'event', 'comment_author', 'active', 'comment_slug', 'liked', 'disliked')
    actions =[make_active, make_inactive]

    def comment_for_author(self, obj):
        author = obj.comment_author
        if author:
            url = (
                reverse("admin:core_event_comment_changelist")
                + "?"
                + urlencode({"comment_author__id": f"{obj.comment_author.id}"})
            )
            return format_html('<a href="{}">{}</a>', url, author)
    comment_for_author.short_description = "MÜƏLLİF"

    def comment_for_events(self, obj):
        news = obj.event
        if news:
            url = (
                reverse("admin:core_event_comment_changelist")
                + "?"
                + urlencode({"event__id": f"{obj.event.id}"})
            )
            return format_html('<a href="{}">{}</a>', url, news)
    comment_for_events.short_description = "HADİSƏ"

    def comment_text_truncated(self, obj):
        return obj.comment_text[:25] + '...' if len(obj.comment_text) > 25 else obj.comment_text
    comment_text_truncated.short_description = 'Comment Text'

