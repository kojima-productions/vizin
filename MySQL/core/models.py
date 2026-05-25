# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Administrador(models.Model):
    id_admin = models.AutoField(primary_key=True)
    tipo_admin = models.CharField(max_length=20)
    cnpj = models.CharField(db_column='CNPJ', max_length=14, blank=True, null=True)  # Field name made lowercase.
    inicio_mandato = models.DateField()
    fim_mandato = models.DateField()
    nome_admin = models.CharField(max_length=100)
    email_admin = models.CharField(unique=True, max_length=100)
    senha_admin = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'administrador'


class Apartamento(models.Model):
    id_apartamento = models.AutoField(primary_key=True)
    numero = models.IntegerField()
    placa_veiculo = models.CharField(max_length=7, blank=True, null=True)
    bloco = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'apartamento'


class AreaReserva(models.Model):
    id_area = models.AutoField(primary_key=True)
    tipo_area = models.CharField(max_length=50)
    regras = models.TextField()
    taxa_reserva = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'area_reserva'


class Comunicado(models.Model):
    id_comunicado = models.AutoField(primary_key=True)
    tipo_comunicado = models.CharField(max_length=16)
    descricao = models.TextField()
    id_admin = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='id_admin')

    class Meta:
        managed = False
        db_table = 'comunicado'


class Encomenda(models.Model):
    id_encomenda = models.AutoField(primary_key=True)
    id_apartamento = models.ForeignKey(Apartamento, models.DO_NOTHING, db_column='id_apartamento')
    chegada = models.DateTimeField()
    status_encomenda = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'encomenda'


class Escala(models.Model):
    data_escala = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    id_escala = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'escala'


class Funcionario(models.Model):
    id_funcionario = models.AutoField(primary_key=True)
    id_escala = models.ForeignKey(Escala, models.DO_NOTHING, db_column='id_escala')
    nome_funcionario = models.CharField(max_length=100)
    email_funcionario = models.CharField(unique=True, max_length=100)
    senha_funcionario = models.CharField(max_length=150)
    cargo = models.CharField(max_length=13)

    class Meta:
        managed = False
        db_table = 'funcionario'


class Morador(models.Model):
    id_morador = models.AutoField(primary_key=True)
    tipo_morador = models.CharField(max_length=11)
    id_apartamento = models.ForeignKey(Apartamento, models.DO_NOTHING, db_column='id_apartamento')
    nome_morador = models.CharField(max_length=100)
    email_morador = models.CharField(unique=True, max_length=100)
    senha_morador = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'morador'


class Ocorrencia(models.Model):
    id_ocorrencia = models.AutoField(primary_key=True)
    tipo_ocorrencia = models.CharField(max_length=19)
    status_ocorrencia = models.CharField(max_length=12)
    id_reclamacao = models.ForeignKey('Reclamacao', models.DO_NOTHING, db_column='id_reclamacao')
    descricao_ocorrencia = models.CharField(max_length=300)
    id_admin = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='id_admin')
    data_ocorrencia = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ocorrencia'


class Reclamacao(models.Model):
    id_reclamacao = models.AutoField(primary_key=True)
    id_apartamento = models.ForeignKey(Apartamento, models.DO_NOTHING, db_column='id_apartamento')
    tipo_reclamacao = models.CharField(max_length=19)
    descricao = models.CharField(max_length=300)
    data_reclamacao = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reclamacao'


class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    horario = models.TimeField()
    data_reserva = models.DateField()
    motivo_reserva = models.CharField(max_length=100)
    id_apartamento = models.ForeignKey(Apartamento, models.DO_NOTHING, db_column='id_apartamento')
    id_area = models.ForeignKey(AreaReserva, models.DO_NOTHING, db_column='id_area')

    class Meta:
        managed = False
        db_table = 'reserva'


class Visita(models.Model):
    id_visita = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=11)
    id_funcionario = models.ForeignKey(Funcionario, models.DO_NOTHING, db_column='id_funcionario')
    nome = models.CharField(max_length=100, blank=True, null=True)
    entrada = models.DateTimeField(blank=True, null=True)
    acesso = models.IntegerField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'visita'
