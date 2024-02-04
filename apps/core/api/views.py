from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.generics import (
    ListCreateAPIView, 
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    RetrieveAPIView
    )

from .serializers import (
    NewsSerializer,
    NewsPostSerializer,
    NewsDetailSerializer,
    NewsCommentSerializer,
    NewsCommentPostSerializer,
    EventSerializer,
    EventDetailSerializer,
    EventPostSerializer,
    EventCommentPostSerializer,
    EventCommentSerializer
    )

from apps.core.models import (
    News,
    News_comment,
    IPs,
    Event,
    Event_comment
    )



class NewsListCreateAPIView(ListCreateAPIView):
    serializer_class = NewsSerializer
    queryset = News.published.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewsPostSerializer
        return super().get_serializer_class()


class NewsDetailAPIView(RetrieveAPIView):
    serializer_class = NewsDetailSerializer
    queryset = News.published.all()

    def get(self, request, pk, format=None):
        news = get_object_or_404(News, pk=pk)
        ip = self.get_client_ip(request)
        ip_obj, created = IPs.objects.get_or_create(view_ip=ip)
        news.viewed_ips.add(ip_obj)
        serializer = NewsDetailSerializer(news)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    

class NewsUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = NewsSerializer
    queryset = News.published.all()


class NewsCommentCreateAPIView(CreateAPIView):
    serializer_class = NewsCommentPostSerializer


class NewsCommentLikeDislikeAPIView(APIView):
    serializer_class = NewsCommentSerializer
    queryset = News_comment.objects.all()

    def get(self, request, pk, *args, **kwargs):
        params = request.query_params
        user = request.user
        news_comment = get_object_or_404(News_comment, pk=pk)
        if params.get("case") == '1':
            news_comment.liked.add(user)
            if user in news_comment.disliked.all():
                news_comment.disliked.remove(user)
        if params.get("case") == '-1':
            news_comment.disliked.add(user)
            if user in news_comment.liked.all():
                news_comment.liked.remove(user)
        if params.get("case") == '0':
            news_comment.liked.remove(user)
            news_comment.disliked.remove(user)
            
        return Response("OK")


class NewsCommentDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = NewsCommentSerializer
    queryset = News_comment.published.all()


class EventListCreateAPIView(ListCreateAPIView):
    serializer_class = EventSerializer
    queryset = Event.published.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EventPostSerializer
        return super().get_serializer_class()


class EventDetailAPIView(RetrieveAPIView):
    serializer_class = EventDetailSerializer
    queryset = Event.published.all()

    def get(self, request, pk, format=None):
        event = get_object_or_404(Event, pk=pk)
        ip = self.get_client_ip(request)
        ip_obj, created = IPs.objects.get_or_create(view_ip=ip)
        event.viewed_ips.add(ip_obj)
        serializer = EventDetailSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class EventUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    queryset = Event.published.all()


class EventCommentCreateAPIView(CreateAPIView):
    serializer_class = EventCommentPostSerializer


class EventCommentUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = EventCommentSerializer
    queryset = Event_comment.published.all()


class EventCommentLikeDislikeAPIView(APIView):
    serializer_class = EventCommentSerializer
    queryset = Event_comment.objects.all()

    def get(self, request, pk, *args, **kwargs):
        params = request.query_params
        user = request.user
        event_comment = get_object_or_404(Event_comment, pk=pk)
        if params.get("case") == '1':
            event_comment.liked.add(user)
            if user in event_comment.disliked.all():
                event_comment.disliked.remove(user)
        if params.get("case") == '-1':
            event_comment.disliked.add(user)
            if user in event_comment.liked.all():
                event_comment.liked.remove(user)
        if params.get("case") == '0':
            event_comment.liked.remove(user)
            event_comment.disliked.remove(user)
        
        return Response("OK")
