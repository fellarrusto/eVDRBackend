from django.urls import path
from .views import status
from .views import handlers

urlpatterns = [
    path('status/ready', status.ready, name='ready'),
    path('bot/indizio', handlers.indizio, name='indizio'),
    path('bot/conversation', handlers.conversation, name='conversation'),
]
