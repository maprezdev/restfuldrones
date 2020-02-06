# drones/serializers.py file
from rest_framework import serializers
from drones.models import DroneCategory, Drone, Pilot, Competition
import drones.views


class DroneCategorySerializer(serializers.HyperlinkedModelSerializer):
    """defines a one-to-many relationship that is read-
only"""
    drones = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='drone-detail',  # browsable API feature
    )

    class Meta:
        """model related to the serializer, and field names that we want
        to include in the serialization"""
        model = DroneCategory
        fields = (
            'url',
            'pk',
            'name',
            'drones')


class DroneSerializer(serializers.HyperlinkedModelSerializer):
    """display the drone category name"""
    drone_category = serializers.SlugRelatedField(
        queryset=DroneCategory.objects.all(),
        slug_field='name')

    class Meta:
        """model related to the serializer, and field names that we want
        to include in the serialization"""
        model = Drone
        fields = (
            'url',
            'name',
            'drone_category',
            'manufacturing_date',
            'has_it_competed',
            'inserted_timestamp',
        )


class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    """display all the details for the related Drone"""
    drone = DroneSerializer()

    class Meta:
        """model related to the serializer, and field names that we want
        to include in the serialization"""
        model = Competition
        fields = (
            'url',
            'pk',
            'distance_in_feet',
            'distance_achievement_date',
            'drone')


class PilotSerializer(serializers.HyperlinkedModelSerializer):
    """serialize Pilot instances and serialize all the Competition instances related to the Pilot"""
    competitions = CompetitionSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(choices=Pilot.gender_choices)
    gender_description = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        """model related to the serializer, and field names that we want
        to include in the serialization"""
        model = Pilot
        fields = (
            'url',
            'name',
            'gender',
            'gender_description',
            'races_count',
            'inserted_timestamp',
            'competitions')


class PilotCompetitionSerializer(serializers.ModelSerializer):
    """display the related Pilot name and the related Drone name"""
    pilot = serializers.SlugRelatedField(
        queryset=Pilot.objects.all(),
        slug_field='name')

    drone = serializers.SlugRelatedField(
        queryset=Drone.objects.all(),
        slug_field='name')

    class Meta:
        """model related to the serializer, and field names that we want
        to include in the serialization"""
        model = Competition
        fields = (
            'url',
            'pk',
            'distance_in_feet',
            'distance_achievement_date',
            'pilot',
            'drone')