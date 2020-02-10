# drones/models.file.
from django.db import models


class DroneCategory(models.Model):
    name = models.CharField(max_length=250, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """returns the contents of the name attribute"""
        return self.name


class Drone(models.Model):
    name = models.CharField(max_length=250, unique=True)
    drone_category = models.ForeignKey(  # many-to-one relationship to the DroneCategory model
        DroneCategory,
        related_name='drones',  # backwards relation
        on_delete=models.CASCADE)
    manufacturing_date = models.DateTimeField()
    has_it_competed = models.BooleanField(default=False)
    inserted_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """returns the contents of the name attribute"""
        return self.name


class Pilot(models.Model):
    male = 'M'
    female = 'F'
    gender_choices = (
        (male, 'Male'),
        (female, 'Female'),
    )
    name = models.CharField(max_length=150, blank=False, unique=True)
    gender = models.CharField(max_length=2, choices=gender_choices, default=male)
    races_count = models.IntegerField()
    inserted_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """returns the contents of the name attribute"""
        return self.name


class Competition(models.Model):
    pilot = models.ForeignKey(  # many-to-one relationship to the Pilot model
        Pilot,
        related_name='competitions',  # backwards relation
        on_delete=models.CASCADE)
    drone = models.ForeignKey(  # many-to-one relationship to the Drone model
        Drone,
        on_delete=models.CASCADE)
    distance_in_feet = models.IntegerField()
    distance_achievement_date = models.DateTimeField()

    class Meta:
        ordering = ('-distance_in_feet',)
