import json
from datetime import datetime, timedelta
import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from psycopg2 import ProgrammingError

from utils.query import connect_to_db, execute_query


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
        query = f"INSERT INTO pemilik_hak_cipta (id, rate_royalti) VALUES ('{phc_id}', '0')"
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
    podcast = podcast[0]

    query = f"SELECT E.judul, E.deskripsi, E.durasi, E.tanggal_rilis FROM EPISODE AS E JOIN KONTEN AS K ON E.id_konten_podcast = K.id WHERE K.id = '{podcast_id}'"
    # Execute the query
    episode = execute_query(query)

    query = f"SELECT G.genre FROM KONTEN AS K JOIN PODCAST AS P ON K.id = P.id_konten JOIN GENRE AS G ON K.id = G.id_konten WHERE K.id = '{podcast_id}'"
    genre = execute_query(query)

    # # Prepare context dictionary with query results
    context = {
        'podcast': podcast,
        'episodes': episode,
        'genres': genre
    }

    return render(request, 'podcast/podcast_page.html', context=context)

def podcast_manager(request):
    query = f"SELECT KONTEN.id, KONTEN.judul, AKUN.nama, KONTEN.durasi, KONTEN.tanggal_rilis, KONTEN.tahun, COUNT(E.id) as episode_count FROM PODCAST JOIN KONTEN ON PODCAST.id_konten = KONTEN.id JOIN PODCASTER ON PODCAST.email_podcaster = PODCASTER.email JOIN AKUN ON PODCASTER.email = AKUN.email LEFT JOIN EPISODE AS E ON KONTEN.id = E.id_konten_podcast GROUP BY KONTEN.id, KONTEN.judul, AKUN.nama, KONTEN.durasi, KONTEN.tanggal_rilis, KONTEN.tahun"
    podcast = execute_query(query)

    query = f"SELECT E.judul, E.deskripsi, E.durasi, E.tanggal_rilis FROM EPISODE AS E JOIN KONTEN AS K ON E.id_konten_podcast = K.id"
    episode = execute_query(query)

    context = {
        'podcasts': podcast,
        'episodes': episode
    }
    return render(request, 'podcast/podcast_manager.html', context)

def add_podcast(request):
    if request.method == 'POST':
        email = request.session.get('email')
        judul = request.POST.get('judul')
        durasi = request.POST.get('durasi')
        tanggal_rilis = request.POST.get('tanggal_rilis')
        tahun = request.POST.get('tahun')
        deskripsi = request.POST.get('deskripsi')
        genre = request.POST.get('genre')
        id = (uuid.uuid4())
        query = f"INSERT INTO KONTEN (id, judul, durasi, tanggal_rilis, tahun) VALUES ('{id}', '{judul}', '{durasi}', '{tanggal_rilis}', '{tahun}')"
        execute_query(query)
        query = f"INSERT INTO PODCAST (id_konten, email_podcaster) VALUES ('{id}', '{email}')"
        execute_query(query)
        query = f"INSERT INTO GENRE (id_konten, genre) VALUES ('{id}', '{genre}')"
        execute_query(query)
        query = f"INSERT INTO PODCASTER (email) VALUES ('{email}')"
        execute_query(query)
        return redirect('main:podcast_manager')
    return render(request, 'podcast_manager.html')

def add_episode(request, podcast_id):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        durasi = request.POST.get('durasi')
        tanggal_rilis = request.POST.get('tanggal_rilis')
        deskripsi = request.POST.get('deskripsi')
        query = f"INSERT INTO KONTEN (id, judul, durasi, tanggal_rilis) VALUES ('{podcast_id}', '{judul}', '{durasi}', '{tanggal_rilis}')"
        execute_query(query)
        query = f"INSERT INTO EPISODE (id_konten_podcast) VALUES ('{podcast_id}')"
        execute_query(query)
        return redirect('main:podcast_manager')
    return render(request, 'podcast_manager.html')

def delete_podcast(request, podcast_id):
    if request.method == 'DELETE':
        query = f"DELETE FROM KONTEN WHERE id = '{podcast_id}'"
        execute_query(query)
        return redirect('main:podcast_manager')

def delete_episode(request, episode_id):
    if request.method == 'DELETE':
        query = f"DELETE FROM KONTEN WHERE id = '{episode_id}'"
        execute_query(query)
        return redirect('main:podcast_manager')
    
def list_podcast_ajax(request):
    query = "SELECT * FROM PODCAST"
    podcasts = execute_query(query)
    return JsonResponse({'podcasts': podcasts})

def list_episode_ajax(request, podcast_id):
    query = f"SELECT * FROM EPISODE WHERE id_konten_podcast = '{podcast_id}'"
    episodes = execute_query(query)
    return JsonResponse({'episodes': episodes})


def chart_list(request):
    query = "SELECT * FROM CHART"
    # Execute the query
    chart = execute_query(query)

    # Prepare context dictionary with query results
    context = {
        'charts': chart
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
    return render(request, 'kelola_playlist/kelola_playlist_awal.html')


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
        # Ambil detail pertama dari hasil query
        'UserPlaylist': playlist_detail[0],
        'Songs': songs
    }
    return render(request, 'kelola_playlist/kelola_playlist_detail.html', context)


