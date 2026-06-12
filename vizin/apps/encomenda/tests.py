from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from apps.administrador.models import Administrador
from apps.funcionario.models import Funcionario
from apps.morador.models import Morador, Apartamento
from .models import Encomenda


class EncomendaTests(TestCase):
    def setUp(self):
        # Usuário administrador
        self.admin_user = User.objects.create_user(
            username='admin', password='12345', email='admin@test.com'
        )
        self.administrador = Administrador.objects.create(user=self.admin_user)

        # Apartamento
        self.apartamento = Apartamento.objects.create(numero="101", bloco="A")

        # Usuário morador (com administrador obrigatório)
        self.morador_user = User.objects.create_user(
            username='morador', password='12345', email='morador@test.com'
        )
        self.morador = Morador.objects.create(
            user=self.morador_user,
            apartamento=self.apartamento,
            administrador=self.administrador
        )

        # Usuário funcionário (também vinculado ao administrador)
        self.func_user = User.objects.create_user(
            username='func', password='12345', email='func@test.com'
        )
        self.funcionario = Funcionario.objects.create(
            user=self.func_user,
            administrador=self.administrador
        )

    # ---------------- CADASTRO ----------------
    def test_funcionario_cadastra_encomenda(self):
        self.client.login(username='func', password='12345')
        url = reverse('encomenda:cadastrar_encomenda')
        data = {
            'apartamento': self.apartamento.id,
            'descricao': 'Pacote da Amazon'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Encomenda.objects.filter(descricao='Pacote da Amazon').exists())

    def test_morador_nao_cadastra_encomenda(self):
        self.client.login(username='morador', password='12345')
        url = reverse('encomenda:cadastrar_encomenda')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    # ---------------- LISTAGEM ----------------
    def test_lista_encomendas_func(self):
        Encomenda.objects.create(
            apartamento=self.apartamento,
            descricao='Documento',
            registrado_por=self.func_user
        )
        self.client.login(username='func', password='12345')
        url = reverse('encomenda:lista_encomendas_func')
        response = self.client.get(url)
        self.assertContains(response, 'Documento')

    def test_lista_encomendas_morador(self):
        Encomenda.objects.create(
            apartamento=self.apartamento,
            descricao='Revista',
            registrado_por=self.func_user
        )
        self.client.login(username='morador', password='12345')
        url = reverse('encomenda:lista_encomendas_morador')
        response = self.client.get(url)
        self.assertContains(response, 'Revista')

    # ---------------- ENTREGA ----------------
    def test_funcionario_registra_entrega(self):
        encomenda = Encomenda.objects.create(
            apartamento=self.apartamento,
            descricao='Pacote',
            registrado_por=self.func_user
        )
        self.client.login(username='func', password='12345')
        url = reverse('encomenda:registrar_entrega', args=[encomenda.id])
        response = self.client.post(url)
        encomenda.refresh_from_db()
        self.assertEqual(encomenda.status, Encomenda.Status.ENTREGUE)
        self.assertEqual(response.status_code, 302)

    def test_morador_nao_registra_entrega(self):
        encomenda = Encomenda.objects.create(
            apartamento=self.apartamento,
            descricao='Livro',
            registrado_por=self.func_user
        )
        self.client.login(username='morador', password='12345')
        url = reverse('encomenda:registrar_entrega', args=[encomenda.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    # ---------------- CASOS EXTRAS ----------------
    def test_nao_registra_entrega_duplicada(self):
        encomenda = Encomenda.objects.create(
            apartamento=self.apartamento,
            descricao='Caixa',
            registrado_por=self.func_user,
            status=Encomenda.Status.ENTREGUE
        )
        self.client.login(username='func', password='12345')
        url = reverse('encomenda:registrar_entrega', args=[encomenda.id])
        response = self.client.post(url)
        encomenda.refresh_from_db()
        self.assertEqual(encomenda.status, Encomenda.Status.ENTREGUE)
        self.assertEqual(response.status_code, 302)

    def test_funcionario_nao_cadastra_em_apartamento_de_outro_adm(self):
        outro_apartamento = Apartamento.objects.create(numero="202", bloco="B")
        self.client.login(username='func', password='12345')
        url = reverse('encomenda:cadastrar_encomenda')
        data = {
            'apartamento': outro_apartamento.id,
            'descricao': 'Pacote indevido'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # volta para o form
        self.assertFalse(Encomenda.objects.filter(descricao='Pacote indevido').exists())

    def test_lista_encomendas_ordem_por_data(self):
        # Força timestamps diferentes
        encomenda1 = Encomenda.objects.create(
            apartamento=self.apartamento,
            descricao='Primeira',
            registrado_por=self.func_user
        )
        encomenda1.data_chegada = timezone.now()
        encomenda1.save()

        encomenda2 = Encomenda.objects.create(
            apartamento=self.apartamento,
            descricao='Segunda',
            registrado_por=self.func_user
        )
        encomenda2.data_chegada = timezone.now() + timezone.timedelta(seconds=5)
        encomenda2.save()

        self.client.login(username='func', password='12345')
        url = reverse('encomenda:lista_encomendas_func')
        response = self.client.get(url)
        encomendas = response.context['encomendas']

        # Agora garantimos que 'Segunda' vem primeiro
        self.assertEqual(encomendas[0].descricao, 'Segunda')
        self.assertEqual(encomendas[1].descricao, 'Primeira')
