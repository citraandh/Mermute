import json
from datetime import datetime, timedelta
import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from psycopg2 import ProgrammingError

from utils.query import connect_to_db, execute_query


def email_exist(email):
    query = f"SELECT * FROM akun WHERE email = '{email}'"
    result = execute_query(query)
    return len(result) > 0


def set_premium(email, is_premium):
    if is_premium:
        query = f"INSERT INTO premium (email) VALUES ('{email}')"
    else:
        query = f"INSERT INTO nonpremium (email) VALUES ('{email}')"
    execute_query(query)


def remove_premium(email, is_premium):
    if is_premium:
        query = f"DELETE FROM premium WHERE email = '{email}'"
    else:
        query = f"DELETE FROM nonpremium WHERE email = '{email}'"
    execute_query(query)


def check_premium(email):
    # Cek apakah user adalah premium
    query = f"SELECT * FROM premium WHERE email = '{email}'"
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
    if request.method == 'POST':
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
        if request.session.get('actor') == 'pengguna':
            gender = request.POST.get('gender')
            tempat_lahir = request.POST.get('place_of_birth')
            tanggal_lahir = request.POST.get('date_of_birth')
            kota_asal = request.POST.get('city_origin')
            is_verified = False
            role = request.POST.get('role')

            id = (uuid.uuid4())
            phc_id = (uuid.uuid4())

        print('role', role)

        query_buat_akun = f"INSERT INTO akun(email, password, nama, gender, tempat_lahir, tanggal_lahir, kota_asal, is_verified) VALUES('{email}', '{password}', '{nama}', '{gender}', '{tempat_lahir}', '{tanggal_lahir}', '{kota_asal}', {is_verified})"
        execute_query(query_buat_akun)
        print(role)

         query = f"INSERT INTO pemilik_hak_cipta (id, rate_royalti) VALUES ('{phc_id}', '0')"
          execute_query(query)
           if role == 'artist':
                query = f"INSERT INTO artist (id, email_akun, id_pemilik_hak_cipta) VALUES ('{id}', '{email}', '{phc_id}')"
                execute_query(query)
            if role == 'label':
                query = f"INSERT INTO label (id, nama, email, password,  kontak, id_pemilik_hak_cipta) VALUES ('{id}', '{nama}', '{email}', '{password}', '{kontak}', '{phc_id}')"
                execute_query(query)
            if role == 'songwriter':
                query = f"INSERT INTO songwriter (id, email_akun, id_pemilik_hak_cipta) VALUES ('{id}', '{email}', '{phc_id}')"
                execute_query(query)
        if role == 'podcaster':
            query = f"INSERT INTO podcaster (email) VALUES ('{email}')"
            print('masuk podcaster')
            execute_query(query)

            # Cek apakah email sudah terdaftar
            if email_exist(email):
                return redirect('main:login')

            query = f"INSERT INTO akun (email, password, nama, gender, tempat_lahir, tanggal_lahir, kota_asal, is_verified) VALUES ('{email}', '{password}', '{nama}', '{gender}', '{tempat_lahir}', '{tanggal_lahir}', '{kota_asal}', {is_verified})"
            execute_query(query)
            set_premium(email, check_premium(email))
        elif request.session.get('actor') == 'label':
            kontak = request.POST.get('contact')
            query = f"INSERT INTO label (email, password, nama, kontak) VALUES ('{email}', '{password}', '{nama}', '{kontak}')"
            execute_query(query)

        return redirect('main:login')
    return render(request, 'register.html')


def dashboard(request):
    email = request.session.get('email')
    query = f"SELECT * FROM akun WHERE email = '{email}'"
    result = execute_query(query)
    pengguna_biasa = is_pengguna_biasa(request)
    artis = is_artist(request)
    label = is_label(request)
    songwriter = is_songwriter(request)
    podcaster = is_podcaster(request)

    # role is pengguna_biasa, artis, label, songwriter, podcaster concatenated with ','
    role = 'pengguna biasa, '
    if artis:
        role += 'artis, '
    if label:
        role += 'label, '
    if songwriter:
        role += 'songwriter, '
    if podcaster:
        role += 'podcaster'

    # remove comma at the end if exist
    if role[-2] == ',':
        role = role[:-2]

    context = {
        'data_user': result[0],
        'is_pengguna_biasa': pengguna_biasa,
        'is_artist': artis,
        'is_label': label,
        'is_songwriter': songwriter,
        'is_podcaster': podcaster,
        'role': role
    }
    print(context)
    print(role)
    return render(request, 'dashboard.html', context)


