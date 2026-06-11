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
                'rows': 3
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

            # 🔹 Validação de conflito de horário
            if fim:
                conflito = Reserva.objects.filter(
                    horario_inicio__lt=fim,
                    horario_fim__gt=inicio
                ).exists()
                if conflito:
                    raise forms.ValidationError("Já existe uma reserva nesse horário.")

        return cleaned_data
