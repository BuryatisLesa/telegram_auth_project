from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.telegram_login, name='telegram_login'),
    path('webhook/', views.webhook, name='webhook'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
