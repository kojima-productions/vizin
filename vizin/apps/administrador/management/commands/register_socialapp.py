import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

# Load .env variables if present
from dotenv import load_dotenv
load_dotenv()

class Command(BaseCommand):
    help = 'Registra um SocialApp para Google usando variáveis OAUTH_ID e OAUTH_KEY do .env/ambiente'

    def handle(self, *args, **options):
        try:
            from django.contrib.sites.models import Site
            from allauth.socialaccount.models import SocialApp
        except Exception as e:
            raise CommandError(f'Erro importando modelos necessários: {e}')

        client_id = os.environ.get('OAUTH_ID')
        client_secret = os.environ.get('OAUTH_KEY')
        if not client_id or not client_secret:
            raise CommandError('Variáveis OAUTH_ID e OAUTH_KEY não encontradas no ambiente ou .env')

        site_id = getattr(settings, 'SITE_ID', 1)
        try:
            site = Site.objects.get(id=site_id)
        except Site.DoesNotExist:
            raise CommandError(f'Site com id={site_id} não existe. Crie um site via admin e ajuste SITE_ID.')

        app, created = SocialApp.objects.update_or_create(
            provider='google',
            defaults={'name': 'Google', 'client_id': client_id, 'secret': client_secret}
        )
        # Associar ao site
        app.sites.set([site])
        app.save()

        if created:
            self.stdout.write(self.style.SUCCESS('SocialApp criado e associado ao site.'))
        else:
            self.stdout.write(self.style.SUCCESS('SocialApp atualizado e associado ao site.'))
