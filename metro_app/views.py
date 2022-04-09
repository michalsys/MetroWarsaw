from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from metro_app.utils import randomize
from metro_app.forms import NewCharacterForm
from metro_app.models import Character, Location, Faction, Event, CharacterEquipment, Equipment, Enemy

from random import randint
# Create your views here.


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class NewCharacterView(LoginRequiredMixin, View):
    def get(self, request):
        form = NewCharacterForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = NewCharacterForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.user = request.user
            character.location = Location.objects.get(id=1)
            character.save()
            return redirect('character_list')
        return render(request, 'form.html', {'form': form})


class CharacterListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        user = User.objects.get(id=self.request.user.id)
        return Character.objects.filter(user=user)
    template_name = 'metro_app/character_list.html'


class DeleteCharacterView(UserPassesTestMixin, LoginRequiredMixin, View):
    def test_func(self):
        character = Character.objects.get(pk=self.kwargs['id'])
        return character.user_id == self.request.user.id

    def get(self, request, id):
        return render(request, 'form.html', {'deletion': True})

    def post(self, request, id):
        character = Character.objects.get(pk=id)
        character.delete()
        return redirect('character_list')


class GameView(UserPassesTestMixin, LoginRequiredMixin, View):
    def test_func(self):
        character = Character.objects.get(pk=self.kwargs['id'])
        return character.user_id == self.request.user.id

    def get(self, request, id):
        character = Character.objects.get(pk=id)
        location = Location.objects.get(pk=character.location_id)
        faction = location.faction
        equipment = CharacterEquipment.objects.filter(character_id=character.id)
        return render(request, 'metro_app/next_level.html',
                      {'character': character, 'location': location, 'faction': faction, 'equipment': equipment})

    def post(self, request, id):
        random_outcome = randomize()
        base_location_id = random_outcome['location_id']
        base_event_id = random_outcome['event_id']
        faction_id = random_outcome['faction_id']
        bullets_found = random_outcome['bullets_found']
        bullets_looted = 0
        bullets_shot = 0
        enemy_id = random_outcome['enemy_id']
        enemies_quant = random_outcome['enemies']
        hp_lost = random_outcome['hp_lost']
        new_event = Event.objects.get(pk=base_event_id)
        new_event.pk = None
        new_event.save()
        new_location = Location.objects.get(pk=base_location_id)
        new_location.pk = None
        if faction_id != 4:
            faction = Faction.objects.get(pk=faction_id)
            new_location.faction = faction
        else:
            faction = None
        new_location.event = new_event
        new_location.save()
        if enemies_quant != 0:
            for enemy in range(enemies_quant):
                base_enemy = Enemy.objects.get(pk=enemy_id)
                new_enemy = base_enemy
                new_enemy.pk = None
                new_enemy.location = new_location
                new_enemy.health = randint(1, base_enemy.health)
                new_enemy.bullets = randint(1, base_enemy.bullets)
                bullets_found += new_enemy.bullets
                bullets_shot += new_enemy.health
                new_enemy.save()
        character = Character.objects.get(pk=id)
        equipment = CharacterEquipment.objects.filter(character_id=character.id)
        enemies = Enemy.objects.filter(location_id=new_location.id)
        old_location = character.location
        old_event = character.location.event
        character.location = new_location
        character.save_date = timezone.now()
        character.bullets += bullets_found
        character.bullets += bullets_looted
        character.bullets -= bullets_shot
        bullets_in_plus = bullets_found + bullets_looted
        if character.bullets < 0:
            character.bullets = 0
        if character.bullets < 100:
            character.health -= hp_lost
            if character.health > 0:
                character.save()
                if old_location != Location.objects.get(pk=1):
                    old_location.delete()
                if old_event:
                    old_event.delete()
                return render(request, 'metro_app/next_level.html',
                              {'character': character,
                               'base_location_id': base_location_id,
                               'location': new_location,
                               'base_event_id': base_event_id,
                               'event': new_event,
                               'faction': faction,
                               'equipment': equipment,
                               'bullets_in_plus': bullets_in_plus,
                               'bullets_in_minus': bullets_shot,
                               'enemies_quant': enemies_quant,
                               'enemies': enemies,
                               'hp_lost': hp_lost})
            else:
                character.save()
                return redirect(reverse('death', args=[id]))
        elif character.bullets > 99:
            character.save()
            return redirect(reverse('victory', args=[id]))


class RestView(UserPassesTestMixin, LoginRequiredMixin, View):
    def test_func(self):
        character = Character.objects.get(pk=self.kwargs['id'])
        return character.user_id == self.request.user.id and character.bullets > 4

    def get(self, request, id):
        return render(request, 'form.html', {'rest': True})

    def post(self, request, id):
        character = Character.objects.get(pk=id)
        character.health += 5
        if character.health > 10:
            character.health = 10
        character.bullets -= 5
        character.save()
        return redirect(reverse('game', args=[id]))


class WinningScreenView(UserPassesTestMixin, LoginRequiredMixin, View):
    def test_func(self):
        if self.request.method == 'GET':
            character = Character.objects.get(pk=self.kwargs['id'])
            return character.user_id == self.request.user.id and character.bullets > 99
        else:
            return True

    def get(self, request, id):
        character = Character.objects.get(pk=id)
        character.delete()
        return render(request, 'form.html', {'victory': True})

    def post(self, request, id):
        return redirect('character_list')


class CharacterDeathView(UserPassesTestMixin, LoginRequiredMixin, View):
    def test_func(self):
        if self.request.method == 'GET':
            character = Character.objects.get(pk=self.kwargs['id'])
            return character.user_id == self.request.user.id and character.health < 1
        else:
            return True

    def get(self, request, id):
        character = Character.objects.get(pk=id)
        character.delete()
        return render(request, 'form.html', {'death': True})

    def post(self, request, id):
        return redirect('character_list')
