from django import forms
from apps.encomenda.models import Encomenda
from apps.morador.models import Apartamento

class EncomendaForm(forms.ModelForm):
    class Meta:
        model = Encomenda
        fields = ['apartamento', 'descricao']
        widgets = {
            'apartamento': forms.Select(attrs={
                'class': 'input-field',
                'id': 'id_apartamento'
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Ex: Pacote da Amazon, Envelope, etc.',
                'id': 'id_descricao'
            }),
        }

    def __init__(self, *args, **kwargs):
        administrador = kwargs.pop('administrador', None)
        super().__init__(*args, **kwargs)
        if administrador:
            # Filter apartments linked to residents of this administrator
            self.fields['apartamento'].queryset = Apartamento.objects.filter(
                morador__administrador=administrador
            ).distinct().order_by('bloco', 'numero')
