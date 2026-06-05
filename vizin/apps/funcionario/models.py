from django.db import models
from django.contrib.auth.models import User
from apps.administrador.models import Administrador

# Create your models here.
class Funcionario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=11)
    cargo = models.CharField(max_length=100)

    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, related_name='funcionarios')

    def __str__(self):
        return f"Funcionário: {self.user.get_full_name() or self.user.email}"

    class Meta:
        db_table = "funcionario"