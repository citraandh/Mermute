from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('dashboard/', dashboard, name='dashboard'),
    # path('konten/', konten, name='konten'),
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    # Langganan Paket
    path('langganan_paket/', langganan_paket, name='langganan_paket'),
    path('pembayaran/<str:jenis_paket>/<int:harga>/',
         pembayaran, name='pembayaran'),
    path('pembayaran_final/', pembayaran_final, name='pembayaran_final'),
    path('podcast/detail/<uuid:podcast_id>',
         podcast_detail, name='podcast_page'),
    path('chart/', chart_list, name='chart'),

]
