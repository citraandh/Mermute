import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from utils.query import *
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import uuid
from utils.query import connect_to_db, execute_query
from .models import *
from django.http import HttpResponseRedirect

def email_exist(email):
    query = f"SELECT * FROM akun WHERE email = '{email}'"
    result = execute_query(query)
    return len(result) > 0


def set_premium(email, is_premium):
    if is_premium:
        query = f'INSERT INTO premium (email) VALUES ("{email}")'
    else:
        query = f'DELETE FROM premium WHERE email = "{email}"'
        execute_query(query)
        query = f'INSERT INTO nonpremium (email) VALUES ("{email}")'
    execute_query(query)


def check_premium(user):
    # Cek apakah user adalah premium
    query = f"SELECT * FROM premium WHERE email = '{user.email}'"
    result = execute_query(query)
    return len(result) > 0


def dashboard(request):
    return render(request, 'dashboard.html')


def konten(request):
    return render(request, 'konten.html')


def landing_page(request):
    return render(request, 'landing_page.html')


@csrf_exempt
def login_user(request):
    print(request)
    if request.method == 'POST':
        print("masuk sini")
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Cek apakah email dan password sesuai

        query = f"SELECT * FROM akun WHERE email = '{email}' AND password = '{password}'"
        result = execute_query(query)
        email = result[0]['email']
        nama = result[0]['nama']
        is_verified = result[0]['is_verified']
        request.session['email'] = email
        request.session['nama'] = nama
        request.session['is_verified'] = is_verified

        print(request.session.get('email', None))
        ctr = 0
        role = None
        while len(result) != 0:
            if ctr == 3:
                break
            ctr += 1
            artist = f"SELECT * FROM artist WHERE artist.email_akun = '{email}'"
            artist = execute_query(artist)
            if len(artist) > 0:
                role = 'artist'
                break
            label = f"SELECT * FROM label WHERE label.email = '{email}'"
            label = execute_query(label)
            if len(label) > 0:
                role = 'label'
                break
            songwriter = f"SELECT * FROM songwriter WHERE songwriter.email_akun = '{email}'"
            songwriter = execute_query(songwriter)
            if len(songwriter) > 0:
                role = 'songwriter'
                break
        print(role)
        request.session['role'] = role

        response = HttpResponseRedirect(reverse("main:dashboard"))
        return response
    return render(request, 'login.html', {})