def is_pengguna_biasa(request):
    return True


def is_artist(request):
    email = request.session.get('email')
    query = f"SELECT * FROM artist WHERE email_akun = '{email}'"
    result = execute_query(query)
    return len(result) > 0


def is_label(request):
    email = request.session.get('email')
    query = f"SELECT * FROM label WHERE email = '{email}'"
    result = execute_query(query)
    return len(result) > 0


def is_songwriter(request):
    email = request.session.get('email')
    query = f"SELECT * FROM songwriter WHERE email_akun = '{email}'"
    result = execute_query(query)
    return len(result) > 0


def is_podcaster(request):
    email = request.session.get('email')
    query = f"SELECT * FROM podcaster WHERE email = '{email}'"
    result = execute_query(query)
    return len(result) > 0


def logout_user(request):
    request.session.flush()
    return redirect('main:landing_page')


def podcast_detail(request):
    podcast_id = request.GET.get('id')

    query = f"SELECT KONTEN.judul, AKUN.nama, KONTEN.durasi, KONTEN.tanggal_rilis, KONTEN.tahun FROM PODCAST JOIN KONTEN ON PODCAST.id_konten = KONTEN.id JOIN PODCASTER ON PODCAST.email_podcaster = PODCASTER.email JOIN AKUN ON PODCASTER.email = AKUN.email WHERE KONTEN.id = '{podcast_id}'"
    podcast = execute_query(query)
    print(podcast)
    podcast = podcast[0]

    query = f"SELECT E.judul, E.deskripsi, E.durasi, E.tanggal_rilis FROM EPISODE AS E JOIN KONTEN AS K ON E.id_konten_podcast = K.id WHERE K.id = '{podcast_id}'"
    episode = execute_query(query)

    query = f"SELECT G.genre FROM KONTEN AS K JOIN PODCAST AS P ON K.id = P.id_konten JOIN GENRE AS G ON K.id = G.id_konten WHERE K.id = '{podcast_id}'"
    genre = execute_query(query)

    context = {
        'podcast': podcast,
        'episodes': episode,
        'genres': genre
    }

    return render(request, 'podcast/podcast_page.html', context)


def podcast_manager(request):
    query = f"SELECT KONTEN.id, KONTEN.judul, AKUN.nama, KONTEN.durasi, KONTEN.tanggal_rilis, KONTEN.tahun, COUNT(E.id_konten_podcast) as episode_count FROM PODCAST JOIN KONTEN ON PODCAST.id_konten = KONTEN.id JOIN PODCASTER ON PODCAST.email_podcaster = PODCASTER.email JOIN AKUN ON PODCASTER.email = AKUN.email LEFT JOIN EPISODE AS E ON KONTEN.id = E.id_konten_podcast GROUP BY KONTEN.id, KONTEN.judul, AKUN.nama, KONTEN.durasi, KONTEN.tanggal_rilis, KONTEN.tahun"
    podcast = execute_query(query)

    query = f"SELECT K.id, E.judul, E.deskripsi, E.durasi, E.tanggal_rilis FROM EPISODE AS E JOIN KONTEN AS K ON E.id_konten_podcast = K.id"
    episode = execute_query(query)

    query = f"SELECT G.genre FROM KONTEN AS K JOIN PODCAST AS P ON K.id = P.id_konten JOIN GENRE AS G ON K.id = G.id_konten"
    genre = execute_query(query)

    id = request.GET.get('id')
    print(id)
    if id is not None:
        query = f"SELECT K.id, E.judul, E.deskripsi, E.durasi, E.tanggal_rilis FROM EPISODE AS E JOIN KONTEN AS K ON E.id_konten_podcast = K.id WHERE K.id = '{id}'"
        episode = execute_query(query)

        query = f"SELECT KONTEN.judul FROM PODCAST JOIN KONTEN ON PODCAST.id_konten = KONTEN.id WHERE KONTEN.id = '{id}'"
        podcast_selected = execute_query(query)

        context = {
            'podcasts': podcast,
            'episodes': episode,
            'genres': genre,
            'podcast_selected': podcast_selected[0]
        }
    else:
        context = {
            'podcasts': podcast,
            'episodes': episode,
            'genres': genre
        }
    print(episode)

    return render(request, 'podcast/podcast_manager.html', context)


