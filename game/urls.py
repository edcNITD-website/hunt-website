from django.urls import path,include
from game.views import *


app_name = 'game'
urlpatterns = [
    path('profile/',profile,name='profile'),
    path('register/',register,name='register'),
    path('scanner/',scanner,name='scanner'),
    path('manage_qr/',manage_qr,name='manage_qr'),
    path('add_qr/',add_qr,name='add_qr'),
    path('delete_qr/<int:qr_id>',delete_qr,name='delete_qr'),
    path('edit_qr/<int:qr_id>',edit_qr,name='edit_qr'),
    path('qr_view/<int:qr_id>',detail_qr,name='qr_detail'),
    path('leaderboard/',leaderboard,name='leaderboard'),
]
