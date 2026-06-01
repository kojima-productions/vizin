import re
from django import forms
from .models import Administrador

class AdministradorSocialSignupForm(forms.Form):
    cpf = forms.CharField(max_length=20, label='CPF')

    def clean_cpf(self):
        cpf_raw = self.cleaned_data.get('cpf', '')
        cpf = re.sub(r'\D', '', cpf_raw)
        if len(cpf) != 11:
            raise forms.ValidationError('CPF inválido. Forneça 11 dígitos numéricos.')
        if Administrador.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError('CPF já cadastrado.')
        # normalize value back into cleaned_data
        self.cleaned_data['cpf'] = cpf
        return cpf

    # allauth will call save in adapter; the form does not need save() here
