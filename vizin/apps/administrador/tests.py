from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
import random
from .models import Administrador
from .models import Funcionario
class AdministradorModelTest(TestCase):

    def test_criar_administrador(self):
        user = User.objects.create_user(
            id = random.randint(1, 10),
            username='admin@email.com',
            email='admin@email.com',
            password='admin123',
            first_name='nome'
        )

        administrador = Administrador.objects.create(
            user=user,
            cpf='12345678901'
        )

        self.assertEqual(
            administrador.cpf,
            '12345678901'
        )

        self.assertEqual(
            administrador.user.username,
            'admin@email.com'
        )

        print(administrador.user.username)
        print(administrador.cpf)
        print(administrador.user.first_name)
        print(administrador.user.email)
        


class RegistroAdministradorTest(TestCase):

    def test_deve_cadastrar_administrador(self):
        response = self.client.post(
            reverse('administrador:registro'), 
            {
            'nome': 'administrador teste',
            'cpf': '12345678901',
            'email': 'admin@email.com',
            'senha': 'admin123456'
        }
    )

        self.assertEqual(response.status_code, 302)  
        # Redirecionamento após registro bem-sucedido

        self.assertTrue(
            User.objects.filter(
                email='admin@email.com'
                ).exists()
            )  # Verifica se o usuário foi criado

        self.assertTrue(
            Administrador.objects.filter(
                cpf='12345678901'
            ).exists()
        )  # Verifica se o administrador foi criado

class LoginAdministradorTest(TestCase):
    
    def test_login_valido(self):
        user = User.objects.create_user(
            username='admin@email.com',
            email='admin@email.com',
            password='admin123'
        )

        Administrador.objects.create(
            user=user,
            cpf='12345678901'
        )

        response = self.client.post(
            reverse('administrador:login'), 
            {
                'email': 'admin@email.com',
                'senha': 'admin123'
            }
        )
        self.assertEqual(response.status_code, 302)  
        # Redirecionamento após login bem-sucedido

    def test_login_invalido(self):
        response = self.client.post(
            reverse('administrador:login'), 
            {
                'email': 'admin@email.com',
                'senha': 'admin123456'
            }
        )
        
        self.assertContains(
            response, 
            'Credenciais inválidas. Por favor, tente novamente.'
        )   
        # Verifica se a mensagem de erro é exibida



class PainelAdministradorTest(TestCase):
    
    def test_acesso_sem_login(self):
        response = self.client.get(
            reverse('administrador:painel'),
            follow=True
        )
          # Redirecionamento para a página de login
        # Verifica se o redirecionamento é para a página de login
        print(response.redirect_chain)

    def test_acesso_com_login(self):

        user = User.objects.create_user(
            username='admin@email.com',
            email='admin@email.com',
            password='admin123'
        )

        Administrador.objects.create(
            user=user,
            cpf='12345678901'
        )

        self.client.login(
            username='admin@email.com',
            password='admin123'
        )

        response = self.client.get(
            reverse('administrador:painel'),
            follow=True
        ) 
         # Acesso permitido ao painel
        print(response.redirect_chain)
        self.assertEqual(response.status_code, 200)
class updateAdministradorTest(TestCase):

    def test_atualizar_informacoes(self):
        user = User.objects.create_user(
            username='admin@email.com',
            email='admins@email.com',
            password='admin123'
        )
        administrador = Administrador.objects.create(
            user=user,
            cpf='12345678901'
        )
        self.client.login(  
            username='admins@email.com',
            password='admin123'
        )
        
        print(self.client.login(
            username='admin',
            password='123456'
        )
        )
        response = self.client.post(
            reverse('administrador:update'), 
            {
                'nome': 'Administrador Atualizado',
                'cpf': '12345678901',
                'email': 'admins@email.com'
            }
        )
        self.assertEqual(response.status_code, 302)  
        # Redirecionamento após atualização bem-sucedida
        administrador.refresh_from_db()
        # Atualiza o objeto do banco de dados
        self.assertEqual(
            administrador.user.username,
            'Administrador Atualizado'
        )

class DeleteAdministradorTest(TestCase):

    def test_deletar_administrador(self):
        user = User.objects.create_user(
            id= random.randint(1, 10),
            username='admin@email.com',
            email='admin@email.com',
            password='admin123'
        )
        administrador = Administrador.objects.create(
            user=user,
            cpf='12345678901'
        )
        self.client.login(
            username='admin@email.com',
            password='admin123'
        )
        response = self.client.post(
            reverse('administrador:delete', kwargs={'id': administrador.id})
        )
        self.assertEqual(response.status_code, 302)  # Redirecionamento após exclusão bem-sucedida
        self.assertFalse(
            Administrador.objects.filter(id=administrador.id).exists()
        )  # Verifica se o administrador foi excluído

