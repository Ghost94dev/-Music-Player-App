from django.urls import path
from Music import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "music"

urlpatterns = [
    path('', views.index, name='index'),
    path("songs/", views.song_list, name="song_list"),
    path('add-song/', views.add_song, name='add_song'),
    path('get-lyrics/', views.get_lyrics, name='get_lyrics'),

]