def add_podcast(request):
    if request.method == 'POST':
        email = request.session.get('email')
        judul = request.POST.get('judul')
        tanggal_rilis = datetime.now()
        tahun = datetime.now().year
        genres = request.POST.get('genre')
        genres = genres.split(',')
        durasi = 0
        id = (uuid.uuid4())
        query = f"INSERT INTO KONTEN (id, judul, durasi, tanggal_rilis, tahun) VALUES ('{id}', '{judul}', '{durasi}', '{tanggal_rilis}', '{tahun}')"
        execute_query(query)
        query = f"INSERT INTO PODCAST (id_konten, email_podcaster) VALUES ('{id}', '{email}')"
        execute_query(query)
        for genre in genres:
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
        tanggal_rilis = datetime.now()
        tahun = datetime.now().year
        deskripsi = request.POST.get('deskripsi')
        id = (uuid.uuid4())
        query = f"INSERT INTO KONTEN (id, judul, durasi, tanggal_rilis, tahun) VALUES ('{id}', '{judul}', '{durasi}', '{tanggal_rilis}', '{tahun}')"
        execute_query(query)
        query = f"INSERT INTO EPISODE (id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis) VALUES ('{id}', '{podcast_id}', '{judul}', '{deskripsi}', '{durasi}', '{tanggal_rilis}')"
        execute_query(query)
        return redirect(reverse('main:podcast'))
    return render(request, 'podcast_manager.html')


def delete_podcast(request, podcast_id):
    if request.method == 'DELETE':
        query = f"DELETE FROM KONTEN WHERE id = '{podcast_id}'"
        execute_query(query)
        return redirect('main:podcast_manager')


def delete_episode(request, episode_id):
    print(request.method)
    print(episode_id)
    query = f"DELETE FROM EPISODE WHERE id_episode = '{episode_id}'"
    execute_query(query)
    return HttpResponseRedirect(reverse('main:podcast'))


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


@ csrf_exempt
def pembayaran(request, jenis_paket, harga):
    return render(request, 'langganan_paket/pembayaran.html', {'jenis': jenis_paket, 'harga': harga})


def beli_paket(request, jenis):
    return render(request, 'langganan_paket/pembayaran.html', {'jenis': jenis})


# # @login_required
def kelola_playlist(request):
    # Ambil email pengguna yang sedang login
    current_user_email = request.session.get('email')
    print(current_user_email)

    if not current_user_email:
        return HttpResponseNotAllowed("Login diperlukan")

    # Query SQL untuk mengambil playlist yang dibuat oleh pengguna yang sedang login
    query = f"SELECT id_playlist, judul, jumlah_lagu, total_durasi FROM USER_PLAYLIST WHERE email_pembuat = '{current_user_email}'"
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
    query = f"SELECT id_playlist, judul, jumlah_lagu, total_durasi FROM USER_PLAYLIST"
    results = execute_query(query)

    context = {
        'UserPlaylist': results
    }

    return render(request, 'kelola_playlist/daftar_playlist.html', context)


