from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('main_characters/', views.MainCharacterListView.as_view(), name='main_characters'),
    path('characters/', views.AllCharacterListView.as_view(), name='characters'),
    path('characters/<int:pk>/', views.CharacterDetailView.as_view(), name='character_detail'),
]