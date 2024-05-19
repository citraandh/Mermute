from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('dashboard/', dashboard, name='dashboard'),
    path('konten/', konten, name='konten'),
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),



    # citra
    path('kelola_playlist/', kelola_playlist, name='kelola_playlist'),
    path('daftar_playlist/',
         daftar_playlist, name='daftar_playlist'),
    path('kelola_playlist/<uuid:id_playlist>/',
         user_playlist_detail, name='kelola_playlist_detail'),
    path('play/<uuid:id_song>/', play_song, name='play_song'),


    # darrel
    path('langganan_paket/', langganan_paket, name='langganan_paket'),
    path('pembayaran/<str:jenis_paket>/<int:harga>/',
         pembayaran, name='pembayaran'),
    path('pembayaran_final/', pembayaran_final, name='pembayaran_final'),
    path('riwayat_transaksi/', riwayat_transaksi, name='riwayat_transaksi'),
    path('search_bar/', search_bar, name='search_bar'),
    path('search', search, name='search'),
    path('detail-konten/<str:judul>/<str:nama>/<str:tipe>',
         detail_konten, name='detail_konten'),
    path('downloaded-song/', downloaded_song, name='downloaded_song'),
    path('downloaded-song-delete/<str:judul>',
         downloaded_song_delete, name='downloaded_song_delete'),
    path('bukan_premium/', bukan_premium, name='bukan_premium'),

    # clarence
    path('podcast/detail/', podcast_detail, name='podcast_page'),
    path('chart/', chart_list, name='chart'),
    path('chart/<int:chart_id>', chart_detail, name='chart_detail'),
    path('podcast/', podcast_manager, name='podcast'),
    path('episodes/<uuid:podcast_id>', list_episode_ajax, name='list_episode'),
    path('podcasts/', list_podcast_ajax, name='list_podcast'),
    path('podcast/add/', add_podcast, name='add_podcast'),
    path('podcast/delete/<uuid:podcast_id>',
         delete_podcast, name='delete_podcast'),
    path('episode/add/<uuid:podcast_id>', add_episode, name='add_episode'),
    path('episode/delete/<uuid:episode_id>',
         delete_episode, name='delete_episode'),
    path('', landing_page, name='landing_page'),
    path('dashboard/', dashboard, name='dashboard'),
    path('konten/', konten, name='konten'),
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),

]