def user_playlist_detail(request, id_playlist):
    # Query untuk mengambil detail dari USER_PLAYLIST berdasarkan user_playlist_id
    playlist_detail = execute_query(
        "SELECT judul, email_pembuat, jumlah_lagu, total_durasi, tanggal_dibuat, deskripsi "
        "FROM USER_PLAYLIST "
        f"WHERE id_playlist = '{id_playlist}'"
    )

    # if not playlist_detail:
    #     return render(request, 'kelola_playlist/kelola_playlist_awal.html', {'error': 'Playlist tidak ditemukan'})

    # Query untuk mengambil nama pembuat playlist
    playlist_detail = playlist_detail[0]
    pembuat = execute_query(
        "SELECT nama "
        "FROM AKUN "
        f"WHERE email = '{playlist_detail['email_pembuat']}'"
    )[0]

    # Query untuk mengambil semua lagu yang ada di dalam USER_PLAYLIST
    songsid = execute_query(
        "SELECT id_song "
        "FROM PLAYLIST_SONG "
        f"WHERE id_playlist = '{id_playlist}'"
    )
    songs = []
    for song in songsid:
        song_detail = execute_query(
            "SELECT judul, durasi, nama "
            "FROM KONTEN "
            "JOIN SONG ON KONTEN.id = SONG.id_konten "
            "JOIN ARTIST ON SONG.id_artist = ARTIST.id "
            "JOIN AKUN ON ARTIST.email_akun = AKUN.email "
            f"WHERE KONTEN.id = '{song['id_song']}'"
        )[0]
        song_detail['id'] = song['id_song']
        songs.append(song_detail)

    # Siapkan context untuk render template
    context = {
        'playlist': playlist_detail,
        'pembuat': pembuat,
        'songs': songs
    }
    print(context)
    return render(request, 'kelola_playlist/kelola_playlist_detail.html', context)


@ csrf_exempt
def pembayaran_final(request):
    if request.method == 'POST':
        # email = 'user_verified_136@example.com'
        email = request.session.get('email')
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

        metode_bayar = request.POST.get('metode_bayar')
        print('metode_bayar', metode_bayar)
        nominal = request.POST.get('harga')
        id = (uuid.uuid4())
        query = f"INSERT INTO TRANSACTION (id, email, jenis_paket, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal) VALUES ('{id}', '{email}', '{jenis_paket}', '{timestamp_mulai}', '{timestamp_selesai}', '{metode_bayar}', {nominal})"
        execute_query(query)
        set_premium(email, True)
        # remove from non_premium
        remove_premium(email, False)
        return redirect('main:langganan_paket')

    return redirect('main:langganan_paket')


def riwayat_transaksi(request):
    # email = 'user_verified_136@example.com'
    email = request.session.get('email')
    query = f"SELECT * FROM TRANSACTION WHERE email = '{email}'"
    results = execute_query(query)
    context = {
        'transactions': results
    }
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
    if check_premium(request.session.get('email')):
        # email = 'user_verified_34@example.com'
        email = request.session.get('email')
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
    else:
        return redirect('main:bukan_premium')


def bukan_premium(request):
    return render(request, 'downloaded_song/bukan_premium.html')


def downloaded_song_delete(request, judul):
    try:
        query_delete = f"DELETE FROM DOWNLOADED_SONG WHERE id_song = (SELECT id FROM KONTEN WHERE judul = '{judul}')"
        execute_query(query_delete)
    except ProgrammingError as e:
        print(f"An error occurred: {e}")
    return redirect('main:downloaded_song')


def play_song(request, id_song):
    song = execute_query(
        "SELECT * "
        "FROM SONG "
        f"WHERE id_konten = '{id_song}'"
    )[0]
    konten = execute_query(
        "SELECT judul, durasi, tanggal_rilis, tahun "
        "FROM KONTEN "
        f"WHERE id = '{id_song}'"
    )[0]
    artist = execute_query(
        "SELECT nama "
        "FROM ARTIST "
        "JOIN AKUN ON ARTIST.email_akun = AKUN.email "
        f"WHERE id = '{song['id_artist']}'"
    )[0]
    album = execute_query(
        "SELECT judul "
        "FROM ALBUM "
        f"WHERE id = '{song['id_album']}'"
    )[0]
    genres = execute_query(
        "SELECT genre "
        "FROM GENRE "
        f"WHERE id_konten = '{id_song}'"
    )
    songwriters = execute_query(
        "SELECT nama "
        "FROM SONGWRITER S "
        "JOIN AKUN A ON S.email_akun = A.email "
        "JOIN SONGWRITER_WRITE_SONG SS ON SS.id_songwriter = S.id "
        f"WHERE SS.id_song = '{id_song}'"
    )
    context = {
        'song': song,
        'konten': konten,
        'artist': artist,
        'album': album,
        'genres': [genre['genre'] for genre in genres],
        'songwriters': [songwriter['nama'] for songwriter in songwriters]
    }
    print(context)
    return render(request, "play_song/play_song.html", context)
