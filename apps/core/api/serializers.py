from rest_framework import serializers
from django.utils.timesince import timesince

from apps.core.models import (
    News, 
    News_comment,
    Event,
    Event_comment
    )



class NewsCommentSerializer(serializers.ModelSerializer):
    days_since_created = serializers.SerializerMethodField()
    comment_author = serializers.SerializerMethodField()
    class Meta:
        model = News_comment
        fields = (
            'id',
            'comment_text',
            'comment_author',
            'days_since_created',
            'liked_count',
            'disliked_count'
            )
        
    def get_days_since_created(self, obj):
        timesince_str = timesince(obj.published_at)
        if 'day' in timesince_str:
            days = timesince_str.split()[0]
            return f'{days} days ago'
        return 0
    
    def get_comment_author(self, obj):
        return f'{obj.comment_author.first_name} {obj.comment_author.last_name}'


class NewsCommentPostSerializer(serializers.ModelSerializer):
    comment_author = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = News_comment
        fields = (
            'id',
            'comment_text',
            'comment_author',
            'news'
        )
    
    def validate(self, attrs):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError('You have to log in')

        attrs['comment_author'] = request.user
        return attrs
    

class NewsSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    class Meta:
        model = News
        fields = ('id',
                  'news_title',
                  'news_image',
                  'news_content',
                  'news_count',
                  'published_date',
                  'comment_count', 
                  'author',
                  'get_absolute_url',
                  'view_count'
                  )
        
    def get_comment_count(self, obj):
        return obj.news_comments.count()
    
    def get_author(self, obj):
        return f'{obj.author.first_name} {obj.author.last_name}'
    

class NewsDetailSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    published_date = serializers.SerializerMethodField()
    news_comments = NewsCommentSerializer(many=True)
    class Meta:
        model = News
        fields = (
            'id',
            'news_title',
            'news_content',
            'news_image',
            'comment_count',
            'author',
            'published_date',
            'news_comments',
            'view_count'

        )

    def get_comment_count(self, obj):
        return obj.news_comments.count()
    
    def get_author(self, obj):
        return f'{obj.author.first_name} {obj.author.last_name}'
    
    def get_published_date(self, obj):
        return obj.published_at.strftime('%b %d, %Y at %I:%M %p')
    

class NewsPostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = News
        fields = (
            'news_title',
            'news_content',
            'news_image',
            'author'
            )
        
    def validate(self, attrs):
            request = self.context.get('request')

            if not request or not request.user.is_authenticated:
                raise serializers.ValidationError('You have to log in')

            attrs['author'] = request.user
            return attrs


class EventCommentSerializer(serializers.ModelSerializer):
    days_since_created = serializers.SerializerMethodField()
    comment_author = serializers.SerializerMethodField()
    class Meta:
        model = Event_comment
        fields = (
            'id',
            'comment_text',
            'comment_author',
            'days_since_created',
            'liked_count',
            'disliked_count'
            )
        
    def get_days_since_created(self, obj):
        timesince_str = timesince(obj.published_at)
        if 'day' in timesince_str:
            days = timesince_str.split()[0]
            return f'{days} days ago'
        return 0
    
    def get_comment_author(self, obj):
        return f'{obj.comment_author.first_name} {obj.comment_author.last_name}'


class EventCommentPostSerializer(serializers.ModelSerializer):
    comment_author = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Event_comment
        fields = (
            'id',
            'comment_text',
            'comment_author',
            'event'
        )
    
    def validate(self, attrs):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError('You have to log in')

        attrs['comment_author'] = request.user
        return attrs


class EventSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = ('id',
                  'event_title',
                  'event_photo', 
                  'event_location',
                  'event_count',
                  'published_date',
                  'comment_count', 
                  'view_count'
                  )
        
    def get_comment_count(self, obj):
        return obj.event_comments.count()
    

class EventPostSerializer(serializers.ModelSerializer):
    event_author = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Event
        fields = (
            'id',
            'event_title', 
            'event_content',
            'event_photo',
            'event_location',
            'event_author'
        )

    def validate(self, attrs):
            request = self.context.get('request')

            if not request or not request.user.is_authenticated:
                raise serializers.ValidationError('You have to log in')

            attrs['event_author'] = request.user
            return attrs


class EventDetailSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    event_author = serializers.SerializerMethodField()
    published_date = serializers.SerializerMethodField()
    event_comments = EventCommentSerializer(many=True)
    class Meta:
        model = Event
        fields = (
            'id',
            'event_title', 
            'event_content',
            'event_photo',
            'event_location',
            'event_author',
            'comment_count',
            'published_date',
            'event_comments'
            'view_count'
        )
        

    def get_comment_count(self, obj):
        return obj.event_comments.count()
    
    def get_event_author(self, obj):
        return f'{obj.event_author.first_name} {obj.event_author.last_name}'
    
    def get_published_date(self, obj):
        return obj.published_at.strftime('%b %d, %Y at %I:%M %p')