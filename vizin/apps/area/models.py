from django.db import models
from apps.administrador.models import Administrador
from apps.morador.models import Morador

# Create your models here.
class Area(models.Model):
    nome = models.CharField(max_length=60) 
    regras = models.CharField(max_length=500) 
    taxa_reserva = models.FloatField()

    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)

    class Meta:
        db_table = "area"

class Reserva(models.Model):
    horario_inicio = models.DateTimeField()
    horario_fim = models.DateTimeField()
    motivo = models.CharField(max_length=500)

    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    morador = models.ForeignKey(Morador, on_delete=models.CASCADE)
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)

    class Meta:
        db_table = "reserva"


