from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.


class Status(models.TextChoices):
    ACTIVO = 'activo', 'activo'
    INACTIVO = 'inactivo', 'inactivo'


class Clientes(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    telefono = models.CharField(max_length=16)
    ciudad = models.CharField(max_length=50)
    email = models.EmailField()
    edad = models.IntegerField()
    status = models.CharField(
        max_length=50, choices=Status.choices, default=Status.ACTIVO)

    def __str__(self):
        return self.nombre


class Servicios(models.Model):
    nombre = models.CharField(max_length=50)
    duracion = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=50, choices=Status.choices, default=Status.ACTIVO)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Status_cita(models.TextChoices):
    PENDIENTE = 'pendiente', 'pend'
    CANCELADA = 'cancelada', 'cancel'
    CONFIRMADA = 'confirmada', 'confir'


class Citas(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=50, choices=Status_cita.choices, default=Status_cita.PENDIENTE)

    def clean(self):
        if self.fecha < timezone.now().date():
            raise ValidationError("no puedes agendar citas en el pasado")

    class Meta:
        ordering = ['fecha', 'hora']
        constraints = [models.UniqueConstraint(
            fields=['fecha', 'hora'],
            name='unique_cita_fecha_hora'
        )]


class Contacto(models.Model):
    nombre = models.CharField(max_length=20)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
