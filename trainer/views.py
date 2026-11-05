from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Avg, Count, Max, Sum
from django.contrib.auth import login
from django.contrib import messages
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

from .forms import PracticeResultForm, PracticeStartForm, SighUpForm
from .models import PracticeResult, PracticeText


def home(request):
    form = PracticeStartForm()
    recent_texts = PracticeText.objects.filter(is_active=True)[:6]

    context = {
        'form': form,
        'recent_texts': recent_texts,
    }

    return render(request, 'trainer/home.html', context)


def practice(request):
    if request.method == 'POST':
        form = PracticeStartForm(request.POST)

        if form.is_valid():
            custom_text = form.cleaned_data['custom_text'].strip()
            saved_text = form.cleaned_data['saved_text']
            language = form.cleaned_data['language']

            if custom_text:
                source_text = custom_text
                title = 'Свободная практика'
            else:
                source_text = saved_text.content
                title = saved_text.title
                language = saved_text.language

            request.session['practice_source'] = source_text
            request.session['practice_language'] = language
            request.session['practice_title'] = title

            return redirect('trainer:practice')

    else:
        source_text = request.session.get('practice_source')
        language = request.session.get('practice_language')
        title = request.session.get('practice_title', 'Свободная практика')

        if not source_text:
            return redirect('trainer:home')

        form = PracticeStartForm(
            initial={
                'language': language,
            }
        )

    context = {
        'form': form,
        'source_text': source_text,
        'language': language,
        'title': title,
    }
    return render(request, 'trainer/practice.html', context)


def recalculate_result_metrics(result):
    source_text = result.source_text or ''
    typed_text = result.typed_text or ''

    correct = 0
    incorrect = 0

    for index, typed_char in enumerate(typed_text):
        if index >= len(source_text):
            incorrect += 1
            continue

        if typed_char == source_text[index]:
            correct += 1
        else:
            incorrect += 1

    checked_characters = correct + incorrect
    accuracy = (
        round((correct / checked_characters) * 100, 2)
        if checked_characters
        else 100.00
    )

    duration_seconds = max(result.duration_seconds or 0, 0)
    minutes = duration_seconds / 60

    cpm = round(len(typed_text) / minutes, 2) if minutes > 0 else 0
    words = len([word for word in typed_text.split() if word])
    wpm = round(words / minutes, 2) if minutes > 0 else 0

    result.characters = len(typed_text)
    result.correct_characters = correct
    result.incorrect_characters = incorrect
    result.accuracy = accuracy
    result.cpm = cpm
    result.wpm = wpm

    return result

@require_POST
def save_result(request):
    form = PracticeResultForm(request.POST)

    if not form.is_valid():
        return JsonResponse(
            {
                'ok': False,
                'errors': form.errors,
            },
            status=400,
        )
    result = form.save(commit=False)

    if request.user.is_authenticated:
        result.user = request.user

    result = recalculate_result_metrics(result)
    result.save()

    messages.success(request, 'Результат тренировки сохранен')

    return JsonResponse(
        {
            'ok': True,
            'redirect_url': reverse('trainer:result_detail', args=[result.pk]),
        }
    )


def result_detail(request, result_id):
    result = get_object_or_404(PracticeResult, pk=result_id)

    if result.user and result.user != request.user:
        return redirect('trainer:home')

    context = {
        'result': result,
    }
    return render(request, 'trainer/result_detail.html', context)


@login_required
def history(request):
    results = (
        request.user.practice_results
        .select_related('practice_text')
        .order_by('created_at')
    )

    recent_results = list(results.reverse()[:20])

    stats = request.user.practice_results.aggregate(
        total_results = Count('id'),
        best_wpm = Max('wpm', default=0),
        average_wpm = Avg('wpm', default=0),
        average_accuracy = Avg('accuracy', default=0),
        average_cpm = Avg('cpm', default=0),
        total_duration = Sum('duration_seconds', default=0),
    )

    english_stats = request.user.practice_results.filter(
        language = PracticeText.Language.ENGLISH
    ).aggregate(
        total_results = Count('id'),
        best_wpm = Max('wpm', default=0),
        average_accuracy = Avg('accuracy', default=0),
    )

    russian_stats = request.user.practice_results.filter(
        language = PracticeText.Language.RUSSIAN
    ).aggregate(
        total_results = Count('id'),
        best_wpm = Max('wpm', default=0),
        average_accuracy = Avg('accuracy', default=0),
    )

    chart_data = {
        'labels': [
            result.created_at.strftime('%d.%m %H:%M')
            for result in results
        ],
        'wpm': [float(result.wpm) for result in results],
        'accuracy': [float(result.accuracy) for result in results],
    }

    context = {
        'results': recent_results,
        'stats': stats,
        'english_stats': english_stats,
        'russian_stats': russian_stats,
        'chart_data': chart_data,
    }

    return render(request, 'trainer/history.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('trainer:home')

    if request.method == "POST":
        form = SighUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                'Аккаунт создан. Добро пожаловать!'
            )

            return redirect('trainer:home')
    else:
        form = SighUpForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)


@login_required
def delete_result(request, result_id):
    result = get_object_or_404(
        PracticeResult,
        pk=result_id,
        user=request.user,
    )

    if request.method == 'POST':
        result.delete()
        messages.success(request, 'Тренировка удалена')
        return redirect('trainer:history')

    return render(
        request,
        'trainer/result_confirm_delete.html',
        {'result': result},
    )


@login_required
def reset_history(request):
    results = request.user.practice_results.all()
    total = results.count()

    if request.method == 'POST':
        if request.POST.get('confirm') != 'RESET':
            messages.error(request, 'Для сброса введите слово RESET')
            return render(
                request,
                'trainer/history_confirm_reset.html',
                {'total': total},
            )

        results.delete()
        messages.success(request, 'История сброшена. Удалено тренировок: {total}')
        return redirect('trainer:history')

    return render(
        request,
        'trainer/history_confirm_reset.html',
        {'total': total},
    )