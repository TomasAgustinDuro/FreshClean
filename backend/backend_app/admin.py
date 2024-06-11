# backend_app/admin.py
from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuarioid', 'nombre', 'apellido', 'email', 'direccion', 'telefono', 'fecha_de_registro', 'is_staff']
    search_fields = ['nombre', 'apellido', 'email']
    list_filter = ['is_staff', 'fecha_de_registro']