class AdministradorGerenciaMoradorTest(TestCase):
    def test_cadastrar_morador(self):
        user = User.objects.create_user(
            id= random.randint(1, 1000),
            username='morador@email.com',
            email='morador@email.com',
            password='morador123'
        )
        administrador = Administrador.objects.create(
            user=user,
            cpf='12345678901'
        )
        self.client.login(
            username='admin@email.com',
            password='admin123'
        )
        response = self.client.post(
            reverse('administrador:cadastrar_morador'), 
            {
                'nome': 'Morador Teste',
                'cpf': '12345678901',
                'email': 'morador@email.com',
                'senha': 'morador123456'
            }
        )
        self.assertEqual(response.status_code, 302)
        # Redirecionamento após cadastro bem-sucedido
        self.assertTrue(
            User.objects.filter(email='morador@email.com').exists()
        )  # Verifica se o usuário do morador foi criado
        self.assertTrue(
            Administrador.objects.filter(cpf='12345678901').exists()
        )  # Verifica se o morador foi criado

    def test_listar_moradores(self):
        user = User.objects.create_user(
            id= random.randint(1, 1000),
            username='morador@email.com',
            email='morador@email.com',
            password='morador123'
        )
        administrador = Administrador.objects.create(
            user=user,
            cpf='12345678901'
        )
        self.client.login(
            username='admin@email.com',
            password='admin123'
        )
        response = self.client.get(
            reverse('administrador:listar_moradores')
        )
        self.assertEqual(response.status_code, 200)
        # Verifica se a lista de moradores é exibida corretamente
        self.assertContains(response, 'Morador Teste')

    def test_atualizar_morador(self):
        user = User.objects.create_user(
            id= random.randint(1, 1000),
            username='morador@email.com',
            email='morador@email.com',
            password='morador123'
        )
        administrador = Administrador.objects.create(
            user=user,
            cpf='12345678901'
        )
        self.client.login(
            username='admin@email.com',
            password='admin123'
        )
        response = self.client.post(
            reverse('administrador:update_morador', kwargs={'id': administrador.id}), 
            {
                'nome': 'Morador Atualizado',
                'cpf': '12345678901',
                'email': 'morador@email.com'
            }
        )
        self.assertEqual(response.status_code, 302)
        # Redirecionamento após atualização bem-sucedida
        administrador.refresh_from_db()
        # Atualiza o objeto do banco de dados
        self.assertEqual(
            administrador.user.username,
            'Morador Atualizado'
        )

    def test_deletar_morador(self):
        user = User.objects.create_user(
            id= random.randint(1, 1000),
            username='morador@email.com',
            email='morador@email.com',
            password='morador123'
        )
        administrador = Administrador.objects.create(
            user=user,
            cpf='12345678901'
        )
        self.client.login(
            username='admin@email.com',
            password='admin123'
        )
        response = self.client.post(
            reverse('administrador:delete_morador', kwargs={'id': administrador.id})
        )
        self.assertEqual(response.status_code, 302)  # Redirecionamento após exclusão bem-sucedida
        self.assertFalse(
            Administrador.objects.filter(id=administrador.id).exists()
        )  # Verifica se o morador foi excluído

class AdministradorGerenciaFuncionarioTest(TestCase):
    
    def test_cadastrar_funcionario(self):
        user = User.objects.create_user(
            id= random.randint(1, 1000),
            username='funcionario@email.com',
            email='funcionario@email.com',
            password='funcionario123'
        )
        self.client.login(
            username='admin@email.com',
            password='admin123'
        )
        response = self.client.post(
            reverse('administrador:cadastrar_funcionario'), 
            {
                'nome': 'Funcionário Teste',
                'cpf': '12345678901',
                'email': 'funcionario@email.com',
                'senha': 'funcionario123456'
            }
        )
        self.assertEqual(response.status_code, 302)
        # Redirecionamento após cadastro bem-sucedido
        self.assertTrue(
            User.objects.filter(email='funcionario@email.com').exists()
        )  # Verifica se o usuário do funcionário foi criado
        self.assertTrue(
            Administrador.objects.filter(cpf='12345678901').exists()
        )  # Verifica se o funcionário foi criado

    def test_listar_funcionarios(self):
        user = User.objects.create_user(
            id= random.randint(1, 1000),
            username='funcionario@email.com',
            email='funcionario@email.com',
            password='funcionario123'
        )
        administrador = Administrador.objects.create(
            user=user,
            cpf='12345678901'
        )
        self.client.login(
            username='admin@email.com',
            password='admin123'
        )
        response = self.client.get(
            reverse('administrador:listar_funcionarios')
        )
        self.assertEqual(response.status_code, 200)
        # Verifica se a lista de funcionário é exibida corretamente
        self.assertContains(response, 'Funcionário Teste')

    def test_atualizar_funcionario(self):
        user = User.objects.create_user(
            id= random.randint(1, 1000),
            username='funcionario@email.com',
            email='funcionario@email.com',
            password='funcionario123'
        )
        administrador = Administrador.objects.create(
            user=user,
            cpf='12345678901'
        )
        self.client.login(
            username='admin@email.com',
            password='admin123'
        )
        response = self.client.post(
            reverse('administrador:update_funcionario', kwargs={'id': administrador.id}), 
            {
                'nome': 'Funcionário Atualizado',
                'cpf': '12345678901',
                'email': 'funcionario@email.com'
            }
        )
        self.assertEqual(response.status_code, 302)
        # Redirecionamento após atualização bem-sucedida
        administrador.refresh_from_db()
        # Atualiza o objeto do banco de dados
        self.assertEqual(
            administrador.user.username,
            'Funcionário Atualizado'
        )

    def test_deletar_funcionario(self):
        user = User.objects.create_user(
            id= random.randint(1, 1000),
            username='funcionario@email.com',
            email='funcionario@email.com',
            password='funcionario123'
        )
        administrador = Administrador.objects.create(
            user=user,
            cpf='12345678901'
        )
        self.client.login(
            username='admin@email.com',
            password='admin123'
        )
        response = self.client.post(
            reverse('administrador:delete_funcionario', kwargs={'id': administrador.id})
        )
        self.assertEqual(response.status_code, 302)  # Redirecionamento após exclusão bem-sucedida
        self.assertFalse(
            Administrador.objects.filter(id=administrador.id).exists()
        )  # Verifica se o funcionário foi excluído
        
