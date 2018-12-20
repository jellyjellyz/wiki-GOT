from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('main_characters/', views.MainCharacterListView.as_view(), name='main_characters'),
    path('characters/', views.AllCharacterListView.as_view(), name='characters'),
    path('characters/<int:pk>/', views.CharacterDetailView.as_view(), name='character_detail'),

    path('characters/new/', views.CharacterCreateView.as_view(), name='character_new'),
    
    path('characters/filter/', views.CharacterFilterView.as_view(), name='character_filter'),
    path('characters/<int:pk>/delete', views.CharacterDeleteView.as_view(), name='character_delete'),
    path('characters/<int:pk>/update', views.CharacterUpdateView.as_view(), name='character_update'),

    path('relationship/new/', views.RelationCreateView.as_view(), name='relation_new'),

]