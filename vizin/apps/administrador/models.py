from django.db import models
from django.contrib.auth.models import User

class Administrador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True)
    inicio_mandato = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Administrador: {self.user.get_full_name() or self.user.email}"

    class Meta:
        db_table = "administrador"

class Comunicado(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=1000)
    data = models.DateTimeField(auto_now_add=True)

    class TipoComunicado(models.TextChoices):
        MANUTENCAO = "Manutenção"
        ASSEMBLEIA = "Assembleia"
        SEGURANCA = "Segurança"
        EVENTO = "Evento"
        URGENTE = "Urgente"
        FINANCEIRO = "Financeiro"
        CONVIVENCIA = "Convivencia"
        FALTA_AGUA = "Falta de agua"
        FALTA_ENERGIA = "Falta de energia"

    tipo = models.CharField(max_length=16, choices=TipoComunicado.choices)

    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comunicado: {self.titulo} | {self.data}"

    class Meta:
        db_table = "comunicado"