class AdministradorAutorizaReservaTest(TestCase):
    
    def test_autorizar_reserva(self):
        user = User.objects.create_user(
            id= random.randint(1, 1000),
            username='admin@email.com',
            password='admin123'
        )

        administrador = Administrador.objects.create(
            user=user,
            cpf='12345678901'
        )

        self.client.login(
            username='admin@email.com',
            password='admin123'
        )

        response = self.client.post(
            reverse('administrador:autorizar_reserva', kwargs={'id': administrador.id}), 
            {
                'status': 'autorizada'
            }
        )
        self.assertEqual(response.status_code, 302)  
        # Redirecionamento após autorização bem-sucedida
        # Verifica se a reserva foi autorizada corretamente
        administrador.refresh_from_db()
        self.assertEqual(administrador.status, 'autorizada')

class AdministradorRegistraOcorrenciaTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin@email.com',
            email='admin@email.com',
            password='admin123'
        )

        self.administrador = Administrador.objects.create(
            user=self.user,
            cpf='12345678901'
        )

        self.client.login(
            username='admin@email.com',
            password='admin123'
        )

    def test_registrar_ocorrencia(self):
    
        response = self.client.post(
            reverse('administrador:registrar_ocorrencia', kwargs={'id': self.administrador.id}), 
            {
                'descricao': 'Ocorrência de teste',
                'tipo': 'Incidente'
            }
        )
        self.assertEqual(response.status_code, 302)  
        # Redirecionamento após registro bem-sucedido
        # Verifica se a ocorrência foi registrada corretamente
        self.assertTrue(
            self.administrador.ocorrencias.filter(
                descricao='Ocorrência de teste',
                tipo='Incidente'
            ).exists()
        )

        self.administrador.refresh_from_db()
        self.assertEqual(self.administrador.ocorrencias.count(), 1)
        ocorrencia = self.administrador.ocorrencias.first()
        self.assertEqual(ocorrencia.descricao, 'Ocorrência de teste')
        self.assertEqual(ocorrencia.tipo, 'Incidente')

class AdministradorDefineEscalaTest(TestCase):

    def setUp(self):
        user_admin = User.objects.create_user(
            username='admin@email.com',
            password='admin123'
        )

        self.administrador = Administrador.objects.create(
            user=user_admin,
            cpf='12345678901'
        )

        user_funcionario = User.objects.create_user(
            username='funcionario@email.com',
            password='funcionario123'
        )

        self.funcionario = Funcionario.objects.create(
            user=user_funcionario,
            cpf='12345678901',
            telefone='1234567890',
            cargo='Porteiro',
            administrador=self.administrador
        )

        self.client.login(
            username='admin@email.com',
            password='admin123'
        )
    def test_definir_escala(self):
        response = self.client.post(
            reverse('administrador:definir_escala', kwargs={'id': self.administrador.id}),
            {
                'funcionario_id': self.funcionario.id,
                'data': '2024-01-01',
                'turno': 'Manhã',
                'hora_inicio': '08:00',
                'hora_fim': '12:00',
            }
        )

        self.assertEqual(response.status_code, 302)
        # Redirecionamento após definição bem-sucedida
        # Verifica se a escala foi definida corretamente
        self.assertTrue(
            self.administrador.escalas.filter(
                id_funcionario=self.funcionario.id,
                data='2024-01-01',
                turno='Manhã',
                hora_inicio='08:00',
                hora_fim='12:00'
            ).exists()
        )