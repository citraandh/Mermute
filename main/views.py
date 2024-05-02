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

def dashboard(request):
  return render(request, 'dashboard.html')

def konten(request):
  return render(request, 'konten.html')

def landing_page(request):
  return render(request, 'landing_page.html')

def login(request):
  return render(request, 'login.html')

def register(request):
  return render(request, 'register.html')


# @login_required
def kelola_playlist(request):
    # Ambil semua playlist yang dibuat oleh pengguna ini
    playlists = UserPlaylist.objects.filter(email_pembuat=request.user.email)
    context = {'playlists': playlists}

    # Cek apakah pengguna telah membuat playlist atau belum
    if playlists.exists():
        return render(request, 'kelola_playlist.html', context)
    else:
        return render(request, 'kelola_playlist.html', {'message': "Anda Belum Memiliki Playlist"})

# @login_required
def play_song(request, song_id):
    song = Song.objects.get(id_konten=song_id)
    genres = song.genre_set.all()  # Asumsikan 'Song' memiliki relation ke model 'Genre'
    context = {
        'song': song,
        'genres': genres,
        'is_premium': request.user.is_premium  # Asumsikan Akun memiliki atribut is_premium
    }
    return render(request, 'play_song.html', context)

# @login_required
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

# @login_required
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

# @login_required
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

# Silakan tambahkan logic lainnya sesuai dengan kebutuhan aplikasi
def royalty_report(request):
  # Sample data for 5 rows
  royalty_data = [
    {
      "judul_lagu": "Lagu 1",
      "judul_album": "Album 1",
      "total_play": 3,
      "total_download": 0,
      "total_royalti": 450000,
    },
    {
      "judul_lagu": "Lagu 2",
      "judul_album": "Album 2",
      "total_play": 2,
      "total_download": 2,
      "total_royalti": 520000,
    },
    # Add 3 more rows with your data
  ]

  # Create the context dictionary
  context = {
    "royalty_data": royalty_data,
  }

  # Render the HTML template with the context
  return render(request, "royalti/list_royalti.html", context)

def label_report(request):
  # Replace this with your logic to fetch album data
  albums = [
    {
      "judul": "Album1",
      "jumlah_lagu": 0,
      "total_durasi": "0 menit",
    },
    {
      "judul": "Album2",
      "jumlah_lagu": 2,
      "total_durasi": "4 menit",
    },
  ]
  context = {
    "albums": albums,
  }
  return render(request, "label/list_album.html", context)

def label_album_detail(request, album_id):
    songs = [
    {
      "judul": "Lagu1",
      "durasi": "2 menit",
      "total_play": 3,
      "total_download": 0,
    },
    {
      "judul": "Lagu2",
      "durasi": "3 menit",
      "total_play": 2,
      "total_download": 2,
    },
  ]

    # Prepare context dictionary
    context = {
        "album_id": album_id,
        "songs": songs,
        
    }

    return render(request, "label/album_detail.html", context)

def artist_songwriter_report(request):
    album = [
    {
      "judul": "Album1",
      "label": "LabelA",
      "jumlah_lagu": 0,
      "total_durasi": 0,
    },
    {
      "judul": "Album2",
      "label": "LabelB",
      "jumlah_lagu": 2,
      "total_durasi": "4 menit",
    },
  ]
    labels = [
    {
      "name": "LabelA",
    },
    {
      "name": "LabelB",
    },
  ]

    # Prepare context dictionary
    context = {
        "albums": album,
        "labels": labels,
    }

    return render(request, 'artist_songwriter/list_album.html', context)

def artist_songwriter_album_detail(request, album_id):
    songs = [
    {
      "judul": "Lagu1",
      "durasi": "2 menit",
      "total_play": 3,
      "total_download": 0,
    },
    {
      "judul": "Lagu2",
      "durasi": "3 menit",
      "total_play": 2,
      "total_download": 2,
    },
  ]
    songwriters = [
    {
      "nama":"Abdul"
    },
    {
      "nama":"Usep"
    },
    {
      "nama":"Luigi"
    },
  ]
    genres = [
    {
      "nama":"chill"
    },
    {
      "nama":"dj jedag jedug"
    },
    {
      "nama":"oldies"
    },
  ]

    # Prepare context dictionary
    context = {
        "album_id": album_id,
        "songs": songs,
        "songwriters": songwriters,
        "genre": genres,
        
    }

    return render(request, 'artist_songwriter/album_detail.html', context)


