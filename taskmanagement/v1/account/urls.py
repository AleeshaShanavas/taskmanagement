from django.urls import path
from django.contrib.auth import views as auth_views

from v1.account import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('panel/login/', views.panel_login, name='panel_login'),
    path('panel/logout/', auth_views.LogoutView.as_view(
        next_page='panel_login'), name='logout'),
]