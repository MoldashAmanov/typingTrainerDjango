from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from trainer import views as trainer_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'accounts/register/',
        trainer_views.register,
        name='register',
        ),
    path(
        'accounts/login/', 
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login',
        ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(
            next_page='trainer:home'
        ),
        name='logout',
    ),
    path('', include('trainer.urls')),
]