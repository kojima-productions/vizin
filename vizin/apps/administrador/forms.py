from django import forms
from django.contrib.auth.models import User
from .models import Administrador, Comunicado

class AdministradorRegistrationForm(forms.Form):
    nome = forms.CharField(
        max_length=150,
        label='Nome',
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Seu nome completo',
            'id': 'id_nome'
        })
    )
    cpf = forms.CharField(
        max_length=11,
        label='CPF',
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Somente números (11 dígitos)',
            'id': 'id_cpf'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'input-field',
            'placeholder': 'seu@email.com',
            'id': 'id_email'
        })
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Senha',
            'id': 'id_senha'
        }),
        label='Senha'
    )

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf', '').strip()
        if not cpf.isdigit() or len(cpf) != 11:
            raise forms.ValidationError('CPF deve conter 11 dígitos numéricos.')
        if Administrador.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError('CPF já cadastrado.')
        return cpf

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Email já cadastrado.')
        return email

class AdministradorLoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'input-field',
            'placeholder': 'seu@email.com',
            'id': 'id_email'
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
