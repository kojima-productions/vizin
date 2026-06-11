from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from apps.administrador.models import Administrador
from apps.funcionario.models import Funcionario


class FuncionarioViewsTest(TestCase):

    def setUp(self):
        """
        Cria um administrador e um funcionário
        que serão utilizados nos testes.
        """
        self.admin_user = User.objects.create_user(
            username='admin@email.com',
            email='admin@email.com',
            password='12345678'
        )

        self.administrador = Administrador.objects.create(
            user=self.admin_user,
            cpf='12345678901'
        )

        self.func_user = User.objects.create_user(
            username='func@email.com',
            email='func@email.com',
            password='12345678',
            first_name='João'
        )

        self.funcionario = Funcionario.objects.create(
            user=self.func_user,
            cpf='11111111111',
            telefone='81999999999',
            cargo='Porteiro',
            administrador=self.administrador
        )

    def test_login_funcionario_sucesso(self):
        """
        Um funcionário com credenciais válidas
        deve conseguir realizar login.
        """
        response = self.client.post(
            reverse('funcionario:login'),
            {
                'login': 'func@email.com',
                'senha': '12345678'
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_login_funcionario_senha_incorreta(self):
        """
        Senha inválida não deve autenticar
        o funcionário.
        """
        response = self.client.post(
            reverse('funcionario:login'),
            {
                'login': 'func@email.com',
                'senha': 'senha_errada'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Credenciais inválidas.')

    def test_login_usuario_sem_perfil_funcionario(self):
        """
        Mesmo autenticando no sistema,
        um usuário sem perfil de funcionário
        não deve acessar a área do funcionário.
        """
        usuario_comum = User.objects.create_user(
            username='comum@email.com',
            email='comum@email.com',
            password='12345678'
        )

        response = self.client.post(
            reverse('funcionario:login'),
            {
                'login': 'comum@email.com',
                'senha': '12345678'
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            'Usuário autenticado não possui perfil de Funcionário.'
        )

    def test_painel_funcionario_logado(self):
        """
        Funcionário autenticado deve acessar
        normalmente o painel.
        """
        self.client.login(
            username='func@email.com',
            password='12345678'
        )

        response = self.client.get(
            reverse('funcionario:painel')
        )

        self.assertEqual(response.status_code, 200)

    def test_painel_exige_login(self):
        """
        Usuários não autenticados devem ser
        redirecionados para login.
        """
        response = self.client.get(
            reverse('funcionario:painel')
        )

        self.assertEqual(response.status_code, 302)

    def test_usuario_comum_nao_acessa_painel(self):
        """
        Usuários autenticados sem perfil
        de funcionário devem receber 403.
        """
        usuario_comum = User.objects.create_user(
            username='comum@email.com',
            email='comum@email.com',
            password='12345678'
        )

        self.client.login(
            username='comum@email.com',
            password='12345678'
        )

        response = self.client.get(
            reverse('funcionario:painel')
        )

        self.assertEqual(response.status_code, 403)

    def test_lista_funcionarios_redireciona_para_administrador(self):
        """
        A rota antiga foi mantida apenas para
        compatibilidade e deve redirecionar.
        """
        self.client.login(
            username='func@email.com',
            password='12345678'
        )

        response = self.client.get(
            reverse('funcionario:lista_funcionarios')
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            response.url,
            reverse('administrador:lista_funcionarios')
        )

    def test_cadastrar_funcionario_redireciona_para_administrador(self):
        """
        A criação de funcionários foi movida
        para o módulo de administrador.
        """
        self.client.login(
            username='func@email.com',
            password='12345678'
        )

        response = self.client.get(
            reverse('funcionario:cadastrar_funcionario')
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            response.url,
            reverse('administrador:cadastrar_funcionario')
        )