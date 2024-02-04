from rest_framework.response import Response

from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView)

from apps.community.models import (
    ChiefDataOfficers,
    TalentPool, 
    TalentPosition,
    TalentLevel,
    TalentSector
)

from .serializers import (
    CDOListSerializer,
    CDOPostSerializer,
    TalentPoolListSerializer,
    TalentPoolPostSerializer,
    TalentPositionListSerializer,
    TalentLevelListSerializer,
    TalentSectorListSerializer
)

from .repositories import TalentPoolRepository


class CDOListCreateAPIView(ListCreateAPIView):
    serializer_class = CDOListSerializer
    queryset = ChiefDataOfficers.published.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CDOPostSerializer
        return super().get_serializer_class()
    

class CDOUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CDOListSerializer
    queryset = ChiefDataOfficers.published.all()


class TalentPoolListCreateAPIView(ListCreateAPIView):
    serializer_class = TalentPoolListSerializer
    queryset = TalentPool.published.all()
    repo = TalentPoolRepository

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TalentPoolPostSerializer
        return super().get_serializer_class()
    
    def get_filter_methods(self):
        repo = self.repo()
        return {
            'sector' : repo.get_by_sector,
            'position' : repo.get_by_position,
            'level' : repo.get_by_level,
            'type' : repo.get_by_job_type,
            'location' : repo.get_by_work_location
        }

    def get_queryset(self, **kwargs):
        qs = self.repo().DEFAULT_QS
        filters = self.get_filter_methods()
        
        for key, value in self.request.query_params.items():
            
            if key in self.get_filter_methods():
                qs = filters[key](value, qs)

        return qs
    
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True,
                context={"request" : request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            qs,
            many=True,
            context={"request" : request}
        )
        return Response(serializer.data)


class TalentPoolUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TalentPoolListSerializer
    queryset = TalentPool.published.all()


class TalentPositionAPIListView(ListAPIView):
    serializer_class = TalentPositionListSerializer
    queryset = TalentPosition.activated.all()


class TalentLevelAPIListView(ListAPIView):
    serializer_class = TalentLevelListSerializer
    queryset = TalentLevel.activated.all()


class TalentSectorAPIListView(ListAPIView):
    serializer_class = TalentSectorListSerializer
    queryset = TalentSector.activated.all()
    