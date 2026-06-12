from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from apps.administrador.models import Administrador
from apps.morador.models import Morador, Apartamento
from apps.funcionario.models import Funcionario
from .models import Comunicado
from .forms import ComunicadoForm

class ComunicadoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin_model@test.com', password='password')
        self.admin = Administrador.objects.create(user=self.user, cpf='99999999999')

    def test_comunicado_creation(self):
        """Verifica a criação do modelo e sua representação em string."""
        comunicado = Comunicado.objects.create(
            titulo='Aviso de Teste',
            descricao='Esta é uma descrição de teste.',
            tipo='Urgente',
            administrador=self.admin
        )
        self.assertEqual(comunicado.titulo, 'Aviso de Teste')
        self.assertEqual(comunicado.tipo, 'Urgente')
        self.assertEqual(str(comunicado), f"Comunicado: Aviso de Teste | {comunicado.data}")

class ComunicadoFormTest(TestCase):
    def test_comunicado_form_valid(self):
        """Valida o formulário com dados corretos."""
        form_data = {
            'titulo': 'Manutenção Elevador',
            'tipo': 'Manutenção',
            'descricao': 'O elevador A estará em manutenção amanhã.'
        }
        form = ComunicadoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comunicado_form_invalid(self):
        """Valida falha no formulário com dados ausentes ou inválidos."""
        form_data = {
            'titulo': '', # Obrigatório
            'tipo': 'Inexistente', # Choice inválida
            'descricao': 'Descrição'
        }
        form = ComunicadoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('titulo', form.errors)
        self.assertIn('tipo', form.errors)

class ComunicadoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Admin 1 e seus dados
        self.user_admin1 = User.objects.create_user(username='admin1@test.com', email='admin1@test.com', password='password')
        self.admin1 = Administrador.objects.create(user=self.user_admin1, cpf='11111111111')
        
        # Admin 2 (para teste de isolamento)
        self.user_admin2 = User.objects.create_user(username='admin2@test.com', email='admin2@test.com', password='password')
        self.admin2 = Administrador.objects.create(user=self.user_admin2, cpf='22222222222')
        
        # Morador vinculado ao Admin 1
        self.apt = Apartamento.objects.create(bloco='A', andar='1', numero='101')
        self.user_morador = User.objects.create_user(username='morador@test.com', email='morador@test.com', password='password')
        self.morador = Morador.objects.create(
            user=self.user_morador, 
            cpf='33333333333', 
            telefone='11111111111', 
            tipo_morador='Proprietario', 
            administrador=self.admin1, 
            apartamento=self.apt
        )
        
        # Funcionário vinculado ao Admin 1
        self.user_func = User.objects.create_user(username='func@test.com', email='func@test.com', password='password')
        self.funcionario = Funcionario.objects.create(
            user=self.user_func, 
            cpf='44444444444', 
            telefone='22222222222', 
            cargo='Zelador', 
            administrador=self.admin1
        )
        
        # Comunicados para teste
        self.comunicado1 = Comunicado.objects.create(titulo='C1 Admin1', descricao='D1', tipo='Urgente', administrador=self.admin1)
        self.comunicado2 = Comunicado.objects.create(titulo='C2 Admin2', descricao='D2', tipo='Evento', administrador=self.admin2)

    def test_lista_comunicados_admin_access(self):
        """Admin deve ver apenas seus próprios comunicados."""
        self.client.login(username='admin1@test.com', password='password')
        response = self.client.get(reverse('comunicado:lista_comunicados'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'C1 Admin1')
        self.assertNotContains(response, 'C2 Admin2')

    def test_lista_comunicados_morador_access(self):
        """Morador deve ver apenas comunicados do seu administrador."""
        self.client.login(username='morador@test.com', password='password')
        response = self.client.get(reverse('comunicado:lista_comunicados'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'C1 Admin1')
        self.assertNotContains(response, 'C2 Admin2')

    def test_lista_comunicados_funcionario_access(self):
        """Funcionário deve ver apenas comunicados do seu administrador."""
        self.client.login(username='func@test.com', password='password')
        response = self.client.get(reverse('comunicado:lista_comunicados'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'C1 Admin1')
        self.assertNotContains(response, 'C2 Admin2')

    def test_cadastrar_comunicado_admin_success(self):
        """Administrador cadastra comunicado com sucesso."""
        self.client.login(username='admin1@test.com', password='password')
        response = self.client.post(reverse('comunicado:cadastrar_comunicado'), {
            'titulo': 'Novo Comunicado',
            'tipo': 'Segurança',
            'descricao': 'Teste de cadastro'
        })
        self.assertEqual(response.status_code, 302) # Redirect após sucesso
        self.assertTrue(Comunicado.objects.filter(titulo='Novo Comunicado', administrador=self.admin1).exists())

    def test_cadastrar_comunicado_morador_denied(self):
        """Moradores não têm permissão para cadastrar comunicados (403)."""
        self.client.login(username='morador@test.com', password='password')
        response = self.client.get(reverse('comunicado:cadastrar_comunicado'))
        self.assertEqual(response.status_code, 403)

    def test_editar_comunicado_admin_success(self):
        """Administrador edita seu próprio comunicado."""
        self.client.login(username='admin1@test.com', password='password')
        response = self.client.post(reverse('comunicado:editar_comunicado', args=[self.comunicado1.id]), {
            'titulo': 'Título Atualizado',
            'tipo': 'Urgente',
            'descricao': 'Descrição'
        })
        self.assertEqual(response.status_code, 302)
        self.comunicado1.refresh_from_db()
        self.assertEqual(self.comunicado1.titulo, 'Título Atualizado')

    def test_editar_comunicado_other_admin_404(self):
        """Admin não pode acessar comunicado de outro admin (404)."""
        self.client.login(username='admin2@test.com', password='password')
        response = self.client.get(reverse('comunicado:editar_comunicado', args=[self.comunicado1.id]))
        self.assertEqual(response.status_code, 404)

    def test_deletar_comunicado_post_success(self):
        """Exclusão via POST deve retornar JSON de sucesso."""
        self.client.login(username='admin1@test.com', password='password')
        response = self.client.post(reverse('comunicado:deletar_comunicado', args=[self.comunicado1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'ok': True})
        self.assertFalse(Comunicado.objects.filter(id=self.comunicado1.id).exists())

    def test_deletar_comunicado_get_fail(self):
        """Exclusão via GET deve ser negada (405)."""
        self.client.login(username='admin1@test.com', password='password')
        response = self.client.get(reverse('comunicado:deletar_comunicado', args=[self.comunicado1.id]))
        self.assertEqual(response.status_code, 405)

    def test_deletar_comunicado_morador_denied(self):
        """Morador não pode deletar comunicados."""
        self.client.login(username='morador@test.com', password='password')
        response = self.client.post(reverse('comunicado:deletar_comunicado', args=[self.comunicado1.id]))
        self.assertEqual(response.status_code, 403)
