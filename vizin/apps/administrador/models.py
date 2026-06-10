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
