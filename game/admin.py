from django.contrib import admin
from game.models import *

# Register your models here.
admin.site.register(Gamer)
admin.site.register(ClubMember)
admin.site.register(QRScan)
admin.site.register(SuccessfullScan)