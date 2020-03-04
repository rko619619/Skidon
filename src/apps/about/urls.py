from django.urls import path
from apps.about.views import TelegramView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [path("telegram/", csrf_exempt(TelegramView.as_view())),]