@csrf_exempt
def pembayaran_final(request):
    if request.method == 'POST':
        # email = request.session.get('email')
        email = 'user_verified_136@example.com'
        jenis_paket = request.POST.get('jenis')
        timestamp_mulai = datetime.now()
        timestamp_selesai = timestamp_mulai

        if jenis_paket == '1 bulan':
            timestamp_selesai = timestamp_mulai + timedelta(days=30)
        elif jenis_paket == '3 bulan':
            timestamp_selesai = timestamp_mulai + timedelta(days=90)
        elif jenis_paket == '6 bulan':
            timestamp_selesai = timestamp_mulai + timedelta(days=180)
        elif jenis_paket == '1 tahun':
            timestamp_selesai = timestamp_mulai + timedelta(days=365)

        metode_bayar = request.POST.get('metode_pembayaran')
        nominal = request.POST.get('harga')
        id = (uuid.uuid4())
        query = f"INSERT INTO TRANSACTION (id, email, jenis_paket, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal) VALUES ('{id}', '{email}', '{jenis_paket}', '{timestamp_mulai}', '{timestamp_selesai}', '{metode_bayar}', {nominal})"
        execute_query(query)
        set_premium(email, True)
        return redirect('langganan_paket/langganan_paket.html')

    return render(request, 'langganan_paket/pembayaran.html')


def riwayat_transaksi(request):
    email = 'user_verified_136@example.com'
    query = f"SELECT * FROM TRANSACTION WHERE email = '{email}'"
    results = execute_query(query)
    context = {
        'transactions': results
    }
    print('masuk sini')
    print(context)
    return render(request, 'langganan_paket/riwayat_transaksi.html', context)


def search_bar(request):
    return render(request, 'search_bar/search_bar.html')


def search(request):
    # Convert search query to lowercase
    search_query = request.GET.get('query', '').lower()
    results = []
    if search_query:
        # Use LOWER function to make the SQL query case-insensitive
        query = f"SELECT KONTEN.judul, AKUN.nama, CASE WHEN SONG.id_konten IS NOT NULL THEN 'song' WHEN PODCAST.id_konten IS NOT NULL THEN 'podcast' WHEN USER_PLAYLIST.id_user_playlist IS NOT NULL THEN 'user playlist' END AS TIPE FROM KONTEN LEFT JOIN SONG ON KONTEN.id = SONG.id_konten LEFT JOIN PODCAST ON KONTEN.id = PODCAST.id_konten LEFT JOIN USER_PLAYLIST ON KONTEN.id = USER_PLAYLIST.id_playlist JOIN ARTIST ON SONG.id_artist = ARTIST.id JOIN AKUN ON ARTIST.email_akun = AKUN.email WHERE (SONG.id_konten IS NOT NULL OR PODCAST.id_konten IS NOT NULL OR USER_PLAYLIST.id_user_playlist IS NOT NULL) AND LOWER(KONTEN.judul) LIKE '%{search_query}%'"
        # Execute the query with case-insensitive search
        results = execute_query(query)
    return render(request, 'search_bar/search_bar.html', {'results': results})


def detail_konten(request, judul, nama, tipe):

    # from konten table, get judul, tanggal_rilis, tahun, and durasi
    query = f"SELECT judul, tanggal_rilis, tahun, durasi FROM KONTEN WHERE judul = '{judul}'"
    konten = execute_query(query)

    context = {'konten': konten, 'judul': judul, 'nama': nama, 'tipe': tipe}
    return render(request, 'search_bar/detail_konten.html', context)


def downloaded_song(request):
    email = 'user_verified_34@example.com'
    # asumsi: dapatkan data dari akun_play_song untuk tanggal_download_lagu
    query = f"""SELECT 
                    KONTEN.judul AS judul_lagu,
                    AKUN.nama AS nama_artis,
                    MAX(akun_play_song.waktu) AS tanggal_download_lagu
                FROM DOWNLOADED_SONG
                JOIN SONG ON DOWNLOADED_SONG.id_song = SONG.id_konten
                JOIN KONTEN ON SONG.id_konten = KONTEN.id
                JOIN ARTIST ON SONG.id_artist = ARTIST.id
                JOIN AKUN ON ARTIST.email_akun = AKUN.email
                LEFT JOIN akun_play_song ON DOWNLOADED_SONG.id_song = akun_play_song.id_song
                WHERE DOWNLOADED_SONG.email_downloader = '{email}'
                GROUP BY KONTEN.judul, AKUN.nama;
            """
    results = execute_query(query)
    context = {
        'downloaded_songs': results
    }
    return render(request, 'downloaded_song/downloaded_song.html', context)


def downloaded_song_delete(request, judul):
    print(judul)
    try:
        query_delete = f"DELETE FROM DOWNLOADED_SONG WHERE id_song = (SELECT id FROM KONTEN WHERE judul = '{judul}')"
        execute_query(query_delete)
    except ProgrammingError as e:
        print(f"An error occurred: {e}")
    return redirect('main:downloaded_song')
