from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from apps.morador.models import Morador, Apartamento
from apps.administrador.models import Administrador


class MoradorViewsTest(TestCase):

    def setUp(self):
        """
        Cria um administrador, um apartamento
        e um morador para utilização nos testes.
        """
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
            cpf='99999999999',
            telefone='81999999999',
            tipo_morador=Morador.TipoMorador.PROPRIETARIO,
            administrador=self.administrador,
            apartamento=self.apartamento
        )

    def test_login_morador_sucesso(self):
        """
        Morador com credenciais válidas
        deve conseguir acessar o sistema.
        """
        response = self.client.post(
            reverse('morador:login'),
            {
                'login': 'morador@email.com',
                'senha': '12345678'
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_login_morador_invalido(self):
        """
        Senha incorreta não deve permitir login.
        """
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
        """
        Usuário autenticado mas sem perfil
        de morador deve ser bloqueado.
        """
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
        """
        Morador autenticado deve acessar
        normalmente o painel.
        """
        self.client.login(
            username='morador@email.com',
            password='12345678'
        )

        response = self.client.get(
            reverse('morador:painel')
        )

        self.assertEqual(response.status_code, 200)

    def test_painel_exige_login(self):
        """
        Usuários não autenticados devem ser
        redirecionados para login.
        """
        response = self.client.get(
            reverse('morador:painel')
        )

        self.assertEqual(response.status_code, 302)

    def test_usuario_comum_nao_acessa_painel(self):
        """
        Usuários sem perfil de morador
        devem receber erro 403.
        """
        usuario_comum = User.objects.create_user(
            username='comum@email.com',
            password='12345678'
        )

        self.client.login(
            username='comum@email.com',
            password='12345678'
        )

        response = self.client.get(
            reverse('morador:painel')
        )

        self.assertEqual(response.status_code, 403)

    def test_deletar_usuario_remove_morador(self):
        """
        Como existe CASCADE, ao remover o User
        o Morador também deve ser removido.
        """
        self.user_morador.delete()

        self.assertFalse(
            Morador.objects.filter(
                id=self.morador.id
            ).exists()
        )

    def test_relacionamento_morador_apartamento(self):
        """
        Verifica se o morador está associado
        ao apartamento correto.
        """
        self.assertEqual(
            self.morador.apartamento.numero,
            '101'
        )

        self.assertEqual(
            self.morador.apartamento.bloco,
            'A'
        )