from django.contrib import admin
from .models import ClientProfile, Employe, Projet, ProjetImage, Tache

admin.site.register(ClientProfile)
admin.site.register(Employe)
admin.site.register(Projet)
admin.site.register(ProjetImage)
admin.site.register(Tache)
