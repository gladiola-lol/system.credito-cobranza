from django.shortcuts import render, redirect
from django.http import response, request
from .forms import ClienteForm, CitaForm, FiltrofechaForm
from .models import Clientes, Citas, Contacto, Servicios
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.generic import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages

from django.urls import reverse_lazy

# Create your views here.


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_autheticated and self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(
            self.request, "no tienes autorizacion para realizar esta accion")
        return redirect('cobranza:home')


class ClienteOStaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.is_authenticated

    def handle_no_permission(self):
        messages.error(
            self.request, "debes iniciar sesion para realizar esta accion")
        return redirect('cobranza:crear_cliente')


def home(request):
    return render(request, 'clientes/home.html')


def crear_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            return redirect('cobranza:detalle_cliente', pk=cliente.pk)
    else:
        form = ClienteForm()

    return render(request, 'clientes/componentes/nuevo_cliente.html', {'form': form})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_cita(request, pk):
    cliente = get_object_or_404(Clientes, pk=pk)
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.cliente = cliente
            cita.save()
            return redirect('cobranza:home')
    else:
        form = CitaForm()
    return render(request, 'clientes/componentes/nueva_cita.html', {'form': form})


def lista_clientes(request):
    clientes = Clientes.objects.all()
    return render(request, 'clientes/componentes/lista_clientes.html', {'clientes': clientes})


def cliente_detalle(request, pk):
    cliente = get_object_or_404(Clientes, pk=pk)
    return render(request, 'clientes/componentes/detalle_cliente.html', {'cliente': cliente})
# ver citas por periodo determinado filtrado


def citas_por_periodo(request):
    citas = Citas.objects.all()
    form = FiltrofechaForm(request.GET or None)

    if form.is_valid():
        fecha_inicio = form.cleaned_data['fecha_inicio']
        fecha_fin = form.cleaned_data['fecha_fin']

        citas = Citas.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin])
    return render(request, 'clientes/componentes/calendario.html', {'form': form,
                                                                    'citas': citas})


class ClienteUpdateView(StaffRequiredMixin, UpdateView):
    model = Clientes
    fields = '__all__'
    template_name = 'clientes/componentes/editar_cliente.html'
    success_url = reverse_lazy('cobranza:home')


class ClienteDeleteView(StaffRequiredMixin, DeleteView):
    model = Clientes
    template_name = 'clientes/componentes/eliminar_cliente.html'
    success_url = reverse_lazy('cobranza:clientes')


class CitaUpdateView(StaffRequiredMixin, UpdateView):
    model = Citas
    fields = ['fecha', 'hora']
    template_name = 'clientes/componentes/editar_cita.html'
    success_url = reverse_lazy('cobranza:citas')


class CitaDeleteView(StaffRequiredMixin, DeleteView):
    model = Citas
    template_name = 'clientes/componentes/eliminar_cita.html'
    success_url = reverse_lazy('cobranza:home')


def servicios(request):
    servicios = Servicios.objects.all()

    return render(request, 'clientes/componentes/servicios.html', {"servicios": servicios})


def contacto(request):
    mensaje = False
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')

        Contacto.objects.create(
            nombre=nombre,
            correo=correo,
            telefono=telefono
        )
        mensaje = True
    return render(request, 'clientes/componentes/contacto.html', {'mensaje': mensaje})
