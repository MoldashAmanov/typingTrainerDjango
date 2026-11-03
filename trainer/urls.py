from django.urls import path

from . import views


app_name = 'trainer'

urlpatterns = [
    path('', views.home, name='home'),
    path('practice/', views.practice, name='practice'),
    path('results/save/', views.save_result, name='save_results'),
    path('history/', views.history, name='history'),
]