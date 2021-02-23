from django.urls import path
from .views import bot_view

urlpatterns = [
    path('', bot_view),
]