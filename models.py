# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Akun(models.Model):
    email = models.CharField(primary_key=True, max_length=50)
    password = models.CharField(max_length=50)
    nama = models.CharField(max_length=100)
    gender = models.IntegerField()
    tempat_lahir = models.CharField(max_length=50)
    tanggal_lahir = models.DateField()
    is_verified = models.BooleanField()
    kota_asal = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'akun'


class AkunPlaySong(models.Model):
    email_pemain = models.OneToOneField(Akun, models.DO_NOTHING, db_column='email_pemain', primary_key=True)  # The composite primary key (email_pemain, id_song, waktu) found, that is not supported. The first column is selected.
    id_song = models.ForeignKey('Song', models.DO_NOTHING, db_column='id_song')
    waktu = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'akun_play_song'
        unique_together = (('email_pemain', 'id_song', 'waktu'),)


class AkunPlayUserPlaylist(models.Model):
    email_pemain = models.OneToOneField(Akun, models.DO_NOTHING, db_column='email_pemain', primary_key=True)  # The composite primary key (email_pemain, id_user_playlist, email_pembuat, waktu) found, that is not supported. The first column is selected.
    id_user_playlist = models.ForeignKey('UserPlaylist', models.DO_NOTHING, db_column='id_user_playlist', to_field='id_user_playlist')
    email_pembuat = models.CharField(max_length=50)
    waktu = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'akun_play_user_playlist'
        unique_together = (('email_pemain', 'id_user_playlist', 'email_pembuat', 'waktu'),)


class Album(models.Model):
    id = models.UUIDField(primary_key=True)
    judul = models.CharField(max_length=100)
    jumlah_lagu = models.IntegerField()
    id_label = models.UUIDField(blank=True, null=True)
    total_durasi = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'album'


