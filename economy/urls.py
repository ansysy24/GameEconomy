"""economy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import path, reverse_lazy, include
from django.views.generic import TemplateView


from users import views as user_views
from economy.views import home, market_view, long_polling_view, PurchasesListView, models_view, market_use_cases,\
    stopwatch_view

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/register/', user_views.register, name='register'),
    path('accounts/profile/', user_views.profile, name='profile'),
    path('accounts/<int:pk>/profile/', user_views.profile, name='public-profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', success_url=reverse_lazy('home')),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(), name='change-password'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_change_done'),

    path('market/', market_view, name='market'),
    path('long_polling', long_polling_view, name='long-polling'),
    path('users/', user_views.users_list, name='users'),
    path('purchases/', PurchasesListView.as_view(), name='purchases'),
    path('models/', models_view, name='models'),
    path('market_use_cases/', market_use_cases, name='market-use'),
    path('project_structure/', TemplateView.as_view(template_name='economy/project_structure.html'),
         name='project-structure'),
    path('stopwatch/', stopwatch_view, name='stopwatch'),
    path('sentry-debug/', trigger_error),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
