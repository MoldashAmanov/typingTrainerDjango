# TypingTrainer

Учебный веб-тренажёр слепой печати на Django.

## Возможности

- Практика свободного текста на английском и русском языках
- Ввод собственного текста или выбор готового текста
- Подсчёт WPM, CPM, точности и ошибок
- Посимвольная подсветка правильного и неправильного ввода
- Сохранение истории тренировок для авторизованных пользователей
- Административная панель для управления текстами и результатами

## Технологии

- Python
- Django
- SQLite
- HTML, CSS, JavaScript

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

## Что демонстрирует проект

- Работа с моделями и миграциями Django
- Формы и валидация данных
- Session-based flow между страницами
- Интеграция JavaScript с Django-шаблонами
- Сохранение результатов через POST-форму
