from django.db import models
from django.contrib.auth.models import User
from apps.morador.models import Apartamento

class Encomenda(models.Model):
    class Status(models.TextChoices):
        RECEBIDA = "Recebida", "Recebida (Não entregue)"
        ENTREGUE = "Entregue", "Entregue"

    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE, related_name='encomendas')
    descricao = models.CharField(max_length=255)
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.RECEBIDA
    )
    data_chegada = models.DateTimeField(auto_now_add=True)
    data_entrega = models.DateTimeField(null=True, blank=True)
    
    registrado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='encomendas_registradas'
    )
    entregue_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='encomendas_entregues'
    )

    class Meta:
        db_table = 'encomenda'

    def __str__(self):
        return f"{self.descricao} - {self.apartamento} ({self.status})"
