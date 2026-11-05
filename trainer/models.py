from django.db import models
from django.conf import settings


class PracticeText(models.Model):
    class Language(models.TextChoices):
        ENGLISH = "en", "Английский"
        RUSSIAN = "ru", "Русский"

    title = models.CharField("Название", max_length=200)
    language = models.CharField(
        "Язык",
        max_length=2,
        choices=Language.choices,
        default=Language.RUSSIAN,
    )
    content = models.TextField("Текст для практики")
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "Текст для практики"
        verbose_name_plural = "Тексты для практики"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_language_display()})"

    @property
    def word_count(self):
        return len(self.content.split())



class PracticeResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="practice_results",
        verbose_name="Пользователь",
        null=True,
        blank=True,
    )
    language = models.CharField(
        "Язык",
        max_length=2,
        choices=PracticeText.Language.choices,
    )
    source_text = models.TextField("Исходный текст")
    typed_text = models.TextField("Введенный текст")
    duration_seconds = models.PositiveIntegerField("Длительность, сек")
    characters = models.PositiveIntegerField("Символов введено")
    correct_characters = models.PositiveIntegerField("Верных символов")
    incorrect_characters = models.PositiveIntegerField("Ошибочных символов")
    accuracy = models.DecimalField(
        "Точность, %",
        max_digits=5,
        decimal_places=2,
        default=0,
    )
    wpm = models.DecimalField(
        "Слов в минуту",
        max_digits=6,
        decimal_places=2,
        default=0,
    )
    cpm = models.DecimalField(
        "Символов в минуту",
        max_digits=7,
        decimal_places=2,
        default=0,
    )
    created_at = models.DateTimeField("Дата тренировки", auto_now_add=True)
    practice_text = models.ForeignKey(
        PracticeText,
        on_delete=models.SET_NULL,
        related_name='results',
        verbose_name='Использованный текст',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Результат тренировки"
        verbose_name_plural = "Результаты тренировок"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Тренировка #{self.pk} - {self.language.upper()} - {self.wpm} WPM"
