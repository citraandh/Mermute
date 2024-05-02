from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    # Add your URL patterns here
    path('kelola_playlist/', kelola_playlist),
    path('play_song/<int:song_id>/', play_song),
    path('play_user_playlist/<int:user_playlist_id>/', play_user_playlist),
    path('shuffle_play/<int:user_playlist_id>/', shuffle_play),
    #Royalti
    path('royalty/', royalty_report, name='royalty_report'),
    #Label
    path('label/', label_report, name='label_report'),
    path('label/<int:album_id>/', label_album_detail, name='label_album_detail'),
    #Artist_Songwriter
    path('artist_songwriter/', artist_songwriter_report, name='artist_songwriter_report'),
    path('artist_songwriter/<int:album_id>/', artist_songwriter_album_detail, name='artist_songwriter_album_detail'),
]