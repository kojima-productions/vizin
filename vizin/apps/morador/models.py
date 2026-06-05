from django.db import models
from django.contrib.auth.models import User

from apps.administrador.models import Administrador

class Apartamento(models.Model):
    bloco = models.CharField(max_length=5)
    andar = models.CharField(max_length=3)
    numero = models.CharField(max_length=10)

    class Meta:
        db_table = 'apartamento'

class Morador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11)
    telefone = models.CharField(max_length=11)

    class TipoMorador(models.TextChoices):
        INQUILINO = "Inquilino"
        PROPRIETARIO = "Proprietario"

    tipo_morador = models.CharField(max_length=12, choices=TipoMorador.choices)

    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE, default=-1)

    class Meta:
        db_table = 'morador'
