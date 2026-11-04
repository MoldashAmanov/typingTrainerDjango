from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Avg
from django.contrib.auth import login
from django.contrib import messages

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


@require_POST
def save_result(request):
    form = PracticeResultForm(request.POST)

    if form.is_valid():
        result = form.save(commit=False)

        if request.user.is_authenticated:
            result.user = request.user

        result.save()
        return redirect('trainer:history')

    return redirect('trainer:home')


@login_required
def history(request):
    results = request.user.practice_results.all()[:20]

    total_results = request.user.practice_results.count()

    if total_results:
        best_wpm = request.user.practice_results.order_by('-wpm').first().wpm
        average_accuracy = (
            request.user.practice_results.aggregate(
                accuracy=Avg('accuracy')
            )['accuracy']
        )
    else:
        best_wpm = 0
        average_accuracy = 0

    context = {
        'results': results,
        'total_results': total_results,
        'best_wpm': best_wpm,
        'average_accuracy': average_accuracy or 0,
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