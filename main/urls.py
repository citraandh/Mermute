from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('dashboard/', dashboard, name='dashboard'),
    path('konten/', konten, name='konten'),
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),



    # citra
    path('kelola_playlist/', kelola_playlist, name='kelola_playlist'),
    path('kelola_playlist/daftar_playlist',
         daftar_playlist, name='daftar_playlist'),
    path('kelola_playlist/kelola_playlist_awal',
         playlist_awal, name='playlist_awal'),
    path('kelola_playlist/kelola_playlist_detail',
         user_playlist_detail, name='kelola_playlist_detail'),

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
    path('podcast/detail/<uuid:podcast_id>',
         podcast_detail, name='podcast_page'),
    path('chart/', chart_list, name='chart'),
    path('chart/<int:chart_id>', chart_detail, name='chart_detail'),
    path('podcast/', podcast_manager, name='podcast'),
    path('episodes/<uuid:podcast_id>', list_episode_ajax, name='list_episode'),
]
