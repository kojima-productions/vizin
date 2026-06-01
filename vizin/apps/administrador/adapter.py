from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.db import transaction

class AdministradorSocialAdapter(DefaultSocialAccountAdapter):
    """Adapter que garante a criação atômica do User e do Administrador.

    Ele espera que o formulário de signup social (signup) forneça 'cpf' em form.cleaned_data.
    """

    def save_user(self, request, sociallogin, form=None):
        # sociallogin.user is a User instance (unsaved in some flows)
        user = sociallogin.user
        cpf = None
        if form and hasattr(form, 'cleaned_data'):
            cpf = form.cleaned_data.get('cpf')

        # Execute em uma transação única para salvar user e administrador atomically
        from django.contrib.auth import get_user_model
        User = get_user_model()
        from .models import Administrador

        with transaction.atomic():
            # Delega ao super para aplicar comportamento padrão de salvar o user (preenche campos, etc.)
            user = super().save_user(request, sociallogin, form)
            if cpf:
                # cria Administrador ligado ao user recém-criado
                Administrador.objects.create(user=user, cpf=cpf)

        return user
