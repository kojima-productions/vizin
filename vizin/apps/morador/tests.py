from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from apps.morador.models import Morador, Apartamento
from apps.administrador.models import Administrador
from apps.area.models import Area, Reserva


class MoradorViewsTest(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin@email.com',
            password='12345678'
        )

        self.administrador = Administrador.objects.create(
            user=self.admin_user,
            cpf='12345678901'
        )

        self.apartamento = Apartamento.objects.create(
            bloco='A',
            andar='1',
            numero='101'
        )

        self.user_morador = User.objects.create_user(
            username='morador@email.com',
            email='morador@email.com',
            password='12345678'
        )

        self.morador = Morador.objects.create(
            user=self.user_morador,
            administrador=self.administrador,
            cpf="99999999999",
            telefone="81999999999",
            tipo_morador=Morador.TipoMorador.PROPRIETARIO,
            apartamento=self.apartamento
        )

    def test_login_morador_sucesso(self):
        response = self.client.post(
            reverse('morador:login'),
            {
                'login': 'morador@email.com',
                'senha': '12345678'
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_login_morador_invalido(self):
        response = self.client.post(
            reverse('morador:login'),
            {
                'login': 'morador@email.com',
                'senha': 'senha_errada'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Credenciais inválidas.')

    def test_usuario_sem_perfil_morador(self):
        usuario_comum = User.objects.create_user(
            username='comum@email.com',
            email='comum@email.com',
            password='12345678'
        )

        response = self.client.post(
            reverse('morador:login'),
            {
                'login': 'comum@email.com',
                'senha': '12345678'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Usuário autenticado não possui perfil de Morador.'
        )

    def test_painel_morador_logado(self):
        self.client.login(
            username='morador@email.com',
            password='12345678'
        )

        response = self.client.get(reverse('morador:painel'))
        self.assertEqual(response.status_code, 200)

    def test_painel_exige_login(self):
        response = self.client.get(reverse('morador:painel'))
        self.assertEqual(response.status_code, 302)

    def test_usuario_comum_nao_acessa_painel(self):
        usuario_comum = User.objects.create_user(
            username='comum@email.com',
            password='12345678'
        )

        self.client.login(
            username='comum@email.com',
            password='12345678'
        )

        response = self.client.get(reverse('morador:painel'))
        self.assertEqual(response.status_code, 403)

    def test_deletar_usuario_remove_morador(self):
        self.user_morador.delete()

        self.assertFalse(
            Morador.objects.filter(id=self.morador.id).exists()
        )

    def test_relacionamento_morador_apartamento(self):
        self.assertEqual(self.morador.apartamento.numero, '101')
        self.assertEqual(self.morador.apartamento.bloco, 'A')


class MoradorReservaTest(TestCase):

    def setUp(self):
        # admin
        self.user_admin = User.objects.create_user(
            username='admin',
            password='12345678'
        )
        self.admin = Administrador.objects.create(
            user=self.user_admin,
            cpf='12345678901'
        )

        # morador
        self.user_morador = User.objects.create_user(
            username='morador',
            password='12345678'
        )

        # apartamento
        self.apartamento = Apartamento.objects.create(
            bloco='A',
            andar='1',
            numero='101'
        )

        self.morador = Morador.objects.create(
            user=self.user_morador,
            administrador=self.admin,
            apartamento=self.apartamento,
            cpf='99999999999',
            telefone='81999999999',
            tipo_morador=Morador.TipoMorador.PROPRIETARIO
        )

        # área
        self.area = Area.objects.create(
            nome="Salão de Festas",
            regras="Sem bagunça",
            taxa_reserva=100,
            administrador=self.admin
        )

    def test_morador_pode_criar_reserva(self):
        """Testa se um morador consegue criar uma reserva."""
        inicio = timezone.now() + timedelta(days=1)
        fim = inicio + timedelta(hours=2)

        reserva = Reserva.objects.create(
            horario_inicio=inicio,
            horario_fim=fim,
            motivo="Aniversário",
            area=self.area,
            morador=self.morador,
            administrador=self.admin,
            status=Reserva.Status.ABERTO
        )

        self.assertEqual(reserva.status, Reserva.Status.ABERTO)
        self.assertEqual(reserva.morador, self.morador)
        self.assertEqual(reserva.area, self.area)

    def test_reserva_data_passada_invalida(self):
        inicio = timezone.now() - timedelta(days=1)
        fim = timezone.now() + timedelta(days=1)

        reserva = Reserva(
            horario_inicio=inicio,
            horario_fim=fim,
            motivo="Teste inválido",
            area=self.area,
            morador=self.morador,
            administrador=self.admin,
            status=Reserva.Status.ABERTO
        )

        is_valida = reserva.horario_inicio >= timezone.now()
        self.assertFalse(is_valida)

    def test_inicio_maior_que_fim(self):
        inicio = timezone.now() + timedelta(days=1)
        fim = timezone.now()

        reserva = Reserva(
            horario_inicio=inicio,
            horario_fim=fim,
            motivo="Erro",
            area=self.area,
            morador=self.morador,
            administrador=self.admin,
            status=Reserva.Status.ABERTO
        )

        is_valida = reserva.horario_inicio < reserva.horario_fim
        self.assertFalse(is_valida)

    def test_conflito_reserva_mesma_area(self):
        inicio = timezone.now() + timedelta(days=1)
        fim = inicio + timedelta(hours=2)

        Reserva.objects.create(
            horario_inicio=inicio,
            horario_fim=fim,
            motivo="Existente",
            area=self.area,
            morador=self.morador,
            administrador=self.admin,
            status=Reserva.Status.ABERTO
        )

        nova = Reserva.objects.create(
            horario_inicio=inicio + timedelta(minutes=30),
            horario_fim=fim,
            motivo="Conflito",
            area=self.area,
            morador=self.morador,
            administrador=self.admin,
            status=Reserva.Status.ABERTO
        )

        conflito = Reserva.objects.filter(
            area=self.area,
            horario_inicio__lt=nova.horario_fim,
            horario_fim__gt=nova.horario_inicio,
        ).count()

        self.assertGreaterEqual(conflito, 1)

    def test_fluxo_reserva_pendente(self):
        inicio = timezone.now() + timedelta(days=1)
        fim = inicio + timedelta(hours=2)

        reserva = Reserva.objects.create(
            horario_inicio=inicio,
            horario_fim=fim,
            motivo="Evento",
            area=self.area,
            morador=self.morador,
            administrador=self.admin,
            status=Reserva.Status.ABERTO
        )

        self.assertEqual(reserva.status, Reserva.Status.ABERTO)

        reserva.status = Reserva.Status.APROVADO
        reserva.save()

        reserva.refresh_from_db()
        self.assertEqual(reserva.status, Reserva.Status.APROVADO)