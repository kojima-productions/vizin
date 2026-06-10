from django import forms
from .models import Comunicado

class ComunicadoForm(forms.ModelForm):
    class Meta:
        model = Comunicado
        fields = ['titulo', 'tipo', 'descricao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Título do comunicado'}),
            'tipo': forms.Select(attrs={'class': 'input-field'}),
            'descricao': forms.Textarea(attrs={'class': 'input-field', 'placeholder': 'Descrição detalhada', 'rows': 4}),
        }
