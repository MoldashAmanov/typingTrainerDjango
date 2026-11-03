from django import forms
from .models import PracticeText, PracticeResult


class PracticeStartForm(forms.Form):
    language = forms.ChoiceField(
        label='Язык',
        choices=PracticeText.Language.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    custom_text = forms.CharField(
        label='Свой текст',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Вставьте или напишите свой текст для тренировки',
            }
        ),
        required=False,
        max_length=7000,
    )

    saved_text = forms.ModelChoiceField(
        label='Готовый текст',
        queryset=PracticeText.objects.filter(is_active=True),
        required=False,
        empty_label='- Не использовать -',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        custom_text = cleaned_data.get('custom_text', '').strip()
        saved_text = cleaned_data.get('saved_text')

        if not custom_text and not saved_text:
            raise forms.ValidationError(
                'Выберите готовый текст или введите свой текст'
            )

        return cleaned_data


class PracticeResultForm(forms.ModelForm):
    class Meta:
        model = PracticeResult
        fields = [
            'language',
            'source_text',
            'typed_text',
            'duration_seconds',
            'characters',
            'correct_characters',
            'incorrect_characters',
            'accuracy',
            'wpm',
            'cpm',
        ]