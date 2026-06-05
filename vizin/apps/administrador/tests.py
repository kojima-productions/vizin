from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Administrador
class AdministradorModelTest(TestCase):

    def test_criar_administrador(self):
        user = User.objects.create_user(
            username='admin@email.com',
            email='admin@email.com',
            password='admin123'
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
            reverse('administrador:painel')
        )
        self.assertEqual(response.status_code, 302)  # Redirecionamento para a página de login
        # Verifica se o redirecionamento é para a página de login


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
            email='admin@email.com',
            password='admin123'
        )

        response = self.client.get(
            reverse('administrador:painel')
        )
        self.assertEqual(response.status_code, 200)  # Acesso permitido ao painel


# Create your tests here.
