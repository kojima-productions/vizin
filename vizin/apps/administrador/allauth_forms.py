import re
from django import forms
from .models import Administrador

class AdministradorSocialSignupForm(forms.Form):
    cpf = forms.CharField(
        max_length=20, 
        label='CPF',
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Somente números (11 dígitos)'})
    )

    def __init__(self, *args, sociallogin=None, **kwargs):
        """Accept sociallogin kwarg that allauth passes when instantiating the form.

        Store sociallogin for potential use (not required here) and call super.
        """
        self.sociallogin = sociallogin
        super().__init__(*args, **kwargs)

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

    def save(self, request, user=None):
        return user

    def try_save(self, request):
        sociallogin = getattr(self, 'sociallogin', None)
        if sociallogin is None:
            return None, None
        from allauth.socialaccount.adapter import get_adapter as get_social_adapter
        user = get_social_adapter().save_user(request, sociallogin, form=self)
        return user, None
