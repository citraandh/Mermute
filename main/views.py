import json
from django.shortcuts import render
from django.http import JsonResponse
from utils.query import *
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Akun, UserPlaylist, Song, AkunPlaySong, AkunPlayUserPlaylist
from django.contrib.auth.decorators import login_required
from datetime import datetime
import uuid

@login_required
def kelola_playlist(request):
    # Ambil semua playlist yang dibuat oleh pengguna ini
    playlists = UserPlaylist.objects.filter(email_pembuat=request.user.email)
    context = {'playlists': playlists}

    # Cek apakah pengguna telah membuat playlist atau belum
    if playlists.exists():
        return render(request, 'kelola_playlist.html', context)
    else:
        return render(request, 'kelola_playlist.html', {'message': "Anda Belum Memiliki Playlist"})

@login_required
def play_song(request, song_id):
    song = Song.objects.get(id_konten=song_id)
    genres = song.genre_set.all()  # Asumsikan 'Song' memiliki relation ke model 'Genre'
    context = {
        'song': song,
        'genres': genres,
        'is_premium': request.user.is_premium  # Asumsikan Akun memiliki atribut is_premium
    }
    return render(request, 'play_song.html', context)

@login_required
def play_user_playlist(request, user_playlist_id):
    user_playlist = UserPlaylist.objects.get(id_user_playlist=user_playlist_id)
    songs = user_playlist.song_set.all()  # Asumsikan UserPlaylist memiliki relation ke model 'Song'

    # Menghitung total durasi playlist
    total_durasi = sum(song.durasi for song in songs)
    total_durasi_str = f"{total_durasi // 60} jam {total_durasi % 60} menit"

    context = {
        'user_playlist': user_playlist,
        'songs': songs,
        'total_durasi': total_durasi_str
    }
    return render(request, 'play_user_playlist.html', context)

@login_required
def shuffle_play(request, user_playlist_id):
    # Logic untuk membuat entry AKUN_PLAY_USER_PLAYLIST dan AKUN_PLAY_SONG
    user_playlist = UserPlaylist.objects.get(id_user_playlist=user_playlist_id)
    timestamp = datetime.now()

    # Membuat entry untuk AKUN_PLAY_USER_PLAYLIST
    AkunPlayUserPlaylist.objects.create(
        email_pemain=request.user,
        id_user_playlist=user_playlist,
        email_pembuat=user_playlist.email_pembuat,
        waktu=timestamp
    )

    # Membuat entry untuk setiap AKUN_PLAY_SONG di playlist
    for song in user_playlist.song_set.all():
        AkunPlaySong.objects.create(
            email_pemain=request.user,
            id_song=song,
            waktu=timestamp
        )

    # Redirect kembali ke halaman detail playlist
    return redirect('play_user_playlist', user_playlist_id=user_playlist_id)

@login_required
def add_song_to_playlist(request, song_id):
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist')
        playlist = UserPlaylist.objects.get(id_user_playlist=playlist_id)
        song = Song.objects.get(id_konten=song_id)

        # Tambahkan lagu ke playlist
        playlist.songs.add(song)
        playlist.save()

        # Informasikan ke pengguna bahwa lagu telah ditambahkan
        context = {
            'message': f"Berhasil menambahkan lagu '{song.judul}' ke playlist '{playlist.judul}'!",
            'playlist': playlist
        }
        return render(request, 'success_message.html', context)

    # Jika GET, tampilkan form untuk menambahkan lagu ke playlist
    playlists = UserPlaylist.objects.filter(email_pembuat=request.user.email)
    context = {
        'playlists': playlists,
        'song': Song.objects.get(id_konten=song_id)
    }
    return render(request, 'add_song_to_playlist.html', context)