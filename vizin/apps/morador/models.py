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

class Veiculo(models.Model):
    class TipoVeiculo(models.TextChoices):
        CARRO = "Carro"
        MOTO = "Moto"
        OUTRO = "Outro"

    modelo = models.CharField(max_length=50)
    cor = models.CharField(max_length=20)
    placa = models.CharField(max_length=7, unique=True)
    tipo = models.CharField(max_length=10, choices=TipoVeiculo.choices)
    
    apartamento = models.OneToOneField(Apartamento, on_delete=models.CASCADE, related_name='veiculo')

    class Meta:
        db_table = 'veiculo'

    def __str__(self):
        return f"{self.modelo} ({self.placa})"
