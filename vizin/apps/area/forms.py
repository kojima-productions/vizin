from django import forms
from .models import Area

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nome', 'regras', 'taxa_reserva']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Nome da área (ex: Piscina)',
                'id': 'id_nome'
            }),
            'regras': forms.Textarea(attrs={
                'class': 'input-field',
                'placeholder': 'Regras de uso',
                'id': 'id_regras',
                'rows': 4
            }),
            'taxa_reserva': forms.NumberInput(attrs={
                'class': 'input-field',
                'placeholder': '0.00',
                'id': 'id_taxa_reserva',
                'step': '0.01'
            }),
        }
