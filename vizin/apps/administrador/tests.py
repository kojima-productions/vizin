from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import json


from apps.administrador.models import Administrador
from apps.funcionario.models import Funcionario
from apps.morador.models import Morador, Apartamento
from apps.area.models import Area, Reserva


class AdministradorViewsTest(TestCase):

    def setUp(self):
        """
        Cria um administrador que será utilizado na maioria
        dos testes e configura o client HTTP do Django.
        """
        self.client = Client()

        self.user_admin = User.objects.create_user(
            username='admin@email.com',
            email='admin@email.com',
            password='12345678'
        )

        self.admin = Administrador.objects.create(
            user=self.user_admin,
            cpf='12345678901'
        )

    def test_registro_administrador_sucesso(self):
        """
        Verifica se o cadastro cria corretamente
        um User e um Administrador.
        """
        response = self.client.post(
            reverse('administrador:registro'),
            {
                'nome': 'Novo Admin',
                'cpf': '98765432100',
                'email': 'novo@email.com',
                'senha': '12345678'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            User.objects.filter(
                email='novo@email.com'
                ).exists()
        )

        self.assertTrue(
            Administrador.objects.filter(
                cpf='98765432100'
                ).exists()
        )

    def test_login_administrador_sucesso(self):
        """
        Garante que um administrador válido
        consiga acessar o sistema.
        """
        response = self.client.post(
            reverse('administrador:login'),
            {
                'email': 'admin@email.com',
                'senha': '12345678'
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_painel_exige_login(self):
        """
        Usuários não autenticados devem ser
        redirecionados para a tela de login.
        """
        response = self.client.get(
            reverse('administrador:painel')
        )

        self.assertEqual(response.status_code, 302)

    def test_painel_administrador_logado(self):
        """
        Um administrador autenticado deve
        acessar normalmente o painel.
        """
        self.client.login(
            username='admin@email.com',
            password='12345678'
        )

        response = self.client.get(
            reverse('administrador:painel')
        )

        self.assertEqual(response.status_code, 200)

    def test_cadastrar_funcionario(self):
        """
        Verifica a criação de funcionário
        vinculada ao administrador logado.
        """
        self.client.login(
            username='admin@email.com',
            password='12345678',
    )

        response = self.client.post(
            reverse('administrador:cadastrar_funcionario'),
            {
                'nome': 'João',
                'email': 'func@email.com',
                'senha': '12345678',
                'cpf': '11111111111',
                'telefone': '81999999999',
                'cargo': 'Porteiro'
            }
    )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Funcionario.objects.filter(
                cpf='11111111111'
            ).exists()
    )

    def test_lista_funcionarios(self):
        """
        Garante que o administrador consiga
        visualizar seus funcionários.
        """
        funcionario_user = User.objects.create_user(
            username='func@email.com',
            password='12345678'
        )

        Funcionario.objects.create(
            user=funcionario_user,
            cpf='11111111111',
            telefone='81999999999',
            cargo='Porteiro',
            administrador=self.admin
        )

        self.client.login(
            username='admin@email.com',
            password='12345678'
        )

        response = self.client.get(
            reverse('administrador:lista_funcionarios')
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Porteiro')

    def test_cadastrar_morador(self):
        """
        Deve criar automaticamente o apartamento
        e associá-lo ao morador.
        """
        self.client.login(
            username='admin@email.com',
            password='12345678'
        )

        response = self.client.post(
            reverse('administrador:cadastrar_morador'),
            {
                'nome': 'Maria',
                'email': 'maria@email.com',
                'senha': '12345678',
                'cpf': '22222222222',
                'telefone': '81888888888',
                'tipo_morador': 'Proprietario',
                'bloco': 'A',
                'andar': '1',
                'numero': '101'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Morador.objects.count(),
        1
        )

        self.assertEqual(
            Apartamento.objects.count(),
        1
        )

    def test_lista_moradores(self):
        """
        Verifica se a listagem retorna os
        moradores cadastrados.
        """
        apartamento = Apartamento.objects.create(
            bloco='A',
            andar='1',
            numero='101'
        )

        morador_user = User.objects.create_user(
            username='morador@email.com',
            password='12345678'
        )

        Morador.objects.create(
            user=morador_user,
            cpf='22222222222',
            telefone='81888888888',
            tipo_morador='Proprietario',
            administrador=self.admin,
            apartamento=apartamento
        )

        self.client.login(
            username='admin@email.com',
            password='12345678'
        )

        response = self.client.get(
            reverse('administrador:lista_moradores')
        )

        self.assertEqual(response.status_code, 200)

    def test_deletar_funcionario(self):
        """
        A exclusão deve remover o funcionário
        e o usuário associado.
        """
        funcionario_user = User.objects.create_user(
            username='func@email.com',
            password='12345678'
        )

        funcionario = Funcionario.objects.create(
            user=funcionario_user,
            cpf='11111111111',
            telefone='81999999999',
            cargo='Porteiro',
            administrador=self.admin
        )

        self.client.login(
            username='admin@email.com',
            password='12345678'
        )

        response = self.client.post(
            reverse(
                'administrador:deletar_funcionario',
                args=[funcionario.id]
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Funcionario.objects.filter(
                id=funcionario.id
            ).exists()
        )

    def test_deletar_morador(self):
        """
        A exclusão deve remover o morador
        e o usuário associado.
        """
        apartamento = Apartamento.objects.create(
            bloco='A',
            andar='1',
            numero='101'
        )

        morador_user = User.objects.create_user(
            username='morador@email.com',
            password='12345678'
        )

        morador = Morador.objects.create(
            user=morador_user,
            cpf='22222222222',
            telefone='81888888888',
            tipo_morador='Proprietario',
            administrador=self.admin,
            apartamento=apartamento
        )

        self.client.login(
            username='admin@email.com',
            password='12345678'
)

        response = self.client.post(
            reverse(
                'administrador:deletar_morador',
                args=[morador.id]
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Morador.objects.filter(
                id=morador.id
            ).exists()
        )

    def test_registro_administrador_cpf_duplicado(self):
        """
        Não deve permitir cadastrar dois administradores
        com o mesmo CPF.
        """
        response = self.client.post(
            reverse('administrador:registro'),
            {
                'nome': 'Outro Admin',
                'cpf': '12345678901',  # CPF já utilizado no setUp
                'email': 'outro@email.com',
                'senha': '12345678'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CPF já cadastrado.')

        self.assertEqual(
            Administrador.objects.filter(cpf='12345678901').count(),
            1
        )


    def test_registro_administrador_email_duplicado(self):
        """
        Não deve permitir cadastrar dois usuários
        com o mesmo e-mail.
        """
        response = self.client.post(
            reverse('administrador:registro'),
            {
                'nome': 'Outro Admin',
                'cpf': '99999999999',
                'email': 'admin@email.com',  # Email do setUp
                'senha': '12345678'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email já cadastrado.')

        self.assertEqual(
            User.objects.filter(email='admin@email.com').count(),
            1
        )


    def test_login_invalido(self):
        """
        Credenciais incorretas devem impedir
        a autenticação do usuário.
        """
        response = self.client.post(
            reverse('administrador:login'),
            {
                'email': 'admin@email.com',
                'senha': 'senha_errada'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Credenciais inválidas.')


    def test_usuario_comum_nao_acessa_painel(self):
        """
        Usuários autenticados sem perfil de administrador
        devem receber erro de permissão.
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
            reverse('administrador:painel')
        )

        self.assertEqual(response.status_code, 403)


    def test_usuario_comum_nao_cadastra_funcionario(self):
        """
        Apenas administradores podem cadastrar
        funcionários.
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
            reverse('administrador:cadastrar_funcionario')
        )

        self.assertEqual(response.status_code, 403)


    def test_usuario_comum_nao_cadastra_morador(self):
        """
        Apenas administradores podem cadastrar
        moradores.  
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
            reverse('administrador:cadastrar_morador')
        )

        self.assertEqual(response.status_code, 403)

class AdministradorReservaTest(TestCase):

    def setUp(self):
        self.user_admin = User.objects.create_user(
            username='admin',
            password='12345678'
        )

        self.admin = Administrador.objects.create(
            user=self.user_admin,
            cpf='12345678901'
        )

        self.user_morador = User.objects.create_user(
            username='morador',
            password='12345678'
        )

        self.apartamento = Apartamento.objects.create(
            bloco='A',
            andar='1',
            numero='101'
        )

        self.morador = Morador.objects.create(
            user=self.user_morador,
            cpf='22222222222',
            telefone='81999999999',
            tipo_morador='Proprietario',
            administrador=self.admin,
            apartamento=self.apartamento
        )

        self.area = Area.objects.create(
            nome="Salão de Festas",
            regras="Sem bagunça",
            taxa_reserva=100,
            administrador=self.admin
        )

        self.inicio = timezone.now() + timedelta(days=1)
        self.fim = self.inicio + timedelta(hours=2)

        self.reserva = Reserva.objects.create(
            horario_inicio=self.inicio,
            horario_fim=self.fim,
            motivo="Evento",
            area=self.area,
            morador=self.morador,
            administrador=self.admin,
            status=Reserva.Status.ABERTO
        )
    def test_aprovar_reserva(self):
        self.reserva.status = Reserva.Status.APROVADO
        self.reserva.save()

        self.reserva.refresh_from_db()

        self.assertEqual(self.reserva.status, Reserva.Status.APROVADO)

    def test_negar_reserva(self):
        self.reserva.status = Reserva.Status.NEGADO
        self.reserva.save()

        self.reserva.refresh_from_db()

        self.assertEqual(self.reserva.status, Reserva.Status.NEGADO)

    def test_admin_nao_pode_alterar_area_de_outro(self):
        outro_user = User.objects.create_user(
            username='admin2',
            password='12345678'
        )

        outro_admin = Administrador.objects.create(
            user=outro_user,
            cpf='98765432100'
        )

        self.client.login(username='admin2', password='12345678')
        response = self.client.post(
            reverse('administrador:validar_reserva', args=[self.reserva.id]),
            data=json.dumps({'acao': 'aprovar'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)
        self.reserva.refresh_from_db()
        self.assertEqual(self.reserva.status, Reserva.Status.ABERTO)
