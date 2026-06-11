from django.db import models
from django.utils import timezone
import secrets

class Visita(models.Model):
    class StatusVisita(models.TextChoices):
        AGENDADA = "Agendada", "Agendada"
        REGISTRADA = "Registrada", "Registrada"

    morador = models.ForeignKey('morador.Morador', on_delete=models.CASCADE, related_name='visitas')
    funcionario = models.ForeignKey('funcionario.Funcionario', on_delete=models.SET_NULL, null=True, blank=True, related_name='visitas_validadas')
    
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    acesso = models.CharField(max_length=10, unique=True)
    
    data_entrada = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=StatusVisita.choices, default=StatusVisita.AGENDADA)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.acesso:
            # Gera um código único alfanumérico de 8 caracteres
            self.acesso = secrets.token_hex(4).upper()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'visita'

    def __str__(self):
        return f"Visita: {self.nome} ({self.status})"
