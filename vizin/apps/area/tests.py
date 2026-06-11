from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from apps.area.forms import AreaForm, ReservaForm
from apps.area.models import Area, Reserva
from apps.morador.models import Morador, Apartamento
from apps.administrador.models import Administrador
from django.contrib.auth.models import User


class AreaFormTest(TestCase):

    def test_area_form_valido(self):
        form_data = {
            'nome': 'Piscina',
            'regras': 'Não correr',
            'taxa_reserva': 50.00
        }

        form = AreaForm(data=form_data)
        self.assertTrue(form.is_valid())


class ReservaFormTest(TestCase):

    def setUp(self):
        # cria usuário para morador
        self.user = User.objects.create_user(
            username='morador',
            password='123456'
        )

        # cria usuário para administrador
        self.admin_user = User.objects.create_user(
            username='admin',
            password='123456'
        )

        # cria administrador vinculado ao usuário admin
        self.admin = Administrador.objects.create(
            user=self.admin_user,
            cpf='12345678901'
        )

        # cria apartamento
        self.apartamento = Apartamento.objects.create(numero="101", bloco="A")

        # cria morador vinculado ao apartamento e administrador
        self.morador = Morador.objects.create(
            user=self.user,
            administrador=self.admin,
            apartamento=self.apartamento,
            cpf='99999999999',
            telefone='81999999999',
            tipo_morador=Morador.TipoMorador.PROPRIETARIO
        )

        # cria área vinculada ao administrador
        self.area = Area.objects.create(
            nome="Salão de Festas",
            regras="Sem bagunça",
            taxa_reserva=100,
            administrador=self.admin
        )

    def test_reserva_data_passada_invalida(self):
        passado = timezone.now() - timedelta(days=1)
        futuro = timezone.now() + timedelta(days=1)

        form_data = {
            'horario_inicio': passado,
            'horario_fim': futuro,
            'motivo': 'Teste'
        }

        form = ReservaForm(data=form_data)
        form.instance.area = self.area
        form.instance.morador = self.morador
        form.instance.administrador = self.admin
        self.assertFalse(form.is_valid())

    def test_reserva_inicio_maior_que_fim(self):
        inicio = timezone.now() + timedelta(days=1)
        fim = timezone.now()

        form_data = {
            'horario_inicio': inicio,
            'horario_fim': fim,
            'motivo': 'Teste'
        }

        form = ReservaForm(data=form_data)
        form.instance.area = self.area
        form.instance.morador = self.morador
        form.instance.administrador = self.admin
        self.assertFalse(form.is_valid())

    def test_reserva_conflito_horario(self):
        inicio = timezone.now() + timedelta(days=1)
        fim = inicio + timedelta(hours=2)

        # cria reserva existente
        Reserva.objects.create(
            horario_inicio=inicio,
            horario_fim=fim,
            motivo="Existente",
            area=self.area,
            morador=self.morador,
            administrador=self.admin
        )

        # tenta criar outra no mesmo horário
        form_data = {
            'horario_inicio': inicio + timedelta(minutes=30),
            'horario_fim': fim + timedelta(hours=1),
            'motivo': 'Conflito'
        }

        form = ReservaForm(data=form_data)
        form.instance.area = self.area
        form.instance.morador = self.morador
        form.instance.administrador = self.admin
        self.assertFalse(form.is_valid())

    def test_reserva_valida(self):
        inicio = timezone.now() + timedelta(days=1)
        fim = inicio + timedelta(hours=2)

        form_data = {
            'horario_inicio': inicio,
            'horario_fim': fim,
            'motivo': 'Evento'
        }

        form = ReservaForm(data=form_data)
        form.instance.area = self.area
        form.instance.morador = self.morador
        form.instance.administrador = self.admin
        self.assertTrue(form.is_valid())