class Artist(models.Model):
    id = models.UUIDField(primary_key=True)
    email_akun = models.ForeignKey(Akun, models.DO_NOTHING, db_column='email_akun', blank=True, null=True)
    id_pemilik_hak_cipta = models.ForeignKey('PemilikHakCipta', models.DO_NOTHING, db_column='id_pemilik_hak_cipta', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artist'


class Chart(models.Model):
    tipe = models.CharField(primary_key=True, max_length=50)
    id_playlist = models.ForeignKey('Playlist', models.DO_NOTHING, db_column='id_playlist', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chart'


class DownloadedSong(models.Model):
    id_song = models.OneToOneField('Song', models.DO_NOTHING, db_column='id_song', primary_key=True)  # The composite primary key (id_song, email_downloader) found, that is not supported. The first column is selected.
    email_downloader = models.ForeignKey('Premium', models.DO_NOTHING, db_column='email_downloader')

    class Meta:
        managed = False
        db_table = 'downloaded_song'
        unique_together = (('id_song', 'email_downloader'),)


class Episode(models.Model):
    id_episode = models.UUIDField(primary_key=True)
    id_konten_podcast = models.ForeignKey('Podcast', models.DO_NOTHING, db_column='id_konten_podcast', blank=True, null=True)
    judul = models.CharField(max_length=100)
    deskripsi = models.CharField(max_length=500)
    durasi = models.IntegerField()
    tanggal_rilis = models.DateField()

    class Meta:
        managed = False
        db_table = 'episode'


class Genre(models.Model):
    id_konten = models.OneToOneField('Konten', models.DO_NOTHING, db_column='id_konten', primary_key=True)  # The composite primary key (id_konten, genre) found, that is not supported. The first column is selected.
    genre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'genre'
        unique_together = (('id_konten', 'genre'),)


class Konten(models.Model):
    id = models.UUIDField(primary_key=True)
    judul = models.CharField(max_length=100)
    tanggal_rilis = models.DateField()
    tahun = models.IntegerField()
    durasi = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'konten'


class Label(models.Model):
    id = models.UUIDField(primary_key=True)
    nama = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    kontak = models.CharField(max_length=50)
    id_pemilik_hak_cipta = models.ForeignKey('PemilikHakCipta', models.DO_NOTHING, db_column='id_pemilik_hak_cipta', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'label'


class Nonpremium(models.Model):
    email = models.OneToOneField(Akun, models.DO_NOTHING, db_column='email', primary_key=True)

    class Meta:
        managed = False
        db_table = 'nonpremium'


class Paket(models.Model):
    jenis = models.CharField(primary_key=True, max_length=50)
    harga = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'paket'


class PemilikHakCipta(models.Model):
    id = models.UUIDField(primary_key=True)
    rate_royalti = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pemilik_hak_cipta'


class Playlist(models.Model):
    id = models.UUIDField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'playlist'


class PlaylistSong(models.Model):
    id_playlist = models.OneToOneField(Playlist, models.DO_NOTHING, db_column='id_playlist', primary_key=True)  # The composite primary key (id_playlist, id_song) found, that is not supported. The first column is selected.
    id_song = models.ForeignKey('Song', models.DO_NOTHING, db_column='id_song')

    class Meta:
        managed = False
        db_table = 'playlist_song'
        unique_together = (('id_playlist', 'id_song'),)


class Podcast(models.Model):
    id_konten = models.OneToOneField(Konten, models.DO_NOTHING, db_column='id_konten', primary_key=True)
    email_podcaster = models.ForeignKey('Podcaster', models.DO_NOTHING, db_column='email_podcaster', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'podcast'


class Podcaster(models.Model):
    email = models.OneToOneField(Akun, models.DO_NOTHING, db_column='email', primary_key=True)

    class Meta:
        managed = False
        db_table = 'podcaster'


class Premium(models.Model):
    email = models.OneToOneField(Akun, models.DO_NOTHING, db_column='email', primary_key=True)

    class Meta:
        managed = False
        db_table = 'premium'


class Royalti(models.Model):
    id_pemilik_hak_cipta = models.OneToOneField(PemilikHakCipta, models.DO_NOTHING, db_column='id_pemilik_hak_cipta', primary_key=True)  # The composite primary key (id_pemilik_hak_cipta, id_song) found, that is not supported. The first column is selected.
    id_song = models.ForeignKey('Song', models.DO_NOTHING, db_column='id_song')
    jumlah = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'royalti'
        unique_together = (('id_pemilik_hak_cipta', 'id_song'),)


class Song(models.Model):
    id_konten = models.OneToOneField(Konten, models.DO_NOTHING, db_column='id_konten', primary_key=True)
    id_artist = models.ForeignKey(Artist, models.DO_NOTHING, db_column='id_artist', blank=True, null=True)
    id_album = models.UUIDField(blank=True, null=True)
    total_play = models.IntegerField()
    total_download = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'song'


class Songwriter(models.Model):
    id = models.UUIDField(primary_key=True)
    email_akun = models.ForeignKey(Akun, models.DO_NOTHING, db_column='email_akun', blank=True, null=True)
    id_pemilik_hak_cipta = models.ForeignKey(PemilikHakCipta, models.DO_NOTHING, db_column='id_pemilik_hak_cipta', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'songwriter'


class SongwriterWriteSong(models.Model):
    id_songwriter = models.OneToOneField(Songwriter, models.DO_NOTHING, db_column='id_songwriter', primary_key=True)  # The composite primary key (id_songwriter, id_song) found, that is not supported. The first column is selected.
    id_song = models.ForeignKey(Song, models.DO_NOTHING, db_column='id_song')

    class Meta:
        managed = False
        db_table = 'songwriter_write_song'
        unique_together = (('id_songwriter', 'id_song'),)


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True)  # The composite primary key (id, jenis_paket, email) found, that is not supported. The first column is selected.
    jenis_paket = models.ForeignKey(Paket, models.DO_NOTHING, db_column='jenis_paket')
    email = models.ForeignKey(Akun, models.DO_NOTHING, db_column='email')
    timestamp_dimulai = models.DateTimeField()
    timestamp_berakhir = models.DateTimeField()
    metode_bayar = models.CharField(max_length=50)
    nominal = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'transaction'
        unique_together = (('id', 'jenis_paket', 'email'),)


class UserPlaylist(models.Model):
    email_pembuat = models.OneToOneField(Akun, models.DO_NOTHING, db_column='email_pembuat', primary_key=True)  # The composite primary key (email_pembuat, id_user_playlist) found, that is not supported. The first column is selected.
    id_user_playlist = models.UUIDField()
    judul = models.CharField(max_length=100)
    deskripsi = models.CharField(max_length=500)
    jumlah_lagu = models.IntegerField()
    tanggal_dibuat = models.DateField()
    id_playlist = models.ForeignKey(Playlist, models.DO_NOTHING, db_column='id_playlist', blank=True, null=True)
    total_durasi = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_playlist'
        unique_together = (('email_pembuat', 'id_user_playlist'),)
