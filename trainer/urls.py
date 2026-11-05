from django.urls import path

from . import views


app_name = 'trainer'

urlpatterns = [
    path('', views.home, name='home'),
    path('practice/', views.practice, name='practice'),
    path('results/save/', views.save_result, name='save_result'),
    path('history/', views.history, name='history'),
    path(
        'results/<int:result_id>/',
        views.result_detail,
        name='result_detail',
    ),
]