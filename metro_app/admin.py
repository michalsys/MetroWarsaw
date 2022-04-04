from django.contrib import admin
from metro_app.models import Character, Enemy, Location, Equipment, Faction, CharacterEquipment, EnemyEquipment, Event

# Register your models here.

admin.site.register(Character)
admin.site.register(Enemy)
admin.site.register(Location)
admin.site.register(Equipment)
admin.site.register(Faction)
admin.site.register(Event)
admin.site.register(CharacterEquipment)
admin.site.register(EnemyEquipment)
