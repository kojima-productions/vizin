from django import forms
from .models import Visita

class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['nome', 'cpf']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'input-field', 
                'placeholder': 'Nome completo do visitante'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'input-field', 
                'placeholder': '000.000.000-00',
                'id': 'cpf_field'
            }),
        }
