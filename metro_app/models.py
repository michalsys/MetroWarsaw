from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Equipment(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Faction(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=64)
    threat_level = models.SmallIntegerField()
    faction = models.ForeignKey(Faction, null=True, blank=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=32)
    bullets = models.IntegerField(default=0)
    health = models.SmallIntegerField(default=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    save_date = models.DateTimeField(auto_now_add=True)
    equipment = models.ManyToManyField(Equipment, through='CharacterEquipment')
    location = models.ForeignKey(Location, default=1, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return self.name


class Enemy(models.Model):
    name = models.CharField(max_length=32)
    bullets = models.IntegerField(default=0)
    health = models.SmallIntegerField(default=5)
    equipment = models.ManyToManyField(Equipment, through='EnemyEquipment')
    faction = models.ForeignKey(Faction, null=True, blank=True, on_delete=models.SET_NULL)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CharacterEquipment(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.equipment.name


class EnemyEquipment(models.Model):
    enemy = models.ForeignKey(Enemy, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.equipment.name
