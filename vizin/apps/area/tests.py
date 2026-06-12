from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import json

from apps.administrador.models import Administrador
from apps.morador.models import Morador, Apartamento
from .models import Area, Reserva
from .forms import AreaForm, ReservaForm

class AreaBaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Criar Administrador 1
        self.user_admin = User.objects.create_user(
            username='admin1@email.com',
            email='admin1@email.com',
            password='password123'
        )
        self.admin = Administrador.objects.create(
            user=self.user_admin,
            cpf='11111111111'
        )

        # Criar Administrador 2 (para testes de segurança)
        self.user_admin2 = User.objects.create_user(
            username='admin2@email.com',
            email='admin2@email.com',
            password='password123'
        )
        self.admin2 = Administrador.objects.create(
            user=self.user_admin2,
            cpf='22222222222'
        )

        # Criar Morador vinculado ao Admin 1
        self.apartamento = Apartamento.objects.create(
            bloco='A', andar='1', numero='101'
        )
        self.user_morador = User.objects.create_user(
            username='morador@email.com',
            email='morador@email.com',
            password='password123'
        )
        self.morador = Morador.objects.create(
            user=self.user_morador,
            cpf='33333333333',
            telefone='81999999999',
            tipo_morador=Morador.TipoMorador.PROPRIETARIO,
            administrador=self.admin,
            apartamento=self.apartamento
        )

        # Criar uma Área vinculada ao Admin 1
        self.area = Area.objects.create(
            nome='Piscina',
            regras='Não correr na borda.',
            taxa_reserva=50.0,
            administrador=self.admin
        )

class AreaModelTest(AreaBaseTestCase):
    def test_area_creation(self):
        self.assertEqual(self.area.nome, 'Piscina')
        self.assertEqual(str(self.area), 'Piscina')

    def test_reserva_creation(self):
        inicio = timezone.now() + timedelta(days=1)
        fim = inicio + timedelta(hours=2)
        reserva = Reserva.objects.create(
            horario_inicio=inicio,
            horario_fim=fim,
            motivo='Aniversário',
            area=self.area,
            morador=self.morador,
            administrador=self.admin
        )
        self.assertEqual(reserva.status, Reserva.Status.ABERTO)
        expected_str = f"{self.morador} - {self.area} ({inicio})"
        self.assertEqual(str(reserva), expected_str)

class AreaFormTest(AreaBaseTestCase):
    def test_area_form_valid(self):
        data = {'nome': 'Salão de Festas', 'regras': 'Limpar após o uso.', 'taxa_reserva': 100.0}
        form = AreaForm(data=data)
        self.assertTrue(form.is_valid())

    def test_reserva_form_invalid_past_date(self):
        inicio = timezone.now() - timedelta(days=1)
        fim = inicio + timedelta(hours=2)
        data = {
            'horario_inicio': inicio,
            'horario_fim': fim,
            'motivo': 'Festa'
        }
        form = ReservaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('Não é possível realizar uma reserva para uma data/hora que já passou.', form.non_field_errors())

    def test_reserva_form_invalid_end_before_start(self):
        inicio = timezone.now() + timedelta(days=1)
        fim = inicio - timedelta(hours=1)
        data = {
            'horario_inicio': inicio,
            'horario_fim': fim,
            'motivo': 'Festa'
        }
        form = ReservaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('O horário de início deve ser anterior ao horário de término.', form.non_field_errors())
    
    def test_reserva_form_conflito(self):
        inicio = (timezone.localtime(timezone.now()) + timedelta(days=5)).replace(second=0, microsecond=0)
        fim = inicio + timedelta(hours=2)
        
        # Reserva existente APROVADA
        Reserva.objects.create(
            horario_inicio=inicio, horario_fim=fim,
            status=Reserva.Status.APROVADO,
            area=self.area, morador=self.morador, administrador=self.admin
        )
        
        # Testar formulário com mesmo horário
        data = {
            'horario_inicio': inicio,
            'horario_fim': fim,
            'motivo': 'Novo'
        }
        # Precisamos passar a instância com a área para o clean() funcionar
        form = ReservaForm(data=data)
        form.instance.area = self.area
        
        self.assertFalse(form.is_valid())
        self.assertIn('Já existe uma reserva pendente ou aprovada para esta área no horário selecionado.', form.non_field_errors())

