from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

from apps.morador.models import Morador, Veiculo, Reclamacao
from apps.administrador.models import Administrador
from apps.funcionario.models import Funcionario

class ReclamacaoForm(forms.ModelForm):
    class Meta:
        model = Reclamacao
        fields = ['tipo', 'descricao']
        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'input-field',
                'id': 'id_tipo'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'input-field',
                'placeholder': 'Descreva aqui o problema...',
                'id': 'id_descricao',
                'rows': 4
            }),
        }

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['modelo', 'cor', 'placa', 'tipo']
        widgets = {
            'modelo': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Ex: Civic',
                'id': 'id_modelo'
            }),
            'cor': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Ex: Preto',
                'id': 'id_cor'
            }),
            'placa': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Ex: ABC1D23',
                'id': 'id_placa'
            }),
            'tipo': forms.Select(attrs={
                'class': 'input-field',
                'id': 'id_tipo'
            }),
        }

    def clean_placa(self):
        placa = self.cleaned_data.get('placa', '').upper()
        if len(placa) != 7:
            raise ValidationError('A placa deve ter exatamente 7 caracteres.')
        return placa


class MoradorForm(forms.Form):
    nome = forms.CharField(max_length=100, required=True)
    cpf = forms.CharField(max_length=14, required=True, label='CPF')
    email = forms.EmailField(required=True)
    telefone = forms.CharField(max_length=15, required=True)
    senha = forms.CharField(min_length=8, widget=forms.PasswordInput, required=True)

    tipo_morador = forms.ChoiceField(choices=Morador.TipoMorador.choices, required=True)

    bloco = forms.CharField(max_length=5, required=True)
    andar = forms.CharField(max_length=3, required=True)
    numero = forms.CharField(max_length=10, required=True)

    def _only_digits(self, value):
        return re.sub(r"\D", "", value or "")

    def clean_cpf(self):
        cpf_raw = self.cleaned_data.get('cpf') or ''
        cpf = self._only_digits(cpf_raw)
        if not cpf:
            raise ValidationError('CPF é obrigatório.')
        if len(cpf) != 11:
            raise ValidationError('CPF deve ter exatamente 11 dígitos numéricos.')
        if Morador.objects.filter(cpf=cpf).exists() or Funcionario.objects.filter(cpf=cpf).exists() or Administrador.objects.filter(cpf=cpf).exists():
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


class MoradorEditForm(forms.Form):
    nome = forms.CharField(max_length=100, required=True)
    cpf = forms.CharField(max_length=14, required=True, label='CPF')
    email = forms.EmailField(required=True)
    telefone = forms.CharField(max_length=15, required=True)
    senha = forms.CharField(min_length=8, widget=forms.PasswordInput, required=False, help_text="Deixe em branco para não alterar.")

    tipo_morador = forms.ChoiceField(choices=Morador.TipoMorador.choices, required=True)

    bloco = forms.CharField(max_length=5, required=True)
    andar = forms.CharField(max_length=3, required=True)
    numero = forms.CharField(max_length=10, required=True)

    def __init__(self, *args, **kwargs):
        self.morador_id = kwargs.pop('morador_id', None)
        super().__init__(*args, **kwargs)

    def _only_digits(self, value):
        return re.sub(r"\D", "", value or "")

    def clean_cpf(self):
        cpf_raw = self.cleaned_data.get('cpf') or ''
        cpf = self._only_digits(cpf_raw)
        if not cpf:
            raise ValidationError('CPF é obrigatório.')
        
        if len(cpf) != 11:
            raise ValidationError('CPF deve ter exatamente 11 dígitos numéricos.')

        # Verifica se o CPF pertence a outro usuário
        if Morador.objects.filter(cpf=cpf).exclude(id=self.morador_id).exists() or \
           Funcionario.objects.filter(cpf=cpf).exists() or \
           Administrador.objects.filter(cpf=cpf).exists():
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
        email = (self.cleaned_data.get('email') or '').strip().lower()
        # Verifica se o email pertence a outro User
        morador = Morador.objects.get(id=self.morador_id)
        if User.objects.filter(email__iexact=email).exclude(id=morador.user.id).exists():
            raise ValidationError('E-mail já cadastrado.')
        return email


class MoradorLoginForm(forms.Form):
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
