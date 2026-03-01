from django import forms
from .models import Citas, Clientes
# from django.django-phonenumber-field


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nombre', 'apellidos', 'email',
                  'edad', 'telefono', 'ciudad', 'status']


class CitaForm(forms.ModelForm):
    class Meta:
        model = Citas
        fields = ['fecha', 'hora', 'estado', 'servicio']
        widgets = {'fecha': forms.DateInput(attrs={'type': 'date',
                                                   'class': 'form-control'}),
                   'hora': forms.TimeInput(attrs={'type': 'time',
                                                  'class': 'form-control'}), }


class FiltrofechaForm(forms.Form):
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


# class ContactoForm(forms.Form):
 #   nombre = forms.CharField(max_length=50)
  #  telefono = forms.CharField(max_length=16)
   # email = forms.EmailField()
# django-phonenumber-field
