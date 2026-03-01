from django.urls import path
from . import views
from .views import ClienteDeleteView, ClienteUpdateView, CitaDeleteView, CitaUpdateView

app_name = 'cobranza'

urlpatterns = [
    path('home', views.home, name='home'),
    path('clientes/', views.lista_clientes, name='clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:pk>/', views.cliente_detalle, name='detalle_cliente'),
    path('clientes/crear/citas/', views.citas_por_periodo, name='citas'),
    path('clientes/<int:pk>/citas/nueva/', views.crear_cita, name='nueva_cita'),
    path('clientes/<int:pk>/editar/',
         ClienteUpdateView.as_view(), name='editar_cliente'),
    path('clientes/<int:pk>/eliminar/',
         ClienteDeleteView.as_view(), name='eliminar_cliente'),
    path('citas/<int:pk>/editar/', CitaUpdateView.as_view(), name='editar_cita'),
    path('citas/<int:pk>/eliminar/',
         CitaDeleteView.as_view(), name='eliminar_cita'),
    path('home/servicios/', views.servicios, name='servicios'),
    path('home/contacto/', views.contacto, name='contacto'),


]
