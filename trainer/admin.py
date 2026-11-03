from django.contrib import admin

from .models import PracticeText, PracticeResult


@admin.register(PracticeText)
class PracticeTextAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'word_count', 'is_active', 'created_at')
    list_filter = ('language', 'is_active')
    search_fields = ('title', 'content')
    list_editable = ('is_active',)


@admin.register(PracticeResult)
class PracticeResultAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'language',
        'wpm',
        'cpm',
        'accuracy',
        'duration_seconds',
        'created_at',
    )
    list_filter = ('language', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = (
        'source_text',
        'typed_text',
        'duration_seconds',
        'characters',
        'correct_characters',
        'incorrect_characters',
        'accuracy',
        'wpm',
        'cpm',
    )