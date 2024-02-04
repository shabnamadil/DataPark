from django.urls import path
from .views import (
    CDOListCreateAPIView,
    TalentPoolListCreateAPIView,
    TalentLevelAPIListView,
    TalentPositionAPIListView,
    TalentSectorAPIListView,
    CDOUpdateDestroyAPIView,
    TalentPoolUpdateDestroyAPIView
)

urlpatterns = [
    path('chief-data-officers/', CDOListCreateAPIView.as_view(), name='chief-data-officers'),
    path('chief-data-officers/<int:pk>/', CDOUpdateDestroyAPIView.as_view(), name='chief-data-officers-delete'),
    path('talent-pool/', TalentPoolListCreateAPIView.as_view(), name='talent-pool'),
    path('talent-pool/<int:pk>', TalentPoolUpdateDestroyAPIView.as_view(), name='talent-pool-delete'),
    path('talent-positions/', TalentPositionAPIListView.as_view(), name="talent-positions"),
    path('talent-levels/', TalentLevelAPIListView.as_view(), name="talent-levels"),
    path('talent-sectors/', TalentSectorAPIListView.as_view(), name="talent-sectors")
]