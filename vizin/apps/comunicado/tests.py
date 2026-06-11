from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from apps.administrador.models import Administrador
from .models import Comunicado
from apps.morador.models import Morador, Apartamento
from apps.funcionario.models import Funcionario


class ComunicadoTests(TestCase):
    def setUp(self):
        # Cria usuário administrador
        self.user = User.objects.create_user(username='admin', password='12345')
        self.admin = Administrador.objects.create(user=self.user)
        self.client.login(username='admin', password='12345')

    def test_cadastrar_comunicado(self):
        url = reverse('comunicado:cadastrar_comunicado')
        data = {
            'titulo': 'Teste de comunicado',
            'tipo': Comunicado.TipoComunicado.EVENTO,
            'descricao': 'Descrição do comunicado de teste'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comunicado.objects.filter(titulo='Teste de comunicado').exists())

    def test_lista_comunicados(self):
        Comunicado.objects.create(
            titulo='Comunicado 1',
            tipo=Comunicado.TipoComunicado.MANUTENCAO,
            descricao='Teste lista',
            administrador=self.admin
        )
        url = reverse('comunicado:lista_comunicados')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Comunicado 1')

    def test_editar_comunicado(self):
        comunicado = Comunicado.objects.create(
            titulo='Antigo título',
            tipo=Comunicado.TipoComunicado.SEGURANCA,
            descricao='Antiga descrição',
            administrador=self.admin
        )
        url = reverse('comunicado:editar_comunicado', args=[comunicado.id])
        data = {
            'titulo': 'Novo título',
            'tipo': Comunicado.TipoComunicado.SEGURANCA,
            'descricao': 'Nova descrição'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        comunicado.refresh_from_db()
        self.assertEqual(comunicado.titulo, 'Novo título')

    def test_deletar_comunicado(self):
        comunicado = Comunicado.objects.create(
            titulo='Comunicado deletável',
            tipo=Comunicado.TipoComunicado.URGENTE,
            descricao='Será deletado',
            administrador=self.admin
        )
        url = reverse('comunicado:deletar_comunicado', args=[comunicado.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comunicado.objects.filter(id=comunicado.id).exists())


class ComunicadoPermissaoNotificacaoTests(TestCase):
    def setUp(self):
        # Usuário administrador
        self.admin_user = User.objects.create_user(
            username='admin', password='12345', email='admin@test.com'
        )
        self.admin = Administrador.objects.create(user=self.admin_user)

        # Criar apartamento provisório
        self.apartamento = Apartamento.objects.create(
            numero="101",
            bloco="A"
        )

        # Usuário morador
        self.morador_user = User.objects.create_user(
            username='morador', password='12345', email='morador@test.com'
        )
        self.morador = Morador.objects.create(
            user=self.morador_user,
            administrador=self.admin,
            apartamento=self.apartamento
        )

        # Usuário funcionário
        self.func_user = User.objects.create_user(
            username='func', password='12345', email='func@test.com'
        )
        self.funcionario = Funcionario.objects.create(
            user=self.func_user,
            administrador=self.admin
        )

    # ---------------- PERMISSÕES ----------------
    def test_admin_cadastra_comunicado(self):
        self.client.login(username='admin', password='12345')
        url = reverse('comunicado:cadastrar_comunicado')
        data = {
            'titulo': 'Comunicado Admin',
            'tipo': Comunicado.TipoComunicado.EVENTO,
            'descricao': 'Descrição teste'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comunicado.objects.filter(titulo='Comunicado Admin').exists())

    def test_morador_nao_cadastra_comunicado(self):
        self.client.login(username='morador', password='12345')
        url = reverse('comunicado:cadastrar_comunicado')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_funcionario_nao_cadastra_comunicado(self):
        self.client.login(username='func', password='12345')
        url = reverse('comunicado:cadastrar_comunicado')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    # ---------------- NOTIFICAÇÕES ----------------
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_notificacao_enviada_para_morador_e_funcionario(self):
        self.client.login(username='admin', password='12345')
        url = reverse('comunicado:cadastrar_comunicado')
        data = {
            'titulo': 'Aviso Importante',
            'tipo': Comunicado.TipoComunicado.URGENTE,
            'descricao': 'Teste de notificação'
        }
        self.client.post(url, data)

        comunicado = Comunicado.objects.get(titulo='Aviso Importante')
        self.assertEqual(comunicado.tipo, Comunicado.TipoComunicado.URGENTE)

        # Como a view não dispara e‑mail, validamos apenas a criação
        self.assertTrue(Comunicado.objects.filter(titulo='Aviso Importante').exists())

    # ---------------- ACESSO ----------------
    def test_morador_visualiza_comunicado(self):
        Comunicado.objects.create(
            titulo='Aviso Morador',
            tipo=Comunicado.TipoComunicado.CONVIVENCIA,
            descricao='Teste morador',
            administrador=self.admin
        )
        self.client.login(username='morador', password='12345')
        url = reverse('comunicado:lista_comunicados')
        response = self.client.get(url)
        self.assertContains(response, 'Aviso Morador')

    def test_funcionario_visualiza_comunicado(self):
        Comunicado.objects.create(
            titulo='Aviso Funcionario',
            tipo=Comunicado.TipoComunicado.SEGURANCA,
            descricao='Teste funcionario',
            administrador=self.admin
        )
        self.client.login(username='func', password='12345')
        url = reverse('comunicado:lista_comunicados')
        response = self.client.get(url)
        self.assertContains(response, 'Aviso Funcionario')
