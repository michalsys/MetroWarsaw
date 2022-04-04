"""MetroGame URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from metro_app import views

urlpatterns = [
    path('new_game/', views.NewCharacterView.as_view(), name='new_game'),
    path('character_list/', views.CharacterListView.as_view(), name='character_list'),
    path('game/<int:id>/', views.GameView.as_view(), name='game'),
    path('delete/<int:id>/', views.DeleteCharacterView.as_view(), name='delete'),
    path('victory/<int:id>/', views.WinningScreenView.as_view(), name='victory'),
    path('death/<int:id>/', views.CharacterDeathView.as_view(), name='death'),
    path('rest/<int:id>/', views.RestView.as_view(), name='rest')
]
