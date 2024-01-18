from django.urls import path
from .views import status
from .views import handlers

urlpatterns = [
    path('status/ready', status.ready, name='ready'),
    path('bot/indizio', handlers.indizio, name='indizio'),
    path('bot/conversation', handlers.conversation, name='conversation'),
    path('bot/auth', handlers.auth, name='auth'),
    path('bot/reset_chat_table', handlers.reset_chat_table, name='reset_chat_table'),
]
