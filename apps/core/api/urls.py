from django.urls import path

from .views import (
    NewsListCreateAPIView,
    NewsDetailAPIView,
    NewsUpdateDestroyAPIView,
    NewsCommentCreateAPIView,
    NewsCommentDestroyAPIView,
    EventListCreateAPIView,
    EventDetailAPIView,
    EventUpdateDestroyAPIView,
    EventCommentUpdateDestroyAPIView,
    EventCommentCreateAPIView,
    NewsCommentLikeDislikeAPIView,
    EventCommentLikeDislikeAPIView
    )

urlpatterns = [
    path('news/', NewsListCreateAPIView.as_view(), name='news'),
    path('news/<int:pk>/', NewsDetailAPIView.as_view(), name='news-detail'),
    path('news-update/<int:pk>/', NewsUpdateDestroyAPIView.as_view(), name='news-update'),
    path('news-comment/', NewsCommentCreateAPIView.as_view(), name='news-comment-create'),
    path('news-comment/<int:pk>/', NewsCommentDestroyAPIView.as_view(), name='news-comment-delete'),
    path('news-comment/like-dislike/<int:pk>/',NewsCommentLikeDislikeAPIView.as_view(), name='news-comment-like-dislike'),
    path('events/', EventListCreateAPIView.as_view(), name='events'),
    path('events/<int:pk>/', EventDetailAPIView.as_view(), name='event-detail'),
    path('event-update/<int:pk>/', EventUpdateDestroyAPIView.as_view(), name='event-delete'),
    path('event-comment/', EventCommentCreateAPIView.as_view(), name='event-comment-create'),
    path('event-comment/<int:pk>/', EventCommentUpdateDestroyAPIView.as_view(), name='event-comment-delete'),
    path('event-comment/like-dislike/<int:pk>/', EventCommentLikeDislikeAPIView.as_view(), name='event-comment-like-dislike')
]