@csrf_exempt
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('name')
        gender = request.POST.get('gender')
        tempat_lahir = request.POST.get('place_of_birth')
        tanggal_lahir = request.POST.get('date_of_birth')
        kota_asal = request.POST.get('city_origin')
        is_verified = False
        role = request.POST.get('role')
        kontak = request.POST.get('contact')

        id = (uuid.uuid4())
        phc_id = (uuid.uuid4())
        query = f"INSERT INTO pemilik_hak_cipta (id, email) VALUES ('{phc_id}', '{email}')"
        execute_query(query)
        if request.session.get('role') == 'artist':
            query = f"INSERT INTO artist (id, email_akun, id_pemilik_hak_cipta) VALUES ('{id}', '{email}', '{phc_id}')"
            execute_query(query)
        if request.session.get('role') == 'label':
            query = f"INSERT INTO label (id, nama, email, password,  kontak, id_pemilik_hak_cipta) VALUES ('{id}', '{nama}', '{email}', '{password}', '{kontak}', '{phc_id}')"
            execute_query(query)
        if request.session.get('role') == 'songwriter':
            query = f"INSERT INTO songwriter (id, email_akun, id_pemilik_hak_cipta) VALUES ('{id}', '{email}', '{phc_id}')"
            execute_query(query)

        # Cek apakah email sudah terdaftar
        if email_exist(email):
            return redirect('main:login')

        # Register user
        print(email, password, nama, gender, tempat_lahir,
              tanggal_lahir, kota_asal, is_verified)
        query = f"INSERT INTO akun (email, password, nama, gender, tempat_lahir, tanggal_lahir, kota_asal, is_verified) VALUES ('{email}', '{password}', '{nama}', '{gender}', '{tempat_lahir}', '{tanggal_lahir}', '{kota_asal}', {is_verified})"
        print(query)
        execute_query(query)
        set_premium(email, False)
        return redirect('main:login')
    return render(request, 'register.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def podcast_detail(request, podcast_id):
    query = f"SELECT KONTEN.judul, AKUN.nama, KONTEN.durasi, KONTEN.tanggal_rilis, KONTEN.tahun FROM PODCAST JOIN KONTEN ON PODCAST.id_konten = KONTEN.id JOIN PODCASTER ON PODCAST.email_podcaster = PODCASTER.email JOIN AKUN ON PODCASTER.email = AKUN.email WHERE KONTEN.id = '{podcast_id}'"
    # Execute the query
    podcast = execute_query(query)

    query = f"SELECT EPISODE.judul, EPISODE.deskripsi, EPISODE.durasi, EPISODE.tanggal_rilis FROM EPISODE JOIN PODCAST ON EPISODE.id_konten_podcast = PODCAST.id_konten JOIN KONTEN ON PODCAST.id_konten = KONTEN.id WHERE KONTEN.judul = 'Podcast1'"
    # Execute the query
    episode = execute_query(query)

    query = f'SELECT genre FROM genre WHERE id_konten = {podcast_id}'
    genre = execute_query(query)

    # # Prepare context dictionary with query results
    context = {
        'podcast': podcast,
        'episode': episode,
        'genre': genre
    }

    return render(request, 'podcast/podcast_page.html', context=context)


def chart_list(request):
    query = "SELECT * FROM CHART"
    # Execute the query
    chart = execute_query(query)

    # Prepare context dictionary with query results
    context = {
        'charta': chart
    }

    return render(request, 'chart/chart.html', context)


def chart_detail(request, chart_id):
    query = f"SELECT * FROM CHART WHERE id = {chart_id}"
    # Execute the query
    chart = execute_query(query)

    query = f"SELECT KONTEN.judul, KONTEN.durasi, KONTEN.tanggal_rilis, KONTEN.tahun FROM KONTEN JOIN CHART ON KONTEN.id = CHART.id_konten WHERE CHART.id = {chart_id}"
    # Execute the query
    konten = execute_query(query)

    # Prepare context dictionary with query results
    context = {
        'chart': chart,
        'konten': konten
    }

    return render(request, 'chart/chart_detail.html', context)


def langganan_paket(request):
    query = "SELECT * FROM paket"
    paket = execute_query(query)
    context = {
        'paket': paket
    }

    return render(request, 'langganan_paket/langganan_paket.html', context)


@csrf_exempt
def pembayaran(request, jenis_paket, harga):
    return render(request, 'langganan_paket/pembayaran.html', {'jenis': jenis_paket, 'harga': harga})


def beli_paket(request, jenis):
    return render(request, 'langganan_paket/pembayaran.html', {'jenis': jenis})
# def list_podcast(request):
#   if try_connect() != False:
#     query = "SELECT * FROM podcast"
#     podcasts = execute_query(query)
#     context = {
#       'podcasts': podcasts
#     }
#     return render(request, 'podcast_manager.html', context)
  


# # @login_required
def kelola_playlist(request):
    # Ambil email pengguna yang sedang login
    current_user_email = request.user.email

    # Query SQL untuk mengambil playlist yang dibuat oleh pengguna yang sedang login
    query = f"SELECT judul, jumlah_lagu, total_durasi FROM USER_PLAYLIST WHERE email_pembuat = '{current_user_email}'"
    results = execute_query(query)

    # Cek apakah pengguna telah membuat playlist atau belum
    if results:
        context = {
            'UserPlaylist': results
        }
        return render(request, 'kelola_playlist/daftar_playlist.html', context)
    else:
        return render(request, 'kelola_playlist/kelola_playlist_awal.html')

  
def playlist_awal(request):
  return render (request, 'kelola_playlist/kelola_playlist_awal.html' )

def daftar_playlist(request):
  query = 'SELECT USER_PLAYLIST.judul, USER_PLAYLIST.jumlah_lagu, USER_PLAYLIST.total_durasi FROM USER_PLAYLIST;'
  
  results = execute_query(query)
  
  context = {
    'UserPlaylist': results
  }
  
  return render(request, 'kelola_playlist/daftar_playlist.html', context)

def user_playlist_detail(request):
    # Query untuk mengambil detail dari USER_PLAYLIST berdasarkan user_playlist_id
    query_playlist = f"""
        SELECT judul, email_pembuat, jumlah_lagu, total_durasi, tanggal_dibuat, deskripsi
        FROM USER_PLAYLIST
    """
    playlist_detail = execute_query(query_playlist)

    if not playlist_detail:
        return render(request, 'kelola_playlist/kelola_playlist_awal.html', {'error': 'Playlist tidak ditemukan'})

    # Query untuk mengambil semua lagu yang ada di dalam USER_PLAYLIST
    query_songs = f"""
        SELECT KONTEN.judul, KONTEN.durasi
        FROM SONG
        JOIN KONTEN ON SONG.id_konten = KONTEN.id_konten
    """
    songs = execute_query(query_songs)

    # Siapkan context untuk render template
    context = {
        'UserPlaylist': playlist_detail[0],  # Ambil detail pertama dari hasil query
        'Songs': songs
    }
    return render(request, 'kelola_playlist/kelola_playlist_detail.html', context)

# def user_playlist_detail (request):
#   query = 'SELECT * FROM USER_PLAYLIST'
#   results = execute_query(query)
#   context = {
#     'UserPlaylist': results
#   }
#   return render(request, 'kelola_playlist/kelola_playlist_detail.html', context)


# # @login_required
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

# # @login_required
def play_song(request, song_id):
    song = Song.objects.get(id_konten=song_id)
    genres = song.genre_set.all()  # Asumsikan 'Song' memiliki relation ke model 'Genre'
    context = {
        'song': song,
        'genres': genres,
        'is_premium': request.user.is_premium  # Asumsikan Akun memiliki atribut is_premium
    }
    return render(request, 'play_song.html', context) 
# # @login_required
def shuffle_play(request, user_playlist_id):
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
# # @login_required
# RAGU NIH
def add_song_to_playlist(request, playlist_id):
    if request.method == 'POST':
        song_id = request.POST.get('song_id')
        query = f"INSERT INTO PLAYLIST_SONG (id_user_playlist, id_song) VALUES ('{playlist_id}', '{song_id}')"
        try:
          execute_query(query)
          return JsonResponse({'status': 'success', 'message': 'Song added to playlist successfully'})
        except Exception as e:
          return JsonResponse({'status': 'error', 'message': str(e)})

    # Jika GET, tampilkan form untuk menambahkan lagu ke playlist
    playlists = Playlist.objects.filter(email_pembuat=request.user.email)
    context = {
        'playlists': playlists,
        'song': Song.objects.get(id_konten=song_id)
    }
    return render(request, 'add_song_to_playlist.html', context)

# # Silakan tambahkan logic lainnya sesuai dengan kebutuhan aplikasi
# def royalty_report(request):
#   # Sample data for 5 rows
#   royalty_data = [
#     {
#       "judul_lagu": "Lagu 1",
#       "judul_album": "Album 1",
#       "total_play": 3,
#       "total_download": 0,
#       "total_royalti": 450000,
#     },
#     {
#       "judul_lagu": "Lagu 2",
#       "judul_album": "Album 2",
#       "total_play": 2,
#       "total_download": 2,
#       "total_royalti": 520000,
#     },
#     # Add 3 more rows with your data
#   ]

#   # Create the context dictionary
#   context = {
#     "royalty_data": royalty_data,
#   }

#   # Render the HTML template with the context
#   return render(request, "royalti/list_royalti.html", context)

# def label_report(request):
#   # Replace this with your logic to fetch album data
#   albums = [
#     {
#       "judul": "Album1",
#       "jumlah_lagu": 0,
#       "total_durasi": "0 menit",
#     },
#     {
#       "judul": "Album2",
#       "jumlah_lagu": 2,
#       "total_durasi": "4 menit",
#     },
#   ]
#   context = {
#     "albums": albums,
#   }
#   return render(request, "label/list_album.html", context)

# def label_album_detail(request, album_id):
#     songs = [
#     {
#       "judul": "Lagu1",
#       "durasi": "2 menit",
#       "total_play": 3,
#       "total_download": 0,
#     },
#     {
#       "judul": "Lagu2",
#       "durasi": "3 menit",
#       "total_play": 2,
#       "total_download": 2,
#     },
#   ]

#     # Prepare context dictionary
#     context = {
#         "album_id": album_id,
#         "songs": songs,
        
#     }

#     return render(request, "label/album_detail.html", context)

# def artist_songwriter_report(request):
#     album = [
#     {
#       "judul": "Album1",
#       "label": "LabelA",
#       "jumlah_lagu": 0,
#       "total_durasi": 0,
#     },
#     {
#       "judul": "Album2",
#       "label": "LabelB",
#       "jumlah_lagu": 2,
#       "total_durasi": "4 menit",
#     },
#   ]
#     labels = [
#     {
#       "name": "LabelA",
#     },
#     {
#       "name": "LabelB",
#     },
#   ]

#     # Prepare context dictionary
#     context = {
#         "albums": album,
#         "labels": labels,
#     }

#     return render(request, 'artist_songwriter/list_album.html', context)

# def artist_songwriter_album_detail(request, album_id):
#     songs = [
#     {
#       "judul": "Lagu1",
#       "durasi": "2 menit",
#       "total_play": 3,
#       "total_download": 0,
#     },
#     {
#       "judul": "Lagu2",
#       "durasi": "3 menit",
#       "total_play": 2,
#       "total_download": 2,
#     },
#   ]
#     songwriters = [
#     {
#       "nama":"Abdul"
#     },
#     {
#       "nama":"Usep"
#     },
#     {
#       "nama":"Luigi"
#     },
#   ]
#     genres = [
#     {
#       "nama":"chill"
#     },
#     {
#       "nama":"dj jedag jedug"
#     },
#     {
#       "nama":"oldies"
#     },
#   ]

#     # Prepare context dictionary
#     context = {
#         "album_id": album_id,
#         "songs": songs,
#         "songwriters": songwriters,
#         "genre": genres,
        
#     }

#     return render(request, 'artist_songwriter/album_detail.html', context)



@csrf_exempt
def pembayaran_final(request):
    if request.method == 'POST':
        email = request.session.get('email')
        jenis_paket = request.POST.get('jenis_paket')
        timestamp_mulai = datetime.now()
        timestamp_selesai = timestamp_mulai  # Initialize with a default value

        if jenis_paket == '1 bulan':
            timestamp_selesai = timestamp_mulai + timedelta(days=30)
        elif jenis_paket == '3 bulan':
            timestamp_selesai = timestamp_mulai + timedelta(days=90)
        elif jenis_paket == '6 bulan':
            timestamp_selesai = timestamp_mulai + timedelta(days=180)
        elif jenis_paket == '1 tahun':
            timestamp_selesai = timestamp_mulai + timedelta(days=365)

        metode_bayar = request.POST.get('metode_bayar')
        nominal = request.POST.get('harga')
        id = (uuid.uuid4())
        query = f"INSERT INTO TRANSACTION (id, email, jenis_paket, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal) VALUES ('{id}', '{email}', '{jenis_paket}', '{timestamp_mulai}', '{timestamp_selesai}', '{metode_bayar}', {nominal})"
        execute_query(query)
        set_premium(email, True)
        return redirect('main:dashboard')
