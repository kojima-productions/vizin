from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from apps.administrador.models import Administrador
from apps.morador.models import Morador, Apartamento
from apps.funcionario.models import Funcionario
from .models import Visita
from .forms import VisitaForm

class VisitaBaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Admin 1
        self.user_admin1 = User.objects.create_user(username='admin1@test.com', email='admin1@test.com', password='pass')
        self.admin1 = Administrador.objects.create(user=self.user_admin1, cpf='11111111111')
        
        # Admin 2 (para teste de isolamento)
        self.user_admin2 = User.objects.create_user(username='admin2@test.com', email='admin2@test.com', password='pass')
        self.admin2 = Administrador.objects.create(user=self.user_admin2, cpf='22222222222')

        # Morador 1 (do Admin 1)
        self.apt1 = Apartamento.objects.create(bloco='A', andar='1', numero='101')
        self.user_morador1 = User.objects.create_user(username='morador1@test.com', email='morador1@test.com', password='pass')
        self.morador1 = Morador.objects.create(
            user=self.user_morador1, cpf='33333333333', telefone='8199', 
            tipo_morador=Morador.TipoMorador.PROPRIETARIO, administrador=self.admin1, apartamento=self.apt1
        )

        # Morador 2 (do Admin 1 - vizinho)
        self.apt2 = Apartamento.objects.create(bloco='A', andar='1', numero='102')
        self.user_morador2 = User.objects.create_user(username='morador2@test.com', email='morador2@test.com', password='pass')
        self.morador2 = Morador.objects.create(
            user=self.user_morador2, cpf='44444444444', telefone='8188', 
            tipo_morador=Morador.TipoMorador.PROPRIETARIO, administrador=self.admin1, apartamento=self.apt2
        )

        # Funcionário 1 (do Admin 1)
        self.user_func1 = User.objects.create_user(username='func1@test.com', email='func1@test.com', password='pass')
        self.func1 = Funcionario.objects.create(
            user=self.user_func1, cpf='55555555555', telefone='8177', cargo='Porteiro', administrador=self.admin1
        )

        # Funcionário 2 (do Admin 2)
        self.user_func2 = User.objects.create_user(username='func2@test.com', email='func2@test.com', password='pass')
        self.func2 = Funcionario.objects.create(
            user=self.user_func2, cpf='66666666666', telefone='8166', cargo='Porteiro', administrador=self.admin2
        )

class VisitaModelTest(VisitaBaseTestCase):
    def test_visita_creation_and_auto_code(self):
        visita = Visita.objects.create(
            morador=self.morador1,
            nome='Visitante Teste',
            cpf='12345678900'
        )
        self.assertEqual(visita.status, Visita.StatusVisita.AGENDADA)
        self.assertTrue(len(visita.acesso) > 0)
        self.assertEqual(visita.acesso, visita.acesso.upper())
        self.assertEqual(str(visita), f"Visita: {visita.nome} ({visita.status})")

class VisitaFormTest(TestCase):
    def test_visita_form_valid(self):
        form = VisitaForm(data={'nome': 'João Silva', 'cpf': '123.456.789-01'})
        self.assertTrue(form.is_valid())

    def test_visita_form_invalid_empty(self):
        form = VisitaForm(data={})
        self.assertFalse(form.is_valid())

class VisitaMoradorViewsTest(VisitaBaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username='morador1@test.com', password='pass')

    def test_cadastrar_visita_sucesso(self):
        response = self.client.post(reverse('visita:cadastrar_visita'), {
            'nome': 'Maria Souza',
            'cpf': '000.000.000-00'
        })
        self.assertEqual(response.status_code, 302)
        visita = Visita.objects.get(nome='Maria Souza')
        self.assertEqual(visita.morador, self.morador1)

    def test_lista_visitas_morador_privacidade(self):
        # Visita do morador 1
        Visita.objects.create(morador=self.morador1, nome='Visita M1', cpf='1')
        # Visita do morador 2
        Visita.objects.create(morador=self.morador2, nome='Visita M2', cpf='2')
        
        response = self.client.get(reverse('visita:lista_visitas_morador'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Visita M1')
        self.assertNotContains(response, 'Visita M2')

class VisitaFuncionarioViewsTest(VisitaBaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username='func1@test.com', password='pass')
        self.visita = Visita.objects.create(morador=self.morador1, nome='Visitante Func', cpf='999')

    def test_lista_visitas_func_scope(self):
        # Visita do mesmo condomínio
        Visita.objects.create(morador=self.morador2, nome='Vizinho', cpf='888')
        
        # Criar visita de OUTRO condomínio (Admin 2)
        user_m3 = User.objects.create_user(username='m3@test.com', password='pass')
        apt3 = Apartamento.objects.create(bloco='B', andar='1', numero='201')
        m3 = Morador.objects.create(user=user_m3, cpf='77', telefone='1', tipo_morador=Morador.TipoMorador.PROPRIETARIO, administrador=self.admin2, apartamento=apt3)
        Visita.objects.create(morador=m3, nome='Visitante Outro Cond', cpf='777')

        response = self.client.get(reverse('visita:lista_visitas_func'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Visitante Func')
        self.assertContains(response, 'Vizinho')
        self.assertNotContains(response, 'Visitante Outro Cond')

    def test_registrar_entrada_sucesso(self):
        response = self.client.post(reverse('visita:registrar_entrada', args=[self.visita.id]))
        self.assertEqual(response.status_code, 302)
        
        self.visita.refresh_from_db()
        self.assertEqual(self.visita.status, Visita.StatusVisita.REGISTRADA)
        self.assertIsNotNone(self.visita.data_entrada)
        self.assertEqual(self.visita.funcionario, self.func1)

    def test_registrar_entrada_seguranca_outro_condominio(self):
        # Login como funcionário do Admin 2
        self.client.login(username='func2@test.com', password='pass')
        # Tentar registrar entrada de visita do Admin 1
        response = self.client.post(reverse('visita:registrar_entrada', args=[self.visita.id]))
        self.assertEqual(response.status_code, 404)
        
        self.visita.refresh_from_db()
        self.assertEqual(self.visita.status, Visita.StatusVisita.AGENDADA)

class VisitaAdminViewsTest(VisitaBaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username='admin1@test.com', password='pass')

    def test_lista_visitas_adm_scope(self):
        Visita.objects.create(morador=self.morador1, nome='Visita Adm', cpf='111')
        
        # Visita de outro condomínio
        user_m3 = User.objects.create_user(username='m3_adm@test.com', password='pass')
        m3 = Morador.objects.create(user=user_m3, cpf='88', telefone='1', tipo_morador=Morador.TipoMorador.PROPRIETARIO, administrador=self.admin2, apartamento=Apartamento.objects.create(bloco='C', numero='1'))
        Visita.objects.create(morador=m3, nome='Invisivel', cpf='222')

        response = self.client.get(reverse('visita:lista_visitas_adm'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Visita Adm')
        self.assertNotContains(response, 'Invisivel')