class AreaAdminViewsTest(AreaBaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username='admin1@email.com', password='password123')

    def test_lista_areas(self):
        response = self.client.get(reverse('administrador:lista_areas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Piscina')

    def test_cadastrar_area_sucesso(self):
        response = self.client.post(reverse('administrador:cadastrar_area'), {
            'nome': 'Churrasqueira',
            'regras': 'Proibido som alto.',
            'taxa_reserva': 30.0
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Area.objects.filter(nome='Churrasqueira').exists())

    def test_editar_area_sucesso(self):
        url = reverse('administrador:editar_area', args=[self.area.id])
        response = self.client.post(url, {
            'nome': 'Piscina VIP',
            'regras': self.area.regras,
            'taxa_reserva': 75.0
        })
        self.assertEqual(response.status_code, 302)
        self.area.refresh_from_db()
        self.assertEqual(self.area.nome, 'Piscina VIP')

    def test_editar_area_outro_admin_negado(self):
        self.client.login(username='admin2@email.com', password='password123')
        url = reverse('administrador:editar_area', args=[self.area.id])
        response = self.client.post(url, {'nome': 'Hacker Area'})
        self.assertEqual(response.status_code, 404)

    def test_deletar_area_sucesso(self):
        url = reverse('administrador:deletar_area', args=[self.area.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'ok': True})
        self.assertFalse(Area.objects.filter(id=self.area.id).exists())

    def test_validar_reserva_aprovar(self):
        reserva = Reserva.objects.create(
            horario_inicio=timezone.now() + timedelta(days=1),
            horario_fim=timezone.now() + timedelta(days=1, hours=2),
            motivo='Teste', area=self.area, morador=self.morador, administrador=self.admin
        )
        url = reverse('administrador:validar_reserva', args=[reserva.id])
        response = self.client.post(url, data=json.dumps({'acao': 'aprovar'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        reserva.refresh_from_db()
        self.assertEqual(reserva.status, Reserva.Status.APROVADO)

class AreaMoradorViewsTest(AreaBaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username='morador@email.com', password='password123')

    def test_lista_areas_comuns(self):
        response = self.client.get(reverse('morador:lista_areas_comuns'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Piscina')

    def test_fazer_reserva_sucesso(self):
        inicio = timezone.now() + timedelta(days=2)
        fim = inicio + timedelta(hours=3)
        url = reverse('morador:fazer_reserva', args=[self.area.id])
        response = self.client.post(url, {
            'horario_inicio': inicio.strftime('%Y-%m-%dT%H:%M'),
            'horario_fim': fim.strftime('%Y-%m-%dT%H:%M'),
            'motivo': 'Churrasco'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Reserva.objects.filter(motivo='Churrasco').exists())

    def test_fazer_reserva_conflito(self):
        # Garantir precisão de minutos para coincidir com o input
        inicio = (timezone.localtime(timezone.now()) + timedelta(days=3)).replace(second=0, microsecond=0)
        fim = inicio + timedelta(hours=2)
        
        # Reserva existente ABERTA (bloqueia o horário)
        Reserva.objects.create(
            horario_inicio=inicio, horario_fim=fim,
            status=Reserva.Status.ABERTO,
            motivo='Existente', area=self.area, morador=self.morador, administrador=self.admin
        )
        
        url = reverse('morador:fazer_reserva', args=[self.area.id])
        response = self.client.post(url, {
            'horario_inicio': inicio.strftime('%Y-%m-%dT%H:%M'),
            'horario_fim': fim.strftime('%Y-%m-%dT%H:%M'),
            'motivo': 'Conflito'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Já existe uma reserva pendente ou aprovada para esta área no horário selecionado.")

    def test_fazer_reserva_sem_conflito_negada(self):
        # Reserva NEGADA não deve bloquear o horário
        inicio = (timezone.localtime(timezone.now()) + timedelta(days=4)).replace(second=0, microsecond=0)
        fim = inicio + timedelta(hours=2)
        
        Reserva.objects.create(
            horario_inicio=inicio, horario_fim=fim,
            status=Reserva.Status.NEGADO,
            area=self.area, morador=self.morador, administrador=self.admin
        )
        
        url = reverse('morador:fazer_reserva', args=[self.area.id])
        response = self.client.post(url, {
            'horario_inicio': inicio.strftime('%Y-%m-%dT%H:%M'),
            'horario_fim': fim.strftime('%Y-%m-%dT%H:%M'),
            'motivo': 'Livre'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Reserva.objects.filter(motivo='Livre').exists())

    def test_fazer_reserva_adjacente_sem_conflito(self):
        # Reservas adjacentes (termina uma, começa outra) são permitidas
        inicio1 = (timezone.localtime(timezone.now()) + timedelta(days=6)).replace(second=0, microsecond=0)
        fim1 = inicio1 + timedelta(hours=1)
        
        Reserva.objects.create(
            horario_inicio=inicio1, horario_fim=fim1,
            status=Reserva.Status.APROVADO,
            area=self.area, morador=self.morador, administrador=self.admin
        )
        
        # Nova reserva começando exatamente quando a outra termina
        url = reverse('morador:fazer_reserva', args=[self.area.id])
        response = self.client.post(url, {
            'horario_inicio': fim1.strftime('%Y-%m-%dT%H:%M'),
            'horario_fim': (fim1 + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M'),
            'motivo': 'Adjacente'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Reserva.objects.filter(motivo='Adjacente').exists())

    def test_cancelar_reserva_sucesso(self):
        reserva = Reserva.objects.create(
            horario_inicio=timezone.now() + timedelta(days=1),
            horario_fim=timezone.now() + timedelta(days=1, hours=2),
            motivo='Cancelar', area=self.area, morador=self.morador, administrador=self.admin
        )
        url = reverse('morador:cancelar_reserva', args=[reserva.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Reserva.objects.filter(id=reserva.id).exists())
