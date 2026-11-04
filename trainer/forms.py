from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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


class SighUpForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': "you@example.com",
            }
        ),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Введите имя пользователя',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Придумайте пароль',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Повторите пароль',
            }
        )