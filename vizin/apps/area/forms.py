from django import forms
from django.utils import timezone
from .models import Area, Reserva

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

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['horario_inicio', 'horario_fim', 'motivo']
        widgets = {
            'horario_inicio': forms.DateTimeInput(attrs={
                'class': 'input-field',
                'type': 'datetime-local',
                'id': 'id_horario_inicio'
            }),
            'horario_fim': forms.DateTimeInput(attrs={
                'class': 'input-field',
                'type': 'datetime-local',
                'id': 'id_horario_fim'
            }),
            'motivo': forms.Textarea(attrs={
                'class': 'input-field',
                'placeholder': 'Motivo da reserva (ex: Aniversário)',
                'id': 'id_motivo',
                'rows': 4
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('horario_inicio')
        fim = cleaned_data.get('horario_fim')
        agora = timezone.now()

        if inicio:
            if inicio < agora:
                raise forms.ValidationError("Não é possível realizar uma reserva para uma data/hora que já passou.")
            
            if fim and inicio >= fim:
                raise forms.ValidationError("O horário de início deve ser anterior ao horário de término.")
        
        return cleaned_data
