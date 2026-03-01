from django.contrib import admin
from .models import Clientes, Citas, Status, Servicios

# Register your models here.

admin.site.register(Servicios)


@admin.register(Clientes)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'telefono', 'ciudad', 'status')
    search_fields = ('nombre', 'apellidos', 'telefono')
    list_filter = ('status', 'ciudad')


@admin.register(Citas)
class CitasAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha', 'hora', 'estado')
    list_filter = ('fecha', 'estado')
    search_fields = ('cliente__nombre',)
