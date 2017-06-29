from django.contrib import admin
from .models import Aparcamiento, Usuario, Fecha, Comentario

# Register your models here.
admin.site.register(Aparcamiento)
admin.site.register(Usuario)
admin.site.register(Fecha)
admin.site.register(Comentario)
