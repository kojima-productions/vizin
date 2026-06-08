from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

from apps.funcionario.models import Funcionario
from apps.administrador.models import Administrador


class FuncionarioForm(forms.Form):
    nome = forms.CharField(max_length=100, required=True)
    cpf = forms.CharField(max_length=14, required=True, label='CPF')  # aceita formatos com pontos/traços
    email = forms.EmailField(required=True)
    telefone = forms.CharField(max_length=15, required=True)  # aceita formatos com espaços/()-+
    cargo = forms.CharField(max_length=100, required=True)
    senha = forms.CharField(min_length=8, widget=forms.PasswordInput, required=True)

    def _only_digits(self, value):
        return re.sub(r"\D", "", value or "")

    def clean_cpf(self):
        cpf_raw = self.cleaned_data.get('cpf') or ''
        cpf = self._only_digits(cpf_raw)
        if not cpf:
            raise ValidationError('CPF é obrigatório.')
        if len(cpf) != 11:
            raise ValidationError('CPF deve ter exatamente 11 dígitos numéricos.')
        if Funcionario.objects.filter(cpf=cpf).exists() or Administrador.objects.filter(cpf=cpf).exists():
            raise ValidationError('CPF já cadastrado.')
        return cpf

    def clean_telefone(self):
        tel_raw = self.cleaned_data.get('telefone') or ''
        tel = self._only_digits(tel_raw)
        if not tel:
            raise ValidationError('Telefone é obrigatório.')
        if len(tel) < 10 or len(tel) > 11:
            raise ValidationError('Telefone deve ter entre 10 e 11 dígitos numéricos.')
        return tel

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('E-mail já cadastrado.')
        return email.lower()


class FuncionarioLoginForm(forms.Form):
    login = forms.EmailField(
        label='Login',
        widget=forms.EmailInput(attrs={
            'class': 'input-field',
            'placeholder': 'seu@email.com',
            'id': 'id_login'
        })
    )
    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Senha',
            'id': 'id_senha'
        })
    )
