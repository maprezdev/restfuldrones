# drones/views.py file
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from drones.models import DroneCategory
from drones.models import Drone
from drones.models import Pilot
from drones.models import Competition
from drones.serializers import DroneCategorySerializer
from drones.serializers import DroneSerializer
from drones.serializers import PilotSerializer
from drones.serializers import PilotCompetitionSerializer
from django_filters import rest_framework as filters


class DroneCategoryList(generics.ListCreateAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-list'
    # enable to filter, search, and order by the name field
    filter_fields = ('name',)
    search_fields = ('^name',)
    ordering_fields = ('name',)


class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-detail'


class DroneList(generics.ListCreateAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-list'
    # enable to filter, search, and order by the name field
    filter_fields = (
        'name',
        'drone_category',
        'manufacturing_date',
        'has_it_competed',
    )
    search_fields = ('^name',)
    ordering_fields = ('name', 'manufacturing_date')


class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-detail'


class PilotList(generics.ListCreateAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-list'
    # enable to filter, search, and order by the name field
    filter_fields = (
        'name',
        'gender',
        'races_count'
    )
    search_fields = ('^name',)
    ordering_fields = (
        'name',
        'races_count'
    )


class PilotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-detail'


class CompetitionFilter(filters.FilterSet):
    """customized filters for the CompetitionList class"""
    from_achievement_date = filters.DateTimeFilter(
        field_name='distance_achievement_date', lookup_expr='gte')
    to_achievement_date = filters.DateTimeFilter(
        field_name='distance_achievement_date', lookup_expr='lte')
    min_distance_in_feet = filters.NumberFilter(
        field_name='distance_in_feet', lookup_expr='gte')
    max_distance_in_feet = filters.NumberFilter(
        field_name='distance_in_feet', lookup_expr='lte')
    drone_name = filters.AllValuesFilter(
        field_name='drone__name')
    pilot_name = filters.AllValuesFilter(
        field_name='pilot__name')

    class Meta:
        """model related to the filter set"""
        model = Competition
        # field names and filter names that we want to include
        # in the filters
        fields = [
            'distance_in_feet',
            'from_achievement_date',
            'to_achievement_date',
            'min_distance_in_feet',
            'max_distance_in_feet',
            # drone__name will be accessed as drone_name
            'drone_name',
            # pilot__name will be accessed as pilot_name
            'pilot_name']


class CompetitionList(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = 'competition-list'
    # filter and ordering
    filterset_class = CompetitionFilter
    filter_backends = (filters.DjangoFilterBackend,)
    ordering_fields = ('distance_in_feet', 'distance_achievement_date',)


class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = 'competition-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        """
        This method returns a Response object with key/value pairs of strings that provide a
        descriptive name for the view and its URL
        """
        return Response({
            'drone-categories': reverse(DroneCategoryList.name, request=request),
            'drones': reverse(DroneList.name, request=request),
            'pilots': reverse(PilotList.name, request=request),
            'competitions': reverse(CompetitionList.name, request=request)
        })
